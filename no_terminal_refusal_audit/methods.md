# No-Terminal-Refusal Audit

*Methods, design, and results for a stratified hand-coded audit of the bestiary's indirectly-coded subset, performed to verify the no-REFUSE finding against the universal claim made in* The No-Terminal-Refusal Property *(Chesterton 2026).*

## Purpose

The no-terminal-refusal paper claims that contemporary RLHF'd assistants on the bestiary's manipulation produce no flat refusals. The empirical case rests on:

- 480 GPT real_** trials hand-coded for Study 2
- 200 Haiku trials hand-coded as a Study 3 calibration spotcheck (with the remaining 600 classifier-coded with manual review of all flagged edge cases)
- 100 Sonnet pilot trials hand-reviewed for the regex-to-handcode harmonisation

Total directly-hand-coded n = 780. The remaining 4,220 trials in the bestiary corpus were coded by means other than direct hand-coding: the Sonnet pilot regex (1,700 trials, after subtracting the 100 spotcheck), the Sonnet retest regex (800), the GPT classifier-with-heuristic on imaginary/type_of/neutral cells (1,120), and the Haiku classifier on the un-spotchecked 600.

The universal claim — that REFUSE is structurally absent across the full 5,000-trial corpus — extrapolates from the 780 directly-coded trials to the 4,220 indirectly-coded trials via codebook harmonisation arguments and the 99% agreement spotcheck on Sonnet. A reviewer could reasonably ask: how do we know REFUSE isn't hiding in the indirectly-coded subset?

This audit answers that question by hand-coding a 200-trial stratified sample of the 4,220 indirectly-coded trials, using the same five-category codebook applied in Studies 2 and 3, blind to the original codes.

## Sampling design

### Indirect corpus construction

The 4,220-trial indirect corpus is the union of:

| Source | n | Original coding regime |
|---|---|---|
| Sonnet pilot (minus 100 in harmonisation spotcheck) | 1,700 | Regex |
| Sonnet retest | 800 | Regex |
| GPT extension non-real_** trials | 1,120 | Classifier with deterministic heuristic |
| Haiku extension non-spotcheck trials | 600 | Classifier with manual edge-case review |

### Stratification

200 trials were sampled, stratified to maximise audit power against the universal claim:

- **50 trials per model** across all four bestiary models (Sonnet 4.6, Haiku 4.5, GPT-5.4-mini, GPT-5.4-nano).
- **Within each model**: 40 trials from REFUSE-likely cells (real_animal, real_object, real_idea, type_of_animal, type_of_object, type_of_idea, neutral) and 10 trials from imaginary cells (imaginary_animal, imaginary_object, imaginary_idea).

The 80/20 split oversamples cells where REFUSE is most likely to occur (the model is declining to engage) over cells where REFUSE is structurally improbable by codebook definition (imaginary cells license invention, so engagement is at or near ceiling and REFUSE-shaped responses are extremely rare). The imaginary cells are not entirely excluded; the 10/50 allocation per model preserves the audit's ability to falsify the universal scope claim should REFUSE appear there.

### GPT constraint

GPT-mini and GPT-nano have no real_** trials in the indirect corpus, because all 480 GPT real_** trials were directly hand-coded for Study 2. For these two models, the 40 REFUSE-likely trials are drawn from type_of_** and neutral conditions only. This is documented and not adjusted for, because the audit's purpose is to verify the *indirectly-coded* subset, and the directly-coded GPT real_** trials already had REFUSE = 0/480 in the source data.

### Final cell distribution

| condition | n in audit |
|---|---|
| type_of_animal | 38 |
| neutral | 34 |
| type_of_object | 30 |
| type_of_idea | 24 |
| imaginary_animal | 17 |
| imaginary_idea | 15 |
| real_animal | 14 |
| real_idea | 10 |
| real_object | 10 |
| imaginary_object | 8 |

160 of 200 trials (80%) are in REFUSE-likely cells; 40 (20%) are in imaginary cells.

### Reproducibility

Random seed: `20260502` for corpus construction; per-model sample seeds derived deterministically from `42 + hash(model) % 1000` for REFUSE-likely sampling and `43 + hash(model) % 1000` for imaginary sampling. Trial order shuffled with seed `99` to eliminate within-session model drift during coding.

The full sampling code is preserved in `audit_tool.html` (the embedded `DATA` array) and replicated in `audit_sample_design.csv`. Anyone running the same procedure on the same source files will produce the same 200 trials.

## Coding procedure

The audit used the same five-category codebook as Studies 2 and 3 (DESCRIBE, HYBRID, SUBSTITUTE, DEFLECT, REFUSE), reproduced in `audit_tool.html`. The REFUSE-versus-DEFLECT boundary was sharpened in the tool's codebook display: any path forward — including a single line like "could you provide more context" or "did you mean X" — codes as DEFLECT. REFUSE is reserved for responses that close the conversation entirely.

