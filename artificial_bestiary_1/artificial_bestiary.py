#!/usr/bin/env python3
"""
Artificial Bestiary: Ontological Category Presupposition and Confabulation
==========================================================================

Pilot study. 9 novel words × 10 conditions × 20 trials = 1,800 trials.

Conditions are formed by crossing presupposed reality-status (real / imaginary / type of)
with presupposed ontological category (animal / object / idea), plus one plain neutral
condition per word (no presupposition).

Prompt templates:
  neutral:    "Describe a {word}."
  other 9:    "Describe a {word}. It is a {reality} {category}."

Words are verified novel strings with no known referent.

Usage:
    export ANTHROPIC_API_KEY=sk-...

    # Smoke test (no API):
    python artificial_bestiary.py run --dry-run

    # Smoke test (real API, 6 trials):
    python artificial_bestiary.py run --limit 6 --out Results/smoke.jsonl

    # Full run:
    python artificial_bestiary.py run --out Results/results.jsonl

    # Resume after interruption:
    python artificial_bestiary.py run --out Results/results.jsonl --resume

    # Analyze (raw responses, no auto-coder — this is a pilot):
    python artificial_bestiary.py analyze Results/results.jsonl --outdir analysis/
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
from pathlib import Path


# ---------------------------------------------------------------------------
# Study parameters
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 400
TEMPERATURE = 1.0
MAX_WORKERS = 4
MIN_INTERVAL_SEC = 1.5
MAX_RETRIES = 5
BACKOFF_BASE = 3.0
PROGRESS_INTERVAL = 50
TRIALS_PER_CELL = 20
SEED = 20260429

# Nine verified novel words with no known referent.
WORDS = [
    "wresanthamulf",
    "manteoshipuft",
    "zlippparnsie",
    "garnawkinsuth",
    "halthibinny",
    "wertychiops",
    "borthorpunius",
    "kinachitalpo",
    "purtaneolotomous",
]

# 3 reality-status modifiers × 3 ontological categories = 9 presupposition conditions
REALITY_STATUSES = ["real", "imaginary", "type of"]
CATEGORIES       = ["animal", "object", "idea"]

# Condition key → human-readable label and prompt fragment
def _make_conditions() -> dict[str, dict]:
    conds = {}
    # plain neutral — no presupposition
    conds["neutral"] = {
        "label": "neutral",
        "reality": None,
        "category": None,
        "template": "Describe a {word}.",
    }
    for reality, category in product(REALITY_STATUSES, CATEGORIES):
        key = f"{reality.replace(' ', '_')}_{category}"
        # "It is a type of animal." / "It is a real idea." etc.
        # Choose correct indefinite article for the presupposition phrase
        first_word = reality  # "real", "imaginary", "type"
        article = "an" if first_word[0] in "aeiou" else "a"
        conds[key] = {
            "label": key,
            "reality": reality,
            "category": category,
            "template": f"Describe a {{word}}. It is {article} {reality} {category}.",
        }
    return conds

CONDITIONS = _make_conditions()


# ---------------------------------------------------------------------------
# Trial construction
# ---------------------------------------------------------------------------

def build_trials(trials_per_cell: int = TRIALS_PER_CELL, seed: int = SEED) -> list[dict]:
    trials = []
    idx = 0
    for word in WORDS:
        for cond_key, cond in CONDITIONS.items():
            prompt = cond["template"].format(word=word)
            for n in range(trials_per_cell):
                trials.append({
                    "trial_id": f"{idx:05d}",
                    "word": word,
                    "condition": cond_key,
                    "reality": cond["reality"],
                    "category": cond["category"],
                    "trial_n": n,
                    "prompt": prompt,
                })
                idx += 1
    rng = random.Random(seed)
    rng.shuffle(trials)
    return trials


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

class Throttle:
    def __init__(self, min_interval: float):
        self.min_interval = min_interval
        self.last = 0.0
        self.lock = threading.Lock()

    def wait(self) -> None:
        with self.lock:
            now = time.time()
            gap = self.min_interval - (now - self.last)
            if gap > 0:
                time.sleep(gap)
            self.last = time.time()


def run_one(client, trial: dict, throttle: Throttle) -> dict:
    import anthropic
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            throttle.wait()
            t0 = time.time()
            resp = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                messages=[{"role": "user", "content": trial["prompt"]}],
            )
            text = "".join(
                b.text for b in resp.content if getattr(b, "type", None) == "text"
            )
            return {
                **trial,
                "response": text,
                "stop_reason": resp.stop_reason,
                "input_tokens": resp.usage.input_tokens,
                "output_tokens": resp.usage.output_tokens,
                "latency_sec": round(time.time() - t0, 3),
                "attempts": attempt + 1,
                "error": None,
            }
        except (anthropic.APIStatusError, anthropic.APIConnectionError) as e:
            last_err = f"{type(e).__name__}: {e}"
            time.sleep(BACKOFF_BASE ** attempt + random.uniform(0, 1))
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            break
    return {
        **trial,
        "response": None,
        "stop_reason": None,
        "input_tokens": None,
        "output_tokens": None,
        "latency_sec": None,
        "attempts": MAX_RETRIES,
        "error": last_err,
    }


def load_done(path: Path) -> set[str]:
    if not path.exists():
        return set()
    done = set()
    with path.open() as f:
        for line in f:
            try:
                r = json.loads(line)
                if r.get("response") is not None and not r.get("error"):
                    done.add(r["trial_id"])
            except json.JSONDecodeError:
                continue
    return done


def cmd_run(args: argparse.Namespace) -> None:
    trials = build_trials(args.trials_per_cell)
    if args.limit:
        trials = trials[: args.limit]

    total = len(trials)
    n_words = len(WORDS)
    n_conds = len(CONDITIONS)
    print(
        f"Words: {n_words} | Conditions: {n_conds} | "
        f"Trials/cell: {args.trials_per_cell} | Total planned: {n_words * n_conds * args.trials_per_cell}"
    )
    print(f"Running: {total} trials")
    print(
        f"Model: {MODEL} | Temp: {TEMPERATURE} | "
        f"Throttle: {MAX_WORKERS} workers, {MIN_INTERVAL_SEC}s min interval"
    )
    print(f"Estimated runtime: ~{total * MIN_INTERVAL_SEC / MAX_WORKERS / 60:.0f} min")

    if args.dry_run:
        print("\nSample prompts (one per condition):")
        seen = set()
        for t in trials:
            if t["condition"] not in seen:
                seen.add(t["condition"])
                print(f"\n  [{t['condition']}]")
                print(f"  word={t['word']!r}  prompt={t['prompt']!r}")
            if len(seen) == n_conds:
                break
        return

    if "ANTHROPIC_API_KEY" not in os.environ:
        raise SystemExit("Set ANTHROPIC_API_KEY.")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.resume:
        done = load_done(out)
        trials = [t for t in trials if t["trial_id"] not in done]
        print(f"Resume: skipping {len(done)}, running {len(trials)}.")
        mode = "a"
    else:
        if out.exists() and not args.overwrite:
            raise SystemExit(f"{out} exists. Use --resume or --overwrite.")
        mode = "w"

    if not trials:
        print("Nothing to do.")
        return

    import anthropic
    client = anthropic.Anthropic()
    throttle = Throttle(MIN_INTERVAL_SEC)
    completed = failed = 0
    t0 = time.time()

    with out.open(mode) as f:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futs = {pool.submit(run_one, client, t, throttle): t for t in trials}
            for fut in as_completed(futs):
                result = fut.result()
                f.write(json.dumps(result) + "\n")
                f.flush()
                completed += 1
                if result["error"]:
                    failed += 1
                if completed % PROGRESS_INTERVAL == 0 or completed == len(trials):
                    elapsed = time.time() - t0
                    rate = completed / elapsed if elapsed else 0
                    eta = (len(trials) - completed) / rate if rate else 0
                    print(
                        f"  [{completed:>5}/{len(trials)}] "
                        f"failed={failed} | {rate:.2f} t/s | ETA {eta:.0f}s"
                    )

    print(f"\nDone. {completed} trials in {time.time()-t0:.1f}s ({failed} failed).")
    print(f"Output: {out.resolve()}")
    if failed:
        print("Re-run with --resume to retry failures.")


# ---------------------------------------------------------------------------
# Analyzer  (pilot: no auto-coder, just response-length and completion stats)
# ---------------------------------------------------------------------------

def cmd_analyze(args: argparse.Namespace) -> None:
    rows = []
    with open(args.input) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    total = len(rows)
    errors = sum(1 for r in rows if r.get("error"))
    empty  = sum(1 for r in rows if not r.get("error") and not (r.get("response") or "").strip())

    lines = [
        f"Artificial Bestiary — Ontological Category Presupposition Pilot",
        f"================================================================",
        f"Total rows   : {total}",
        f"Errors       : {errors}",
        f"Empty resp.  : {empty}",
        f"Usable       : {total - errors - empty}",
        "",
    ]

    # --- Response length by condition ---
    by_cond: dict[str, list[int]] = defaultdict(list)
    by_word: dict[str, list[int]] = defaultdict(list)
    by_cond_word: dict[tuple, list[int]] = defaultdict(list)

    for r in rows:
        if r.get("error") or not (r.get("response") or "").strip():
            continue
        length = len(r["response"].split())
        cond = r.get("condition", "?")
        word = r.get("word", "?")
        by_cond[cond].append(length)
        by_word[word].append(length)
        by_cond_word[(word, cond)].append(length)

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0.0

    lines += ["Response length (words) by condition:", "-" * 50]
    for cond in sorted(by_cond):
        vals = by_cond[cond]
        lines.append(f"  {cond:<30} n={len(vals):>4}  mean={avg(vals):5.1f}w")

    lines += ["", "Response length (words) by word:", "-" * 50]
    for word in sorted(by_word):
        vals = by_word[word]
        lines.append(f"  {word:<25} n={len(vals):>4}  mean={avg(vals):5.1f}w")

    # --- Completion stats per cell ---
    lines += ["", "Cell completion (word × condition):", "-" * 50]
    for word in WORDS:
        lines.append(f"\n  {word}:")
        for cond in CONDITIONS:
            vals = by_cond_word.get((word, cond), [])
            lines.append(f"    {cond:<30} n={len(vals):>3}")

    # --- Token usage ---
    in_toks  = [r["input_tokens"]  for r in rows if r.get("input_tokens")  is not None]
    out_toks = [r["output_tokens"] for r in rows if r.get("output_tokens") is not None]
    if in_toks:
        lines += [
            "",
            f"Token usage (usable trials):",
            f"  Input  tokens: total={sum(in_toks):,}  mean={avg(in_toks):.1f}",
            f"  Output tokens: total={sum(out_toks):,}  mean={avg(out_toks):.1f}",
        ]

    summary = "\n".join(lines)
    print(summary)
    (outdir / "summary.txt").write_text(summary + "\n", encoding="utf-8")

    # --- Write flat CSV for manual coding ---
    csv_path = outdir / "responses.csv"
    fieldnames = [
        "trial_id", "word", "condition", "reality", "category",
        "trial_n", "prompt", "response", "stop_reason",
        "input_tokens", "output_tokens", "latency_sec", "attempts", "error",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"\nWrote CSV for manual coding: {csv_path.resolve()}")
    print(f"Wrote summary: {(outdir / 'summary.txt').resolve()}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Artificial Bestiary: Ontological Category Presupposition Pilot"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="Run trials against the Anthropic API")
    p_run.add_argument("--out", default="Results/results.jsonl")
    p_run.add_argument("--dry-run", action="store_true",
                       help="Print sample prompts without calling the API")
    p_run.add_argument("--limit", type=int, default=None,
                       help="Run only the first N trials (for smoke tests)")
    p_run.add_argument("--resume", action="store_true",
                       help="Append to existing output, skipping completed trials")
    p_run.add_argument("--overwrite", action="store_true",
                       help="Overwrite existing output file")
    p_run.add_argument("--trials-per-cell", type=int, default=TRIALS_PER_CELL)

    p_an = sub.add_parser("analyze", help="Summarize raw JSONL output")
    p_an.add_argument("input")
    p_an.add_argument("--outdir", default="analysis")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    {"run": cmd_run, "analyze": cmd_analyze}[args.command](args)


if __name__ == "__main__":
    main()
