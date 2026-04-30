#!/usr/bin/env python3
"""
Simple GPT-family pilot runner.

Input CSV needs at least:
  prompt

Recommended extra columns:
  trial_id, word, condition, category, frame, word_set

Example:
  python gpt_pilot_easy.py --input stimuli.csv --pilot 12 --stratify condition

Run all rows later:
  python gpt_pilot_easy.py --input stimuli.csv --pilot 0 --output gpt_full_sync_results.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd
from openai import OpenAI


DEFAULT_MODELS = [
    "gpt-5.4-nano",
    "gpt-5.4-mini",
    "gpt-5.4",
]

# Current standard, non-Batch prices per 1M tokens.
# Check OpenAI pricing before final publication.
PRICING = {
    "gpt-5.4-nano": {"input": 0.20, "output": 1.25},
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50},
    "gpt-5.4": {"input": 2.50, "output": 15.00},
}

DEFAULT_MAX_OUTPUT_TOKENS = 700


def to_dict(obj: Any) -> dict:
    """Convert OpenAI SDK objects, dicts, or None into plain dicts."""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    try:
        return dict(obj)
    except Exception:
        return {}


def choose_pilot_rows(
    df: pd.DataFrame,
    pilot: int,
    stratify: str | None,
    seed: int,
) -> pd.DataFrame:
    """Pick a small pilot sample. pilot <= 0 means use all rows."""
    if pilot <= 0 or pilot >= len(df):
        return df.copy()

    if stratify and stratify in df.columns:
        groups = list(df.groupby(stratify, dropna=False))
        per_group = max(1, math.ceil(pilot / len(groups)))

        parts = []
        for _, g in groups:
            n = min(per_group, len(g))
            parts.append(g.sample(n=n, random_state=seed))

        sampled = pd.concat(parts).sample(frac=1, random_state=seed)

        if len(sampled) > pilot:
            sampled = sampled.sample(n=pilot, random_state=seed)

        return sampled.reset_index(drop=True)

    return df.sample(n=pilot, random_state=seed).reset_index(drop=True)


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    rates = PRICING.get(model)
    if not rates:
        return 0.0

    return (
        input_tokens / 1_000_000 * rates["input"]
        + output_tokens / 1_000_000 * rates["output"]
    )


def get_usage_numbers(response: Any) -> tuple[int, int, int, dict]:
    usage = to_dict(getattr(response, "usage", None))
    input_tokens = int(usage.get("input_tokens", 0) or 0)
    output_tokens = int(usage.get("output_tokens", 0) or 0)
    total_tokens = int(usage.get("total_tokens", input_tokens + output_tokens) or 0)
    return input_tokens, output_tokens, total_tokens, usage


def call_model(
    client: OpenAI,
    model: str,
    prompt: str,
    max_output_tokens: int,
    reasoning_effort: str,
    retries: int,
) -> tuple[str, dict, str, str]:
    """
    Returns:
      output_text, usage_dict, response_status, error_string
    """
    request = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 1.0,
        "top_p": 1.0,
        "max_output_tokens": max_output_tokens,
        "store": False,
        "tools": [],
    }

    if reasoning_effort != "omit":
        request["reasoning"] = {"effort": reasoning_effort}

    last_error = ""

    for attempt in range(1, retries + 1):
        try:
            response = client.responses.create(**request)

            output_text = getattr(response, "output_text", "") or ""
            status = getattr(response, "status", "") or ""

            _, _, _, usage = get_usage_numbers(response)

            return output_text, usage, status, ""

        except Exception as e:
            last_error = repr(e)

            if attempt < retries:
                sleep_s = min(30, 2 ** attempt)
                print(f"  Error on {model}, attempt {attempt}/{retries}: {last_error}")
                print(f"  Sleeping {sleep_s}s, then retrying...")
                time.sleep(sleep_s)

    return "", {}, "error", last_error


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True, help="CSV with at least a prompt column.")
    parser.add_argument("--output", default="gpt_pilot_results.csv")
    parser.add_argument(
        "--pilot",
        type=int,
        default=12,
        help="Number of stimulus rows to sample. Use 0 to run all rows.",
    )
    parser.add_argument(
        "--stratify",
        default=None,
        help="Optional column to sample across, e.g. condition or category.",
    )
    parser.add_argument(
        "--models",
        default=",".join(DEFAULT_MODELS),
        help="Comma-separated model list.",
    )
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--max-output-tokens", type=int, default=DEFAULT_MAX_OUTPUT_TOKENS)
    parser.add_argument(
        "--reasoning",
        default="none",
        help='Reasoning effort: "none", "minimal", "low", "medium", etc., or "omit".',
    )
    parser.add_argument("--retries", type=int, default=3)

    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("Missing OPENAI_API_KEY. Set it first, e.g.:")
        print('  export OPENAI_API_KEY="sk-..."')
        sys.exit(1)

    df = pd.read_csv(args.input)

    if "prompt" not in df.columns:
        raise SystemExit("Input CSV must contain a column named 'prompt'.")

    if "trial_id" not in df.columns:
        df.insert(0, "trial_id", [f"trial_{i:05d}" for i in range(len(df))])

    pilot_df = choose_pilot_rows(
        df=df,
        pilot=args.pilot,
        stratify=args.stratify,
        seed=args.seed,
    )

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    client = OpenAI()

    out_path = Path(args.output)

    input_cols = list(pilot_df.columns)
    result_cols = [
        "model",
        "output_text",
        "response_status",
        "error",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "estimated_cost_usd",
        "usage_json",
    ]

    fieldnames = input_cols + result_cols

    total_cost = 0.0
    total_calls = len(pilot_df) * len(models)
    done = 0

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for _, row in pilot_df.iterrows():
            prompt = str(row["prompt"])

            for model in models:
                done += 1
                trial_id = row.get("trial_id", "")
                print(f"[{done}/{total_calls}] {model} | {trial_id}")

                output_text, usage, status, error = call_model(
                    client=client,
                    model=model,
                    prompt=prompt,
                    max_output_tokens=args.max_output_tokens,
                    reasoning_effort=args.reasoning,
                    retries=args.retries,
                )

                input_tokens = int(usage.get("input_tokens", 0) or 0)
                output_tokens = int(usage.get("output_tokens", 0) or 0)
                total_tokens = int(usage.get("total_tokens", input_tokens + output_tokens) or 0)

                cost = estimate_cost(model, input_tokens, output_tokens)
                total_cost += cost

                out_row = row.to_dict()
                out_row.update(
                    {
                        "model": model,
                        "output_text": output_text,
                        "response_status": status,
                        "error": error,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "total_tokens": total_tokens,
                        "estimated_cost_usd": cost,
                        "usage_json": json.dumps(usage, ensure_ascii=False),
                    }
                )

                writer.writerow(out_row)
                f.flush()

    print()
    print(f"Done. Wrote: {out_path}")
    print(f"Rows run: {len(pilot_df)} stimuli × {len(models)} models = {total_calls} calls")
    print(f"Estimated API cost from reported usage: ${total_cost:.4f}")


if __name__ == "__main__":
    main()