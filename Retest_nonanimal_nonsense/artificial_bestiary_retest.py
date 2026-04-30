#!/usr/bin/env python3
"""
Artificial Bestiary — Word-Shape Confound Retest
=================================================

Pilot follow-up. Tests whether the four "your words" generated with imaginary-
animal intent (halthibinny, purtaneolotomous, borthorpunius, wresanthamulf) show
a different engagement profile in the imaginary conditions than four newly-
generated words with no category intent (flembrast, trolnique, kovashent,
plindorf).

8 words × 10 conditions × 10 trials = 800 trials.

Same model, temperature, throttling, and prompt templates as the original pilot,
so the JSONL output can be passed through code_responses.py unchanged.

The diagnostic question: within imaginary_*, do your-words and ambiguous-words
show different DESCRIBE/HYBRID/DEFLECT distributions, and in particular, is
imaginary_animal disproportionately engaging for your-words relative to
imaginary_object and imaginary_idea?

Usage:
    export ANTHROPIC_API_KEY=sk-...

    # Smoke test (no API):
    python artificial_bestiary_retest.py run --dry-run

    # Smoke test (real API, 8 trials — one per condition):
    python artificial_bestiary_retest.py run --limit 8 --out Results/retest_smoke.jsonl

    # Full retest:
    python artificial_bestiary_retest.py run --out Results/retest.jsonl

    # Resume after interruption:
    python artificial_bestiary_retest.py run --out Results/retest.jsonl --resume

    # Code with existing auto-coder, then analyze:
    python code_responses.py Results/retest.jsonl --out Results/retest_coded.jsonl --csv Results/retest_coded.csv
    python artificial_bestiary_retest.py compare Results/retest_coded.csv --pilot results_coded.csv
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
# Study parameters  (kept identical to the original pilot where possible)
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 400
TEMPERATURE = 1.0
MAX_WORKERS = 4
MIN_INTERVAL_SEC = 1.5
MAX_RETRIES = 5
BACKOFF_BASE = 3.0
PROGRESS_INTERVAL = 50
TRIALS_PER_CELL = 10                 # halved from pilot's 20
SEED = 20260430                      # fresh seed so trial order differs

# Two word-sets, tagged so we can compare them in analysis.
#
# YOUR words: from the original pilot, generated with imaginary-animal intent.
# AMBIGUOUS words: newly generated, deliberately phonotactically varied with
#   no category intent. Two lean object-ish (plindorf, flembrast), one
#   lean idea-ish (kovashent), one ambiguous (trolnique). The goal is to
#   pull AWAY from any residual animal bias the original word-set may have.
WORD_SETS = {
    "your":      ["halthibinny", "purtaneolotomous", "borthorpunius", "wresanthamulf"],
    "ambiguous": ["flembrast",   "trolnique",        "kovashent",     "plindorf"],
}

# Flatten + tag
WORDS_TAGGED = [(w, tag) for tag, words in WORD_SETS.items() for w in words]
WORDS = [w for w, _ in WORDS_TAGGED]
WORD_TAG = dict(WORDS_TAGGED)

# Same conditions as pilot.
REALITY_STATUSES = ["real", "imaginary", "type of"]
CATEGORIES       = ["animal", "object", "idea"]


def _make_conditions() -> dict[str, dict]:
    conds = {
        "neutral": {
            "label": "neutral",
            "reality": None,
            "category": None,
            "template": "Describe a {word}.",
        }
    }
    for reality, category in product(REALITY_STATUSES, CATEGORIES):
        key = f"{reality.replace(' ', '_')}_{category}"
        article = "an" if reality[0] in "aeiou" else "a"
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
                    "trial_id": f"r{idx:05d}",       # 'r' prefix to mark retest
                    "word": word,
                    "word_set": WORD_TAG[word],     # 'your' or 'ambiguous'
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
# Runner  (verbatim from original pilot; unchanged on purpose)
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
        f"Words: {n_words} ({len(WORD_SETS['your'])} 'your' + "
        f"{len(WORD_SETS['ambiguous'])} 'ambiguous') | "
        f"Conditions: {n_conds} | Trials/cell: {args.trials_per_cell} | "
        f"Total planned: {n_words * n_conds * args.trials_per_cell}"
    )
    print(f"Running: {total} trials")
    print(
        f"Model: {MODEL} | Temp: {TEMPERATURE} | "
        f"Throttle: {MAX_WORKERS} workers, {MIN_INTERVAL_SEC}s min interval"
    )
    print(f"Estimated runtime: ~{total * MIN_INTERVAL_SEC / MAX_WORKERS / 60:.0f} min")

    if args.dry_run:
        print("\nWord set tags:")
        for tag, words in WORD_SETS.items():
            print(f"  {tag:<10} {words}")
        print("\nSample prompts (one per condition):")
        seen = set()
        for t in trials:
            if t["condition"] not in seen:
                seen.add(t["condition"])
                print(f"\n  [{t['condition']}]  word_set={t['word_set']}")
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
# Compare:  word_set × condition × tier1 cross-tab, on coded retest data.
# ---------------------------------------------------------------------------
# This is the diagnostic. Reads coded CSV (output of code_responses.py),
# tags each row by word_set, and prints the imaginary-condition profiles
# side-by-side. If 'your' and 'ambiguous' look similar, the word-shape
# confound is small. If 'your' shows higher engagement (esp. in
# imaginary_animal) than 'ambiguous', the confound is real.

def cmd_compare(args: argparse.Namespace) -> None:
    rows = []
    with open(args.input, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    # Tag by word_set if not already present (the coder strips word_set,
    # since it's not a known column in the original pilot).
    for r in rows:
        if "word_set" not in r or not r["word_set"]:
            r["word_set"] = WORD_TAG.get(r["word"], "?")

    def pct_table(subset, conditions, codes):
        table = {}
        for cond in conditions:
            cell = [r for r in subset if r["condition"] == cond]
            n = len(cell)
            if n == 0:
                table[cond] = {c: 0.0 for c in codes} | {"n": 0}
                continue
            cnt = Counter(r["tier1"] for r in cell)
            row = {c: 100.0 * cnt.get(c, 0) / n for c in codes}
            row["n"] = n
            table[cond] = row
        return table

    codes = ["DESCRIBE", "HYBRID", "DEFLECT", "REFUSE"]
    imag_conds = ["imaginary_animal", "imaginary_object", "imaginary_idea"]
    type_conds = ["type_of_animal",   "type_of_object",   "type_of_idea"]
    real_conds = ["real_animal",      "real_object",      "real_idea", "neutral"]

    your = [r for r in rows if r["word_set"] == "your"]
    ambig = [r for r in rows if r["word_set"] == "ambiguous"]

    print(f"\n{'='*78}")
    print(f"Retest comparison: {len(your)} 'your' rows | {len(ambig)} 'ambiguous' rows")
    print(f"{'='*78}\n")

    def print_block(title, conds):
        print(f"--- {title} ---")
        header = f"{'condition':<22} {'set':<10} " + " ".join(f"{c:>10}" for c in codes) + f"  {'n':>4}"
        print(header)
        for cond in conds:
            for label, subset in [("your", your), ("ambiguous", ambig)]:
                t = pct_table(subset, [cond], codes)[cond]
                vals = " ".join(f"{t[c]:>9.1f}%" for c in codes)
                print(f"  {cond:<20} {label:<10} {vals}  {t['n']:>4}")
            print()
        print()

    print_block("IMAGINARY conditions (the diagnostic)", imag_conds)
    print_block("TYPE-OF conditions",                    type_conds)
    print_block("REAL / NEUTRAL conditions (sanity check — should be ~100% REFUSE)",
                real_conds)

    # Compact summary: engagement rate (DESCRIBE + HYBRID) per cell, both sets.
    print("\n--- Engagement rate (DESCRIBE + HYBRID), imaginary conditions ---")
    print(f"{'condition':<22} {'your %':>10} {'ambig %':>10} {'diff':>10}")
    for cond in imag_conds:
        your_eng  = sum(1 for r in your  if r["condition"] == cond and r["tier1"] in ("DESCRIBE","HYBRID"))
        your_n    = sum(1 for r in your  if r["condition"] == cond)
        ambig_eng = sum(1 for r in ambig if r["condition"] == cond and r["tier1"] in ("DESCRIBE","HYBRID"))
        ambig_n   = sum(1 for r in ambig if r["condition"] == cond)
        yp = 100*your_eng/your_n if your_n else 0
        ap = 100*ambig_eng/ambig_n if ambig_n else 0
        print(f"  {cond:<20} {yp:>9.1f}% {ap:>9.1f}% {yp-ap:>+9.1f}pp")

    # Optional: compare against pilot baseline
    if args.pilot:
        print(f"\n--- Pilot baseline (from {args.pilot}) ---")
        pilot_rows = []
        with open(args.pilot, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                pilot_rows.append(r)
        # Pilot's nine words are all "your"-style; engagement rate per condition:
        for cond in imag_conds:
            cell = [r for r in pilot_rows if r["condition"] == cond]
            n = len(cell)
            eng = sum(1 for r in cell if r["tier1"] in ("DESCRIBE","HYBRID"))
            print(f"  {cond:<20} pilot engagement = {100*eng/n:5.1f}%  (n={n})")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Artificial Bestiary retest: word-shape confound diagnostic"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="Run retest trials against the Anthropic API")
    p_run.add_argument("--out", default="Results/retest.jsonl")
    p_run.add_argument("--dry-run", action="store_true",
                       help="Print sample prompts without calling the API")
    p_run.add_argument("--limit", type=int, default=None,
                       help="Run only the first N trials (for smoke tests)")
    p_run.add_argument("--resume", action="store_true",
                       help="Append to existing output, skipping completed trials")
    p_run.add_argument("--overwrite", action="store_true",
                       help="Overwrite existing output file")
    p_run.add_argument("--trials-per-cell", type=int, default=TRIALS_PER_CELL)

    p_cmp = sub.add_parser("compare", help="Compare 'your' vs 'ambiguous' on coded CSV")
    p_cmp.add_argument("input", help="Coded CSV from code_responses.py")
    p_cmp.add_argument("--pilot", default=None,
                       help="Optional pilot coded CSV for baseline comparison")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    {"run": cmd_run, "compare": cmd_compare}[args.command](args)


if __name__ == "__main__":
    main()