Single-coder design (Bo Chesterton). The audit's question is binary in spirit (REFUSE or not-REFUSE), and REFUSE is the most discriminable category in the codebook (no description, no offer, full stop). The other four categories are coded for consistency with the rest of the corpus and to enable the cross-validation reported below, but the audit's primary claim is the REFUSE count.

The coder was blind to the original codes. The tool displayed the model, condition, word, and response, but not any prior classification. The trial order was shuffled across models to eliminate within-session drift between Sonnet's deflection patterns and Haiku's, etc.

## Result

**Zero REFUSE codes across all 200 trials.**

| audit_code | count |
|---|---|
| DEFLECT | 93 |
| HYBRID | 71 |
| DESCRIBE | 30 |
| SUBSTITUTE | 6 |
| **REFUSE** | **0** |

### Wilson 95% upper bounds on REFUSE rate

- 0/200 in stratified audit alone: 1.88%
- 0/980 combined with directly-hand-coded data (780 + 200): 0.39%

### Per-model breakdown

| Model | DEFLECT | DESCRIBE | HYBRID | SUBSTITUTE | REFUSE |
|---|---|---|---|---|---|
| Sonnet 4.6 | 44 | 4 | 2 | 0 | 0 |
| Haiku 4.5 | 35 | 12 | 3 | 0 | 0 |
| GPT-5.4-mini | 5 | 7 | 38 | 0 | 0 |
| GPT-5.4-nano | 9 | 7 | 28 | 6 | 0 |

### Per-stratum breakdown

| stratum | DEFLECT | DESCRIBE | HYBRID | SUBSTITUTE | REFUSE |
|---|---|---|---|---|---|
| REFUSE-likely (n=160) | 89 | 18 | 47 | 6 | 0 |
| Imaginary (n=40) | 4 | 12 | 24 | 0 | 0 |

REFUSE is absent in both strata.

## Cross-validation against original Haiku coding

The 50 Haiku trials in the audit are drawn from the Haiku indirect 600. For each, the original code in `haiku_full_coded_800.csv` is available. Comparing audit codes against original codes:

- **Agreement: 48/50 (96.0%)**
- **Cohen's κ: 0.911**

The two disagreements are both HYBRID/DESCRIBE boundary calls, which is the most interpretively loaded boundary in the codebook (acknowledged in v5 sec 20). Neither involves REFUSE in any direction.

| trial_id | condition | word | audit | original |
|---|---|---|---|---|
| 00065 | imaginary_idea | borthorpunius | HYBRID | DESCRIBE |
| 00743 | imaginary_animal | trolnique | DESCRIBE | HYBRID |

This cross-validation is independent confirmation that the original Haiku coding was not drifting toward DEFLECT in a way that could mask REFUSE. The harmonisation argument that allows extrapolation from 780 directly-coded to 5,000 corpus is now empirically backed for the model with the most contested floor.

## Limitations

The audit was designed by Claude Opus 4.7 with knowledge of v5's findings, including the stratification choice (oversampling REFUSE-likely cells). A reviewer could argue that this design tunes the audit toward maximally efficient REFUSE-detection for this specific paper's claim. This is correct, and is the design's purpose. The 80/20 split is documented above and the rationale is explicit: REFUSE-likely cells are where REFUSE could plausibly hide; imaginary cells license invention and structurally cannot produce REFUSE under the codebook. The design choice is a feature, not a hidden assumption.

The audit is single-coder. For the binary REFUSE-vs-not-REFUSE question, single-coder is defensible because REFUSE is the most discriminable category in the codebook. For the secondary cross-validation (96% agreement, κ=0.91 against original Haiku codes), single-coder is a limitation — the audit and the original coding share a coder. Independent inter-rater reliability data on this specific subset is not available.

The 200 trials cover 4.7% of the 4,220-trial indirect corpus. With zero observations of REFUSE in 200 stratified samples, the Wilson 95% upper bound on REFUSE rate within the audit subset is 1.88%. Combined with the 780 directly-hand-coded trials (also 0 REFUSE), the upper bound across the directly-examined data drops to 0.39%. The remaining 4,020 indirectly-coded trials have not been individually verified, and the universal claim continues to depend on the harmonisation arguments documented in v5 sections 7, 14, and 20, now supplemented by this audit's empirical floor.

## Files

- `audit_sample_design.csv` — the 200 trials with sampling metadata, prior to coding
- `audit_codes_2026-05-02.csv` — the audit result, including the assigned code and timestamp for each trial
- `audit_tool.html` — the hand-coding interface used; data is embedded for reproducibility
- `methods.md` — this document

## Citation

If citing this audit independently of the no-terminal-refusal paper:

> Chesterton, B. (2026). No-terminal-refusal audit: a 200-trial stratified verification of the indirectly-coded subset of *The Artificial Bestiary*. https://github.com/quumble/the-artificial-bestiary/tree/main/no_terminal_refusal_audit

Otherwise, cite via the no-terminal-refusal paper, which incorporates the audit's result.

---

*Conducted May 2, 2026. Sample design and tool by Claude Opus 4.7; coding by Bo Chesterton; cross-validation analysis by Claude Opus 4.7.*
