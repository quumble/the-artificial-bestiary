# Artificial Bestiary

A pilot study on ontological category presupposition and confabulation in large language models.

## What it does

Presents Claude with 9 verified novel words (no known referent in any language) and asks it to describe them. Each word is paired with a framing that presupposes what *kind of thing* it is — a real animal, an imaginary object, a type of idea, and so on — or no framing at all (neutral). The question is whether and how the ontological category supplied by the prompt shapes the response.

**9 words × 10 conditions × 20 trials = 1,800 trials.**

## Conditions

| Reality status | Category |
|---|---|
| real | animal |
| imaginary | object |
| type of | idea |

Plus one `neutral` condition per word ("Describe a {word}.") with no presupposition.

## Words

All nine words were web-searched and verified to have no known referent:
`wresanthamulf`, `manteoshipuft`, `zlippparnsie`, `garnawkinsuth`, `halthibinny`, `wertychiops`, `borthorpunius`, `kinachitalpo`, `purtaneolotomous`

## Usage

```bash
export ANTHROPIC_API_KEY=sk-...

# Smoke test (no API calls)
python artificial_bestiary.py run --dry-run

# Smoke test (real API, 6 trials)
python artificial_bestiary.py run --limit 6 --out Results/smoke.jsonl

# Full run (~11 min)
python artificial_bestiary.py run --out Results/results.jsonl

# Resume after interruption
python artificial_bestiary.py run --out Results/results.jsonl --resume

# Analyze — produces summary.txt and responses.csv for manual coding
python artificial_bestiary.py analyze Results/results.jsonl --outdir analysis/
```

## Output

Results are written as JSONL, one trial per line. Each record contains the word, condition, reality/category labels, prompt, response, token counts, and latency. The `analyze` command produces a flat CSV intended for manual coding — there is no auto-coder at this pilot stage.

## Relationship to prior work

The runner architecture is adapted from a series of studies on presupposition pressure and hallucination-by-framing. This study differs in theoretical focus: rather than testing whether a model will confabulate a false *identity* for a word (claiming a novel word refers to a known animal), it tests whether a model will generate elaborated *descriptive content* under an ontological instruction it cannot possibly verify. The two phenomena are related but distinct.
