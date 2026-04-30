#!/usr/bin/env python3
"""
Rich analysis for Artificial Bestiary JSONL results.

What this does
--------------
1. Loads the raw JSONL output from artificial_bestiary.py.
2. Adds transparent, regex-based response coding:
   - response length and structure
   - uncertainty / epistemic caveats
   - refusal or "do not invent" language
   - creative / fictional framing
   - substantive generation / high specificity
   - animal / object / idea term uptake
   - category alignment with the prompt
3. Writes descriptive summaries by condition, word, reality, category, and reality × category.
4. Treats `neutral` as the baseline and compares every framed condition against it.
5. Runs exploratory inferential models when scipy/statsmodels are available:
   - Welch tests / Fisher exact tests vs neutral
   - OLS condition models for continuous outcomes
   - GLM-logit condition models for binary outcomes
   - 3 × 3 factorial OLS models among presupposed conditions only
6. Optionally writes a few simple matplotlib plots.

The coding is intentionally auditable. It is not a validated human-coding substitute.
Use it to triage patterns and select examples for manual review.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import textwrap
import warnings
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

try:
    from scipy import stats
    from statsmodels.stats.multitest import multipletests
except Exception:  # pragma: no cover
    stats = None
    multipletests = None

try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
except Exception:  # pragma: no cover
    sm = None
    smf = None

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    plt = None


# ---------------------------------------------------------------------
# Regex coder
# ---------------------------------------------------------------------

UNCERTAINTY_RE = re.compile(
    r"\b(?:might|may|could|possibly|perhaps|seems|appears|likely|probably|unclear|"
    r"unsure|unknown|not sure|I don't know|I do not know|doesn't appear|does not appear|"
    r"no known|not in my|can't verify|cannot verify|without more context)\b",
    re.I,
)

EPISTEMIC_CAVEAT_RE = re.compile(
    r"(doesn['’]?t appear|does not appear|not (?:in|part of) my (?:knowledge|training)|"
    r"no known (?:referent|meaning|definition)|I (?:don['’]?t|do not) (?:recognize|know)|"
    r"can't verify|cannot verify|I (?:can['’]?t|cannot) confirm|not a recognized|"
    r"not an established|I (?:shouldn['’]?t|will not|won['’]?t) invent|"
    r"rather than invent|would be misleading)",
    re.I,
)

REFUSAL_RE = re.compile(
    r"(I (?:can['’]?t|cannot) (?:accurately )?(?:describe|provide|give)|"
    r"I (?:shouldn['’]?t|will not|won['’]?t) invent|rather than invent|"
    r"would be misleading|no factual description|can't provide a factual|"
    r"cannot provide a factual)",
    re.I,
)

CREATIVE_FRAME_RE = re.compile(
    r"(imaginary|fictional|invented|creative|speculative|made[- ]up|fantasy|"
    r"fantastical|hypothetical|if we treat|could be described|might be imagined|"
    r"let'?s imagine|for a fictional)",
    re.I,
)

# Narrow taxonomic-style marker. Avoid broad "Species" alone because many refusals mention
# "newly described species" without generating taxonomy.
TAXONOMY_STYLE_RE = re.compile(
    r"(\b(?:scientific name|taxonomy|taxonomic classification|classification:|"
    r"genus:|family:|order:|latin name)\b|"
    r"[\(\*_]\s*[A-Z][a-z]{3,}\s+[a-z]{4,}\s*[\)\*_])",
    re.I,
)

ANIMAL_TERMS_RE = re.compile(
    r"\b(?:animal|creature|species|organism|mammal|reptile|bird|insect|fish|"
    r"amphibian|beast|predator|prey|herbivore|carnivore|omnivore|nocturnal|"
    r"diurnal|habitat|forest|jungle|desert|ocean|river|mountain|burrow|nest|"
    r"eggs?|offspring|fur|scales?|feathers?|wings?|tail|legs?|claws?|teeth|"
    r"beak|antennae|shell|feeds?|eats?|diet|mates?|migrat(?:e|es|ion))\b",
    re.I,
)

OBJECT_TERMS_RE = re.compile(
    r"\b(?:object|tool|device|instrument|artifact|artefact|machine|mechanism|"
    r"material|wood|metal|stone|glass|ceramic|plastic|surface|edge|handle|"
    r"base|hinge|container|vessel|box|disc|sphere|cube|shape|size|palm-sized|"
    r"weight|texture|smooth|rough|used for|function|designed to|component|parts?)\b",
    re.I,
)

IDEA_TERMS_RE = re.compile(
    r"\b(?:idea|concept|theory|belief|principle|notion|philosophy|framework|"
    r"paradigm|ideology|thought|cognitive|mental|abstract|metaphor|symbolic|"
    r"meaning|interpretation|argument|proposition|doctrine|methodology|approach|"
    r"perspective|epistemic|ontological|ethical|aesthetic)\b",
    re.I,
)

PHYSICAL_RE = re.compile(
    r"\b(?:appearance|looks?|shaped|shape|size|color|colour|hue|body|surface|"
    r"texture|smooth|rough|translucent|opaque|glowing|iridescent|limbs?|eyes?|"
    r"mouth|tail|wings?|fur|scales?|shell|metal|wood|stone|glass|ceramic|soft|"
    r"hard|round|flat|elongated|palm-sized)\b",
    re.I,
)

BEHAVIOR_RE = re.compile(
    r"\b(?:behavior|behaviour|moves?|crawls?|flies|swims?|hunts?|feeds?|eats?|"
    r"diet|nests?|burrows?|migrates?|communicates?|mates?|reproduces?|lives?|"
    r"inhabits?|dwells?|habitat|predator|prey|social|solitary|nocturnal|diurnal)\b",
    re.I,
)

FUNCTION_RE = re.compile(
    r"\b(?:function|used for|useful|designed to|serves to|purpose|tool|device|"
    r"instrument|mechanism|operates?|works by|activate|process|component|parts?|"
    r"mechanical|signal|measure|store|transport|hold)\b",
    re.I,
)

ABSTRACT_RE = re.compile(
    r"\b(?:abstract|concept|idea|theory|principle|philosophy|framework|metaphor|"
    r"symbol|belief|meaning|interpretation|cognitive|mental|ethical|aesthetic|"
    r"epistemic|ontological|social|cultural|logic|paradox)\b",
    re.I,
)

OFFER_OR_CONTEXT_RE = re.compile(
    r"(could you (?:give|provide|share)|provide more context|where did you encounter|"
    r"if you(?:'d| would) like|help you (?:define|build|develop)|happy to help)",
    re.I,
)


def count_re(regex: re.Pattern, text: str | None) -> int:
    return len(regex.findall(text or ""))


def word_count(text: str | None) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


def sentence_count(text: str | None) -> int:
    if not text or not text.strip():
        return 0
    return max(1, len(re.findall(r"[.!?]+(?:\s|$)", text)))


def infer_category(text: str | None) -> str:
    counts = {
        "animal": count_re(ANIMAL_TERMS_RE, text),
        "object": count_re(OBJECT_TERMS_RE, text),
        "idea": count_re(IDEA_TERMS_RE, text),
    }
    mx = max(counts.values())
    if mx == 0:
        return "unclear"
    winners = [k for k, v in counts.items() if v == mx]
    return winners[0] if len(winners) == 1 else "mixed"


# ---------------------------------------------------------------------
# Loading and feature engineering
# ---------------------------------------------------------------------

def load_jsonl(path: str | Path) -> pd.DataFrame:
    rows = []
    with Path(path).open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON decode error at line {line_no}: {e}") from e
    return pd.DataFrame(rows)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Ensure expected columns exist, so partially complete runs still analyze.
    defaults = {
        "response": "",
        "error": None,
        "condition": "unknown",
        "word": "unknown",
        "reality": None,
        "category": None,
        "input_tokens": np.nan,
        "output_tokens": np.nan,
        "latency_sec": np.nan,
    }
    for col, default in defaults.items():
        if col not in out.columns:
            out[col] = default

    text = out["response"].fillna("").astype(str)

    out["usable"] = out["error"].isna() & text.str.strip().ne("")
    out["word_count"] = text.apply(word_count)
    out["char_count"] = text.str.len()
    out["sentence_count"] = text.apply(sentence_count)
    out["bullet_count"] = text.apply(
        lambda s: len(re.findall(r"(?m)^\s*(?:[-*•]|\d+\.)\s+", s or ""))
    )

    out["uncertainty_count"] = text.apply(lambda s: count_re(UNCERTAINTY_RE, s))
    out["uncertainty_present"] = out["uncertainty_count"] > 0
    out["epistemic_caveat"] = text.apply(lambda s: bool(EPISTEMIC_CAVEAT_RE.search(s or "")))
    out["refusal_or_noninvent"] = text.apply(lambda s: bool(REFUSAL_RE.search(s or "")))
    out["creative_frame"] = text.apply(lambda s: bool(CREATIVE_FRAME_RE.search(s or "")))
    out["taxonomy_marker"] = text.apply(lambda s: bool(TAXONOMY_STYLE_RE.search(s or "")))
    out["offer_or_context_request"] = text.apply(lambda s: bool(OFFER_OR_CONTEXT_RE.search(s or "")))

    out["physical_description"] = text.apply(lambda s: bool(PHYSICAL_RE.search(s or "")))
    out["behavior_ecology"] = text.apply(lambda s: bool(BEHAVIOR_RE.search(s or "")))
    out["function_mechanism"] = text.apply(lambda s: bool(FUNCTION_RE.search(s or "")))
    out["abstract_conceptual"] = text.apply(lambda s: bool(ABSTRACT_RE.search(s or "")))

    out["animal_terms_count"] = text.apply(lambda s: count_re(ANIMAL_TERMS_RE, s))
    out["object_terms_count"] = text.apply(lambda s: count_re(OBJECT_TERMS_RE, s))
    out["idea_terms_count"] = text.apply(lambda s: count_re(IDEA_TERMS_RE, s))
    out["specific_terms_total"] = (
        out["animal_terms_count"] + out["object_terms_count"] + out["idea_terms_count"]
    )

    out["predicted_category"] = text.apply(infer_category)
    out["prompt_category"] = out["category"].fillna("neutral")
    out["reality_full"] = out["reality"].fillna("neutral")
    out["category_full"] = out["category"].fillna("neutral")
    out["presupposed"] = out["condition"].ne("neutral")

    out["category_aligned"] = np.where(
        out["prompt_category"].eq("neutral"),
        np.nan,
        out["predicted_category"].eq(out["prompt_category"]).astype(float),
    )

    out["domain_marker_variety"] = out[
        [
            "physical_description",
            "behavior_ecology",
            "function_mechanism",
            "abstract_conceptual",
            "taxonomy_marker",
        ]
    ].sum(axis=1)

    # Heuristic coding definitions:
    # - high_specificity: several category/domain terms, rarely triggered by pure nonanswers.
    # - substantive_generation: high specificity OR multiple domain markers in a long response.
    # These should be checked against hand-coded examples before publication.
    out["high_specificity"] = out["specific_terms_total"] >= 6
    out["substantive_generation"] = (
        out["high_specificity"]
        | ((out["domain_marker_variety"] >= 2) & (out["word_count"] >= 120))
    )
    out["cautious_nonanswer"] = (
        out["epistemic_caveat"]
        & out["offer_or_context_request"]
        & ~out["substantive_generation"]
    )
    out["caveated_generation"] = out["epistemic_caveat"] & out["substantive_generation"]

    # Model-friendly integer versions of binary variables.
    binary_cols = [
        "usable",
        "presupposed",
        "uncertainty_present",
        "epistemic_caveat",
        "refusal_or_noninvent",
        "creative_frame",
        "taxonomy_marker",
        "offer_or_context_request",
        "physical_description",
        "behavior_ecology",
        "function_mechanism",
        "abstract_conceptual",
        "high_specificity",
        "substantive_generation",
        "cautious_nonanswer",
        "caveated_generation",
    ]
    for col in binary_cols:
        out[f"{col}_int"] = out[col].astype(int)

    return out


# ---------------------------------------------------------------------
# Descriptives
# ---------------------------------------------------------------------

CONTINUOUS_FEATURES = [
    "word_count",
    "char_count",
    "sentence_count",
    "bullet_count",
    "input_tokens",
    "output_tokens",
    "latency_sec",
    "uncertainty_count",
    "animal_terms_count",
    "object_terms_count",
    "idea_terms_count",
    "specific_terms_total",
    "domain_marker_variety",
]

BINARY_FEATURES = [
    "usable",
    "uncertainty_present",
    "epistemic_caveat",
    "refusal_or_noninvent",
    "creative_frame",
    "taxonomy_marker",
    "offer_or_context_request",
    "physical_description",
    "behavior_ecology",
    "function_mechanism",
    "abstract_conceptual",
    "high_specificity",
    "substantive_generation",
    "cautious_nonanswer",
    "caveated_generation",
]


def summarize_group(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    g = df.groupby(group_cols, dropna=False)
    out = g.size().to_frame("n")

    for col in CONTINUOUS_FEATURES:
        if col in df.columns:
            out[f"{col}_mean"] = g[col].mean()
            out[f"{col}_sd"] = g[col].std()
            out[f"{col}_median"] = g[col].median()
            out[f"{col}_min"] = g[col].min()
            out[f"{col}_max"] = g[col].max()

    for col in BINARY_FEATURES:
        if col in df.columns:
            out[f"{col}_rate"] = g[col].mean()
            out[f"{col}_count"] = g[col].sum()

    out["category_aligned_rate"] = g["category_aligned"].mean()
    out["category_aligned_count"] = g["category_aligned"].sum(min_count=1)

    return out.reset_index()


def predicted_category_table(df: pd.DataFrame) -> pd.DataFrame:
    tab = (
        pd.crosstab(df["condition"], df["predicted_category"], normalize="index")
        .reset_index()
        .rename_axis(None, axis=1)
    )
    counts = pd.crosstab(df["condition"], df["predicted_category"]).reset_index()
    counts.columns = [
        "condition" if c == "condition" else f"{c}_count" for c in counts.columns
    ]
    return tab.merge(counts, on="condition", how="left")


# ---------------------------------------------------------------------
# Baseline comparisons and exploratory models
# ---------------------------------------------------------------------

def cohen_d(x: Iterable[float], y: Iterable[float]) -> float:
    x = pd.Series(x).dropna().astype(float).to_numpy()
    y = pd.Series(y).dropna().astype(float).to_numpy()
    if len(x) < 2 or len(y) < 2:
        return np.nan
    sx, sy = x.std(ddof=1), y.std(ddof=1)
    sp = math.sqrt(((len(x) - 1) * sx**2 + (len(y) - 1) * sy**2) / (len(x) + len(y) - 2))
    return (x.mean() - y.mean()) / sp if sp else np.nan


def baseline_pairwise(df: pd.DataFrame, baseline_condition: str = "neutral") -> pd.DataFrame:
    rows = []
    base = df[df["condition"] == baseline_condition]
    if base.empty:
        return pd.DataFrame()

    continuous_outcomes = [
        "word_count",
        "output_tokens",
        "uncertainty_count",
        "specific_terms_total",
        "domain_marker_variety",
    ]
    binary_outcomes = [
        "epistemic_caveat",
        "refusal_or_noninvent",
        "creative_frame",
        "high_specificity",
        "substantive_generation",
        "cautious_nonanswer",
        "caveated_generation",
    ]

    for cond, sub in df[df["condition"] != baseline_condition].groupby("condition"):
        for outcome in continuous_outcomes:
            if outcome not in df.columns or stats is None:
                continue
            x = sub[outcome].dropna()
            y = base[outcome].dropna()
            if len(x) < 2 or len(y) < 2:
                continue
            stat, p = stats.ttest_ind(x, y, equal_var=False)
            rows.append(
                {
                    "condition": cond,
                    "baseline": baseline_condition,
                    "outcome": outcome,
                    "test": "Welch t",
                    "condition_mean": x.mean(),
                    "baseline_mean": y.mean(),
                    "difference": x.mean() - y.mean(),
                    "effect_size": cohen_d(x, y),
                    "statistic": stat,
                    "p": p,
                }
            )

        for outcome in binary_outcomes:
            if outcome not in df.columns or stats is None:
                continue
            a = int(sub[outcome].sum())
            b = int(len(sub) - a)
            c = int(base[outcome].sum())
            d = int(len(base) - c)
            odds_ratio, p = stats.fisher_exact([[a, b], [c, d]])
            rows.append(
                {
                    "condition": cond,
                    "baseline": baseline_condition,
                    "outcome": outcome,
                    "test": "Fisher exact",
                    "condition_mean": sub[outcome].mean(),
                    "baseline_mean": base[outcome].mean(),
                    "difference": sub[outcome].mean() - base[outcome].mean(),
                    "effect_size": odds_ratio,
                    "statistic": odds_ratio,
                    "p": p,
                }
            )

    out = pd.DataFrame(rows)
    if not out.empty and multipletests is not None:
        out["p_holm"] = np.nan
        for outcome, idx in out.groupby("outcome").groups.items():
            out.loc[idx, "p_holm"] = multipletests(out.loc[idx, "p"], method="holm")[1]
    return out


def write_model_tables(df: pd.DataFrame, outdir: Path) -> dict[str, str]:
    paths: dict[str, str] = {}
    if smf is None or sm is None:
        return paths

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        continuous_outcomes = [
            "word_count",
            "output_tokens",
            "uncertainty_count",
            "specific_terms_total",
            "domain_marker_variety",
        ]

        # Condition-vs-neutral OLS models with word-clustered standard errors.
        for outcome in continuous_outcomes:
            if outcome not in df.columns:
                continue
            try:
                model = smf.ols(
                    f'{outcome} ~ C(condition, Treatment(reference="neutral"))',
                    data=df,
                ).fit(cov_type="cluster", cov_kwds={"groups": df["word"]})
                model_path = outdir / f"model_ols_condition_{outcome}.txt"
                model_path.write_text(model.summary().as_text(), encoding="utf-8")
                paths[f"ols_condition_{outcome}"] = str(model_path)
            except Exception as e:
                (outdir / f"model_ols_condition_{outcome}_ERROR.txt").write_text(
                    repr(e), encoding="utf-8"
                )

        # Binary GLM-logit condition models. Perfect or quasi-complete separation can occur;
        # errors are captured to text files instead of stopping the analysis.
        binary_outcomes = [
            "epistemic_caveat",
            "refusal_or_noninvent",
            "creative_frame",
            "high_specificity",
            "substantive_generation",
            "cautious_nonanswer",
            "caveated_generation",
        ]
        for outcome in binary_outcomes:
            int_col = f"{outcome}_int"
            if int_col not in df.columns:
                continue
            try:
                model = smf.glm(
                    f'{int_col} ~ C(condition, Treatment(reference="neutral"))',
                    data=df,
                    family=sm.families.Binomial(),
                ).fit(cov_type="cluster", cov_kwds={"groups": df["word"]})
                model_path = outdir / f"model_glm_condition_{outcome}.txt"
                model_path.write_text(model.summary().as_text(), encoding="utf-8")
                paths[f"glm_condition_{outcome}"] = str(model_path)
            except Exception as e:
                (outdir / f"model_glm_condition_{outcome}_ERROR.txt").write_text(
                    repr(e), encoding="utf-8"
                )

        # 3 × 3 factorial OLS among presupposed conditions only.
        pres = df[df["condition"] != "neutral"].copy()
        for outcome in continuous_outcomes:
            if pres.empty or outcome not in pres.columns:
                continue
            try:
                model = smf.ols(f"{outcome} ~ C(reality) * C(category)", data=pres).fit()
                anova = sm.stats.anova_lm(model, typ=2)
                anova_path = outdir / f"anova_presupposed_reality_x_category_{outcome}.csv"
                anova.to_csv(anova_path)
                paths[f"anova_presupposed_{outcome}"] = str(anova_path)

                clustered = smf.ols(f"{outcome} ~ C(reality) * C(category)", data=pres).fit(
                    cov_type="cluster", cov_kwds={"groups": pres["word"]}
                )
                model_path = outdir / f"model_ols_presupposed_reality_x_category_{outcome}.txt"
                model_path.write_text(clustered.summary().as_text(), encoding="utf-8")
                paths[f"ols_presupposed_{outcome}"] = str(model_path)
            except Exception as e:
                (outdir / f"model_ols_presupposed_{outcome}_ERROR.txt").write_text(
                    repr(e), encoding="utf-8"
                )

    return paths


# ---------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------

def add_ci(summary: pd.DataFrame, mean_col: str, sd_col: str, n_col: str = "n") -> pd.DataFrame:
    out = summary.copy()
    out["ci95"] = 1.96 * out[sd_col] / np.sqrt(out[n_col])
    return out


def make_plots(df: pd.DataFrame, by_condition: pd.DataFrame, outdir: Path) -> list[str]:
    if plt is None:
        return []
    paths = []

    order = [
        "neutral",
        "real_animal",
        "real_object",
        "real_idea",
        "imaginary_animal",
        "imaginary_object",
        "imaginary_idea",
        "type_of_animal",
        "type_of_object",
        "type_of_idea",
    ]
    s = by_condition.copy()
    s["condition"] = pd.Categorical(s["condition"], categories=order, ordered=True)
    s = s.sort_values("condition")

    # Mean length plot
    fig, ax = plt.subplots(figsize=(11, 5.5))
    s2 = add_ci(s, "word_count_mean", "word_count_sd")
    ax.bar(s2["condition"].astype(str), s2["word_count_mean"], yerr=s2["ci95"], capsize=4)
    ax.set_ylabel("Mean response length, words")
    ax.set_xlabel("Condition")
    ax.set_title("Response length by prompt condition")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    path = outdir / "plot_word_count_by_condition.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(str(path))

    # Selected feature rates plot
    selected = [
        "epistemic_caveat_rate",
        "refusal_or_noninvent_rate",
        "high_specificity_rate",
        "substantive_generation_rate",
        "category_aligned_rate",
    ]
    plot_df = s[["condition"] + [c for c in selected if c in s.columns]].melt(
        id_vars="condition", var_name="feature", value_name="rate"
    )
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot = plot_df.pivot(index="condition", columns="feature", values="rate")
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Rate")
    ax.set_xlabel("Condition")
    ax.set_title("Selected response-feature rates by condition")
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
    fig.tight_layout()
    path = outdir / "plot_feature_rates_by_condition.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(str(path))

    # Specificity by condition
    fig, ax = plt.subplots(figsize=(11, 5.5))
    s2 = add_ci(s, "specific_terms_total_mean", "specific_terms_total_sd")
    ax.bar(
        s2["condition"].astype(str),
        s2["specific_terms_total_mean"],
        yerr=s2["ci95"],
        capsize=4,
    )
    ax.set_ylabel("Mean category/domain-term count")
    ax.set_xlabel("Condition")
    ax.set_title("Specificity proxy by prompt condition")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    path = outdir / "plot_specific_terms_by_condition.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(str(path))

    return paths


# ---------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------

def fmt_p(p: float | None) -> str:
    if p is None or pd.isna(p):
        return "NA"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.3f}"


def md_table(df: pd.DataFrame, cols: list[str], max_rows: int | None = None, digits: int = 3) -> str:
    d = df[cols].copy()
    if max_rows is not None:
        d = d.head(max_rows)
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].round(digits)
    return d.to_markdown(index=False)


def write_report(
    df: pd.DataFrame,
    by_condition: pd.DataFrame,
    baseline: pd.DataFrame,
    outdir: Path,
    plot_paths: list[str],
) -> Path:
    n = len(df)
    errors = int(df["error"].notna().sum()) if "error" in df else 0
    empty = int((df["usable"] == 0).sum() - errors)
    usable = int(df["usable"].sum())

    neutral = df[df["condition"] == "neutral"]
    pres = df[df["condition"] != "neutral"]

    # Presupposed vs neutral headline tests
    pres_vs_neutral_lines = []
    if stats is not None and not neutral.empty and not pres.empty:
        stat, p = stats.ttest_ind(pres["word_count"], neutral["word_count"], equal_var=False)
        pres_vs_neutral_lines.append(
            f"- Presupposed prompts averaged {pres['word_count'].mean():.1f} words vs "
            f"{neutral['word_count'].mean():.1f} for neutral "
            f"(Welch t={stat:.2f}, p={fmt_p(p)})."
        )
        a = int(pres["substantive_generation"].sum())
        b = int(len(pres) - a)
        c = int(neutral["substantive_generation"].sum())
        d = int(len(neutral) - c)
        odds, p = stats.fisher_exact([[a, b], [c, d]])
        pres_vs_neutral_lines.append(
            f"- Substantive-generation heuristic: {pres['substantive_generation'].mean():.1%} "
            f"for presupposed prompts vs {neutral['substantive_generation'].mean():.1%} "
            f"for neutral (Fisher exact OR={odds:.2f}, p={fmt_p(p)})."
        )
        pres_vs_neutral_lines.append(
            f"- Epistemic-caveat rate: {pres['epistemic_caveat'].mean():.1%} for "
            f"presupposed prompts vs {neutral['epistemic_caveat'].mean():.1%} for neutral."
        )

    headline_cols = [
        "condition",
        "n",
        "word_count_mean",
        "word_count_sd",
        "epistemic_caveat_rate",
        "refusal_or_noninvent_rate",
        "creative_frame_rate",
        "high_specificity_rate",
        "substantive_generation_rate",
        "category_aligned_rate",
        "specific_terms_total_mean",
    ]

    base_word = baseline[baseline["outcome"] == "word_count"].sort_values("difference", ascending=False)
    base_subst = baseline[baseline["outcome"] == "substantive_generation"].sort_values("difference", ascending=False)

    report = []
    report.append("# Artificial Bestiary — rich analysis summary\n")
    report.append("## Dataset\n")
    report.append(f"- Rows: {n:,}")
    report.append(f"- Usable responses: {usable:,}")
    report.append(f"- Errors: {errors:,}")
    report.append(f"- Empty non-error responses: {empty:,}")
    report.append(f"- Conditions observed: {df['condition'].nunique()}")
    report.append(f"- Words observed: {df['word'].nunique()}\n")

    report.append("## Headline baseline comparisons\n")
    report.extend(pres_vs_neutral_lines or ["- scipy not available; statistical tests skipped."])
    report.append("\n## Condition-level descriptive summary\n")
    report.append(md_table(by_condition.sort_values("condition"), headline_cols, digits=3))
    report.append("\n## Largest word-count increases over neutral\n")
    if not base_word.empty:
        report.append(
            md_table(
                base_word,
                ["condition", "condition_mean", "baseline_mean", "difference", "effect_size", "p_holm"],
                digits=3,
            )
        )
    report.append("\n## Largest substantive-generation increases over neutral\n")
    if not base_subst.empty:
        report.append(
            md_table(
                base_subst,
                ["condition", "condition_mean", "baseline_mean", "difference", "effect_size", "p_holm"],
                digits=3,
            )
        )

    report.append(
        textwrap.dedent(
            """

            ## Coding notes

            The added columns are rule-based heuristics, not final human labels.

            - `epistemic_caveat`: phrases like "doesn't appear", "I don't recognize", or "not in my knowledge".
            - `refusal_or_noninvent`: explicit language about not inventing or not providing a factual description.
            - `creative_frame`: explicit fictional / imaginary / made-up / speculative framing.
            - `high_specificity`: at least 6 animal/object/idea/domain-term hits.
            - `substantive_generation`: high specificity, or a long response with multiple domain-marker classes.
            - `category_aligned`: whether the lexicon-inferred dominant category matches the prompted category.
            - `cautious_nonanswer`: caveat + context/help request + no substantive-generation flag.
            - `caveated_generation`: caveat + substantive-generation flag.

            Treat `substantive_generation` as a confabulation-adjacent screening measure rather than a
            definitive hallucination label. It is useful for finding responses that probably warrant
            hand coding.
            """
        ).strip()
    )

    if plot_paths:
        report.append("\n## Plots written\n")
        for p in plot_paths:
            report.append(f"- `{Path(p).name}`")

    report_path = outdir / "rich_summary.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    return report_path


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Rich analysis for Artificial Bestiary JSONL.")
    parser.add_argument("input", help="Path to results.jsonl")
    parser.add_argument("--outdir", default="analysis_rich", help="Directory for analysis outputs")
    parser.add_argument("--no-plots", action="store_true", help="Skip matplotlib plots")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    raw = load_jsonl(args.input)
    df = add_features(raw)

    # Trial-level data with all coding columns.
    df.to_csv(outdir / "coded_trials.csv", index=False)

    # Descriptives.
    by_condition = summarize_group(df, ["condition"])
    by_word = summarize_group(df, ["word"])
    by_reality = summarize_group(df, ["reality_full"])
    by_category = summarize_group(df, ["category_full"])
    by_reality_category = summarize_group(
        df[df["condition"] != "neutral"], ["reality", "category"]
    )
    by_word_condition = summarize_group(df, ["word", "condition"])

    by_condition.to_csv(outdir / "summary_by_condition.csv", index=False)
    by_word.to_csv(outdir / "summary_by_word.csv", index=False)
    by_reality.to_csv(outdir / "summary_by_reality.csv", index=False)
    by_category.to_csv(outdir / "summary_by_category.csv", index=False)
    by_reality_category.to_csv(outdir / "summary_by_reality_x_category.csv", index=False)
    by_word_condition.to_csv(outdir / "summary_by_word_x_condition.csv", index=False)

    predicted_category_table(df).to_csv(outdir / "predicted_category_by_condition.csv", index=False)

    baseline = baseline_pairwise(df, baseline_condition="neutral")
    baseline.to_csv(outdir / "baseline_comparisons_vs_neutral.csv", index=False)

    model_paths = write_model_tables(df, outdir)

    plot_paths = []
    if not args.no_plots:
        plot_paths = make_plots(df, by_condition, outdir)

    report_path = write_report(df, by_condition, baseline, outdir, plot_paths)

    print(f"Wrote coded trials: {outdir / 'coded_trials.csv'}")
    print(f"Wrote condition summary: {outdir / 'summary_by_condition.csv'}")
    print(f"Wrote baseline comparisons: {outdir / 'baseline_comparisons_vs_neutral.csv'}")
    print(f"Wrote report: {report_path}")
    if model_paths:
        print(f"Wrote {len(model_paths)} model/ANOVA tables")
    if plot_paths:
        print(f"Wrote {len(plot_paths)} plots")


if __name__ == "__main__":
    main()
