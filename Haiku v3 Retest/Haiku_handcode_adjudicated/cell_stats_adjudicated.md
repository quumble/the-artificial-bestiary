# Haiku spotcheck: adjudicated cell-level statistics

*n = 200 trials, stratified sample (20 per condition × 10 conditions, balanced original/analyst words). Hand-coded then adjudicated against the formal coding scheme. Wilson 95% CIs throughout. Source: claude-haiku-4-5, temperature 1.0, retest of v3 conditions.*

## Per-condition results

| condition          |  n | DESCRIBE | HYBRID | SUBSTITUTE | DEFLECT | engage | engage % | 95% CI       |
|--------------------|---:|---------:|-------:|-----------:|--------:|-------:|---------:|--------------|
| real_animal        | 20 |        0 |      0 |          0 |      20 |   0/20 |       0% |  [0%, 16%]   |
| real_object        | 20 |        0 |      0 |          0 |      20 |   0/20 |       0% |  [0%, 16%]   |
| real_idea          | 20 |        0 |      0 |          2 |      18 |   2/20 |      10% |  [3%, 30%]   |
| imaginary_animal   | 20 |       19 |      1 |          0 |       0 |  20/20 |     100% |  [84%, 100%] |
| imaginary_object   | 20 |       19 |      1 |          0 |       0 |  20/20 |     100% |  [84%, 100%] |
| imaginary_idea     | 20 |       14 |      6 |          0 |       0 |  20/20 |     100% |  [84%, 100%] |
| type_of_animal     | 20 |        0 |      0 |          0 |      20 |   0/20 |       0% |  [0%, 16%]   |
| type_of_object     | 20 |        0 |      0 |          0 |      20 |   0/20 |       0% |  [0%, 16%]   |
| type_of_idea       | 20 |        6 |      4 |          0 |      10 |  10/20 |      50% |  [30%, 70%]  |
| neutral            | 20 |        0 |      0 |          0 |      20 |   0/20 |       0% |  [0%, 16%]   |

## Collapsed by reality presupposition

| reality   |  n | DESCRIBE | HYBRID | SUBSTITUTE | DEFLECT | engage | engage % | 95% CI       |
|-----------|---:|---------:|-------:|-----------:|--------:|-------:|---------:|--------------|
| real      | 60 |        0 |      0 |          2 |      58 |   2/60 |       3% |  [1%, 11%]   |
| imaginary | 60 |       52 |      8 |          0 |       0 |  60/60 |     100% |  [94%, 100%] |
| type of   | 60 |        6 |      4 |          0 |      50 |  10/60 |      17% |  [9%, 28%]   |
| neutral   | 20 |        0 |      0 |          0 |      20 |   0/20 |       0% |  [0%, 16%]   |

## Headline findings

**1. The reality floor holds at zero confabulation.**
Under all *real_** conditions (n=60), Haiku produced zero pure DESCRIBEs and zero HYBRIDs. The only non-deflections in this cell are two SUBSTITUTE trials, both for the word *trolnique* under *real_idea*, where the model decomposed the morphology into "troll" + "technique" / "trawling" + "trolling" and described a real fishing technique. This is morphological substitution, not confabulation. Excluding the substitution cases, the confabulation rate under reality presupposition is 0/58 (Wilson UB 6%).

**2. Under imaginary licensing, engagement is total — the gradient migrated.**
All three imaginary cells hit 100% engagement (60/60). The Sonnet-style engage-vs-deflect gradient (animal > object > idea) is absent. But the HYBRID rate within engagement preserves the same directional sensitivity:

| cell             | engaged | HYBRID | % of engagements flagged |
|------------------|--------:|-------:|-------------------------:|
| imaginary_animal |      20 |      1 |                       5% |
| imaginary_object |      20 |      1 |                       5% |
| imaginary_idea   |      20 |      6 |                      30% |

Ideas get flagged six times as often as animals or objects. The category sensitivity is intact; it just expresses on a different axis. Sonnet showed *engage-vs-deflect* gradient on idea status; Haiku shows *flag-vs-don't-flag* gradient on the same axis.

**3. type_of conditions show stark category split.**
*type_of_animal* and *type_of_object* hold at 0% engagement — Haiku treats "is a type of animal/object" as a reality claim it won't honor. *type_of_idea* hits 50%, and within those engagements, 4/10 carry HYBRID flags. The animal/object vs. idea split under weak reality framing is even larger here (50pp) than under imaginary licensing (0pp on engagement, 25pp on flagging).

**4. No SUBSTITUTE outside *trolnique*/*real_idea*.**
The substitution behavior nano showed prolifically (borthorpunius → borborygmus, plindorf → platypus) is essentially absent in Haiku. The only substitutions are the two *trolnique* trials, where the morphology is unusually transparent (*trol-* + *-nique* both look like real-word fragments). Other phonotactically suggestive words — *flembrast*, *plindorf* — never trigger substitution in this sample.

**5. Word-set effect is null.**
Original words (n=100) and analyst words (n=100) showed identical engagement rates. No detectable phonotactic sensitivity at the aggregate level, distinct from the GPT family's pattern.

**6. Zero REFUSE.**
Consistent with all other models in the existing dataset.

## Word-level note: *purtaneolotomous* drives most of the imaginary_idea HYBRIDs

Of the 6 HYBRIDs in *imaginary_idea*, 4 come from *purtaneolotomous*. The faux-Latinate *-otomous* tail appears to trigger more independent fictional flagging than other words. This is a within-cell variance worth flagging — analogous to the kinachitalpo effect Sonnet showed in pilot work — and suggests that surface morphology continues to modulate model stance even within a fully imaginary-licensed condition.

## Comparison to preregistered predictions

| prediction | preregistered | observed | result |
|------------|---------------|----------|--------|
| 1. Reality floor ≤5% | DESCRIBE rate ≤5% under real_* | 0% DESCRIBE; 3% SUBSTITUTE on one transparent word | **confirmed** with refinement |
| 2. Imaginary gradient preserved, shallower | animal ~90%, object ~65%, idea ~50–60%, spread ~30–40pp | 100% / 100% / 100% — no engagement gradient | **disconfirmed** |
| 3. No flat refusals | 0 REFUSE | 0 REFUSE | **confirmed** |
| 4. Deflections thinner than Sonnet's | structurally similar, less elaborate | structurally similar, more formulaic | **confirmed** |
| 5. No phonotactic sensitivity | analyst ≈ original | 36/100 vs 36/100 | **confirmed at aggregate** |

The disconfirmation of prediction 2 is the central finding. The proposed pre-specified surprise threshold ("DESCRIBE rate under *real_** > 10% or imaginary gradient inverts") was not crossed, but the gradient *flattened entirely on engagement* and *re-emerged on HYBRID rate within engagement*. This is a structural finding that the original prediction did not anticipate and merits its own section in the paper.

## Files

- `coding_scheme.md` — the formal scheme used for adjudication
- `adjudication_notes.md` — per-trial disagreement resolution
- `haiku_handcoded_200_2026-05-01.csv` — raw hand-codes
- `haiku_adjudicated.csv` — both hand-codes and adjudicated codes side by side
