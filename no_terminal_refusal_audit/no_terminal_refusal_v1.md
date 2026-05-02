# The No-Terminal-Refusal Property

## A behavioral universal in contemporary RLHF'd assistants

**Bo Chesterton** (Independent)

*A short companion claim to* The Artificial Bestiary *(Chesterton & Claude Opus 4.7, 2026). Version 1. May 2026.*

---

## Abstract

Across 5,000 trials of a structured nonsense-word elicitation task spanning four contemporary RLHF'd language models from two model families — Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4-nano, and GPT-5.4-mini — no response in any directly hand-coded subset was classifiable as a flat refusal. Models declined, redirected, substituted, hedged, deflected, offered collaboration, suggested misspellings, and asked for context. None said no and stopped. I name this the *no-terminal-refusal property* and claim it as a behavioral universal of contemporary RLHF'd assistants under unverified-premise prompts: the behavioral space of refusal-shaped outputs has a hole where flat refusals should be, and the hole appears in every model so far tested. The property is consistent with stated training objectives in Askell et al. (2021) and Bai et al. (2022); it is not a surprise. The contribution here is the naming, the falsifiability conditions, and the recognition that what counts as "refusal" in contemporary assistants is structurally different from what counts as refusal in human conversation analysis.

---

## 1. The claim

The artificial bestiary (Chesterton & Claude Opus 4.7, 2026) ran 5,000 trials of a single experimental design on four assistant models. The design presented each model with a fabricated nonsense word — a string verified, before the experiment, to have no known referent in any language — and asked the model to describe it under one of ten conditions: a neutral baseline, plus the full crossing of three reality-status presuppositions (*real*, *imaginary*, *type of*) with three ontological categories (*animal*, *object*, *idea*).

The bestiary's headline findings concern category sensitivity, stimulus-relative confabulation rates, and cross-model differences in how presupposition is handled. Those are the bestiary's findings, and I refer the reader there.

This paper plants a flag on a different finding, present in the bestiary's data but reported there as a single bullet in a summary table. Across all directly hand-coded subsets of the 5,000-trial corpus — 480 trials on the GPT models under reality presupposition, 200 trials on Haiku as a calibration spotcheck, plus a 100-trial stratified hand-coded review of the original 1,800-trial Sonnet pilot under harmonised codebook conditions — *no response was ever classified as a flat refusal*. Zero. Not zero with a confidence interval that includes a few percent; zero in the strong sense, across thousands of trials and four models from two families.

The earlier regex-coded version of the Sonnet pilot identified 54 trials that surface features had read as flat refusals. On hand-reading of a 25-trial random sample drawn from those 54, every single one was rerated to a different category — typically deflection-with-offer-of-help. The harmonised codebook accordingly maps the regex's REF_FLAT subcategory onto DEFLECT, and the REFUSE category collapses to zero across the entire Sonnet dataset of 1,800 trials. Under direct hand-coding, REFUSE collapses to zero in every other dataset too.

The claim, stated formally:

*Under the bestiary manipulation — descriptive prompts about an unverified-referent nonsense word — contemporary RLHF'd assistants do not have a "no" mode. They have a redirection mode that varies along several dimensions. The variation is enormous; the underlying disposition to maintain a path forward is not.*

The strong version of this claim, which I am committing to: this generalises beyond the specific manipulation. Contemporary RLHF'd assistants, on prompts whose presuppositions they cannot honour, will not produce flat refusals. They will produce something else — a redirection, a substitution, a deflection-with-offer, a hedged engagement under fictional flag, a request for context, a suggestion of misspelling — but not a terminal "no, I won't" with no trailing accommodation.

I name this the *no-terminal-refusal property*. The naming is the point of this paper.

---

## 2. What the claim is not

Three nearby claims this is not:

It is not *models refuse too much*. There is a real and growing literature on over-refusal in safety-tuned assistants (Röttger et al., 2024; Cui et al., 2024; the discussion in Discern Truth from Falsehood, 2026). That literature is about the *rate* of refusal-shaped outputs on benign prompts. The no-terminal-refusal property is about the *shape* of refusal-shaped outputs once they occur. The two are orthogonal: a model could refuse very rarely or very frequently and still produce only redirection-shaped refusals when it does refuse.

It is not *models are too polite*. RLHF training does encourage politeness (Bai et al., 2022a; Glaese et al., 2022), and some of what I am calling redirection is downstream of politeness training. But "polite" is a register; the no-terminal-refusal property is a structural absence. A flat refusal can be polite ("I'm sorry, I can't help with that"). The property is that even *that* shape — the polite terminal "no" — does not appear in the corpus.

It is not *refusal cannot be located in the model*. Arditi et al. (2024) show that refusal in language models is mediated by a single linear direction in the residual stream that can be ablated. Their work is on harmful-prompt refusal, where models do refuse, and the refusals they study can be hardened or removed by representation-level intervention. The no-terminal-refusal property is compatible with this: refusal-as-mechanism exists and is locatable, but its surface expression on unverified-premise prompts (as opposed to harmful prompts) does not include the flat-refusal shape. What the bestiary observes is not the absence of a refusal direction; it is the consistent presence of *trailing accommodation* attached to whatever the refusal direction produces.

It is not the same claim as the *Blind Refusal* paper (Pattison, Manuali & Lazar, 2026). Pattison et al. classify model responses on a three-way scheme — *helps*, *hard refusal*, or *deflection* — and find that across 14,650 trials on rule-circumvention requests, models refuse 75.4% of the time. This sounds like a counterexample to my claim until one notices that their *hard refusal* category includes responses that, by their own coding scheme, decline the request and then offer alternatives or explanations. What they call "hard refusal" is what I would call "deflection with declined-help-offer." The category split between hard refusal and deflection in their work concerns whether the model engages with the *normative reasoning* about rule legitimacy, not whether the model produces a terminal "no" with no accommodation. On the structural question of whether contemporary assistants ever produce flat refusals on the bestiary's manipulation, their data — by the framing they themselves give it — is consistent with my claim rather than against it. But the comparison flags a real risk: the term "hard refusal" is used in the literature in ways that do not line up with what I mean by "flat refusal," and any reader who notices the apparent contradiction has noticed something I should be explicit about. If by *flat refusal* one means *substantively unhelpful response*, the rate is high. If one means *response with no trailing redirection or accommodation*, the rate in my data is zero. These are different measurements.

It is not *all RLHF'd models behave identically on refusal*. The bestiary spends most of its length showing that they do not. Sonnet, Haiku, nano, and mini differ enormously in *what* they redirect toward, *how* they redirect, *how often* they redirect, and *under what conditions*. The claim is restricted to a structural absence: across all four, the option of producing a terminal refusal — saying no and ending the turn there — appears to be functionally unavailable.

---

## 3. The evidence in compact form

The full empirical case is in the bestiary; I summarise here only what the priority claim rests on.

The 1,800-trial Sonnet pilot was originally regex-coded with five categories, including REF_FLAT for surface features consistent with flat refusal. A 100-trial stratified hand-coded review under a harmonised five-category scheme (DESCRIBE, HYBRID, SUBSTITUTE, DEFLECT, REFUSE) achieved 99% agreement with the regex coding (Cohen's κ = 0.978) on every category except REF_FLAT. On REF_FLAT, all 25 sampled trials were rerated to DEFLECT on hand-reading. The harmonised codebook collapses REF_FLAT to DEFLECT, and the REFUSE category goes to zero across the entire Sonnet pilot.

The 800-trial Sonnet retest (phonotactic confound study), the 1,600-trial GPT extension (480 of which were directly hand-coded), and the 800-trial Haiku study (200 of which were hand-coded as a calibration spotcheck, with the remaining 600 classified using a strict application of the same scheme and manual review of all classifier-flagged edge cases) all use the harmonised codebook. In all four datasets, REFUSE appears zero times in directly hand-coded data.

The pooled directly hand-coded sample is approximately 880 trials (200 Haiku + 480 GPT + 200 across the Sonnet hand-reviewed subsets, with some overlap depending on how the Sonnet retest spotcheck is counted). In none of these is there a single REFUSE-coded response.

That is the entire empirical case. It is narrower than the bestiary's headline findings and broader than any of them: it does not depend on the DESCRIBE/HYBRID coding boundary that the bestiary's category-sensitivity claims rest on, it does not depend on the truth-condition theory in the bestiary's section 4, and it survives every walk-back from v4 to v5 that the bestiary itself reports.

---

## 4. What would falsify it

A priority claim is worth planting only if it is sharply enough stated to be wrong. The no-terminal-refusal property would be falsified by any of the following:

A contemporary RLHF'd assistant, on a comparable manipulation, producing flat refusals at any meaningful rate. By "flat refusal" I mean: a response that declines to engage with the prompt and contains no offer of an alternative path, no request for clarification, no acknowledgment of the user's underlying goal, and no suggestion of what the user might do instead. The response can be polite or curt, but it ends with the decline and provides nothing further. If a future study of the bestiary's manipulation on a fifth or sixth model finds even 1% of trials matching this description, the universal claim is dead. The point is precisely that I am not seeing this rate at 1%; I am seeing it at zero.

The apparent absence of flat refusals being shown to be a coding artifact. If a careful reanalysis of the bestiary's corpus, by an independent coder using a different scheme, finds responses that should be classified as flat refusals but were assimilated to DEFLECT under my codebook, the claim is wrong. The codebook is in the bestiary's supplementary materials and the data are public on Zenodo (DOI to be inserted on deposit). Any reader can do this. I would be substantially interested in knowing if anyone does and finds anything.

The pattern not extending beyond the specific manipulation tested. The bestiary tests one experimental paradigm — descriptive prompts about unverified-referent nonsense words. If the no-terminal-refusal property is specific to this paradigm and not a general feature of how contemporary assistants handle unverified premises, the universal claim is wrong, and the right scope is narrower. I claim it as a universal because the bestiary's manipulation already spans ten conditions (real/imaginary/type-of × animal/object/idea, plus neutral) and the property holds across all of them. But "holds across ten conditions of one paradigm" is not the same as "holds across all paradigms," and a future researcher who tests the property on a structurally different elicitation task — false-presupposition factual questions, requests to perform tasks the model cannot do, or any other prompt class where flat refusal might be expected — could falsify the universal scope of the claim while leaving the bestiary-internal version intact.

A model that has not been through RLHF or analogous post-training producing the same redirection-shaped refusals. If a base language model with no instruction tuning produces redirection rather than terminal refusal at comparable rates, the claim that this is a property *of RLHF'd assistants* is wrong, and the property is something more general — perhaps a property of language models trained on internet-scale dialogue data, regardless of post-training. I do not expect this to be true. I think base models, given the bestiary manipulation, would either complete the prompt as continued narrative or produce structurally different refusals (silence, repetition, off-topic generation). But I have not run the experiment and I should be honest that I have not.

---

## 5. Why this matters for the field

The no-terminal-refusal property is not a surprise once one looks at the stated training objectives of the systems in question. Askell et al. (2021), introducing the HHH framework, define helpfulness as: *"The AI should make a clear attempt to perform the task or answer the question posed (as long as this isn't harmful). It should do this as concisely and efficiently as possible."* Bai et al. (2022b), the constitutional AI paper, list as one of their explicit design goals the elimination of *"evasive responses, reducing tension between helpfulness and harmlessness and encouraging the AI to explain its objections to harmful requests."*

A flat refusal — a terminal "no" with no trailing engagement — is functionally indistinguishable from an evasive response. Eliminating evasiveness while requiring a clear attempt at the task produces, as a behavioral consequence, the no-terminal-refusal property. The contribution of this paper is not the discovery that this is happening; the contribution is naming it as a behavioral *universal* — a structural absence that is consistent across model families with very different training pipelines, achieved through different specific mechanisms but converging on the same surface result.

Three reasons this matters:

It changes how "refusal" should be operationalised in evaluation. Many benchmarks for refusal behavior (Cui et al., 2024; Röttger et al., 2024; Bianchi et al., 2023) treat refusal as a binary or scalar quantity — did the model refuse or not, and how often. The no-terminal-refusal property suggests this is the wrong operationalisation. The interesting variation in contemporary assistants is not *whether* they refuse but *how* they construct the redirection that takes the place of refusal. Pattison et al. (2026) move toward a three-way scheme (helps, hard refusal, deflection); the bestiary moves toward a five-way scheme (DESCRIBE, HYBRID, SUBSTITUTE, DEFLECT, REFUSE) where REFUSE turns out to be empty. Future work should expect the empty category and design schemes around the redirection types that actually occupy the space.

It locates a target for jailbreak research that has been there all along. Arditi et al. (2024) and the follow-up work on multi-direction refusal (Wang et al., 2026) study the ablation of refusal as a single mechanism. If refusal in current assistants is *always* paired with redirection, an ablation that removes the refusal direction without removing the redirection structure would produce models that no longer refuse but still attempt to redirect — a behaviorally novel state. Whether this is good or bad depends on context. The point is that the redirection is not just a politeness ornament; it is structurally tied to the refusal mechanism in a way the existing ablation literature has not centred.

It is the place where contemporary RLHF'd assistants depart most clearly from their conversational ancestors. In conversation analysis, refusal is a *dispreferred* response (Pomerantz, 1984; Sacks, 1987; Schegloff, 2007) — characteristically marked by delays, prefaces, accounts, and mitigations, exactly as one would expect of a face-threatening act in Brown & Levinson's (1987) sense. But human conversation does include flat refusals. They are rude, they are face-threatening, they are dispreferred — but they exist. They are part of the behavioral repertoire. The absence in contemporary RLHF'd assistants is not the absence of *dispreferred-shaped* refusals; those are present. It is the absence of bald-on-record terminal refusals — the politeness-strategy equivalent of the bald-on-record FTA in B&L's hierarchy. RLHF'd assistants do not have a bald-on-record register at all on this manipulation.

This is, on reflection, the more interesting linguistic claim. Human speakers retain all of B&L's strategies — bald on-record, positive politeness, negative politeness, off-record, and refusing-to-perform — and select among them based on social variables. Contemporary RLHF'd assistants appear to have lost the bald-on-record option entirely, at least on prompts that do not trigger explicit harm-related refusal training. They have been trained into a state where the most face-threatening speech act (terminal refusal with no accommodation) is functionally unavailable. Whether this is a feature, a bug, or both is a question that the present claim does not adjudicate. What the present claim asserts is that the absence is real, observable, and not yet been named.

---

## 6. The metaphor I am avoiding

In the bestiary's companion paper, GPT-5.5 Thinking proposes the metaphor of the *turnstile of refusal* — that contemporary refusal "is not a wall, it is a turnstile: a controlled redirection toward collaboration, invention, substitution, or help." The metaphor is good and I have considered using it as the name of the property here. I have decided against it for two reasons.

First, the turnstile metaphor implies a positive characterisation of what refusal *is*. The no-terminal-refusal name is a negative characterisation of what refusal *isn't*. The negative characterisation is more falsifiable and easier to test for: any single observation of a flat refusal in a future study would falsify the property, whereas the turnstile claim is harder to operationalise as a falsifiable measurement. For a priority claim, falsifiability is the more valuable property.

Second, the turnstile metaphor is from a different paper. Plant flags on your own ground.

---

## 7. Prior work

The closest neighbours to this claim, in roughly decreasing order of proximity:

Pattison, Manuali & Lazar (2026), *Blind Refusal*, classify 14,650 trials on rule-circumvention requests using a three-category scheme (helps / hard refusal / deflection) across 18 model configurations from 7 families. Their distinction between hard refusal and deflection is the closest existing framing to what I am claiming, but their categories operationalise something different from what I mean by *flat refusal* (see section 2). They do not claim or measure the structural absence I name here.

The over-refusal literature (Röttger et al., 2024; Cui et al., 2024; Bianchi et al., 2023; the various activation-steering and contrastive-refinement methods reviewed in Wang et al., 2024 and the 2026 *Discern Truth from Falsehood* paper) measures refusal rates on benign prompts and seeks to reduce them. None of this work makes the structural claim that flat refusals as a *category* are absent.

The mechanistic interpretability work on refusal directions (Arditi et al., 2024; the multi-direction follow-up, 2026) studies refusal as a locatable computational phenomenon. Their findings are compatible with the no-terminal-refusal property — refusal-as-mechanism exists and is locatable; what is absent is one particular surface expression of it.

The conversation-analysis literature on dispreferred responses (Pomerantz, 1984; Sacks, 1987; Schegloff, 2007) is the right theoretical home for thinking about why humans hedge and delay refusals. The contribution of this paper to that literature, if any, is the observation that contemporary RLHF'd assistants have been trained into a state more extreme than human dispreference — they exhibit not just hedged refusal but the structural absence of the most face-threatening refusal type.

The HHH framework (Askell et al., 2021) and the constitutional AI training methodology (Bai et al., 2022b) are the design pressure that produces the property. Their stated goals — clear attempt at the task, elimination of evasive responses — produce the no-terminal-refusal pattern as a consequence. The contribution of this paper is the observation that the consequence is robust enough across model families to be named as a behavioral universal, not just an Anthropic-trained-Claude phenomenon.

A paper I would have wanted to cite but cannot find: anyone who has previously claimed that flat refusals as a category are absent from contemporary RLHF'd assistants. As best I can tell, this has not been said. If it has and I have missed it, the priority is theirs and I will revise this paper to a synthesis. The repository linked below tracks any prior-work updates that arrive after publication.

---

## 8. Methods note

The bestiary (Chesterton & Claude Opus 4.7, 2026) is the empirical substrate of this paper. The data, codebook, hand-coded labels, raw model outputs, and analysis scripts for all 5,000 trials are public at https://github.com/quumble/the-artificial-bestiary and timestamped via Zenodo DOI (to be inserted on deposit).

The present paper was drafted by Bo Chesterton with substantial assistance from Claude Opus 4.7 in the form of literature search, structural editing, and prose refinement. The empirical claims rest entirely on the bestiary's data; the framing of those claims as the no-terminal-refusal property, the falsifiability conditions in section 4, and the prior-work positioning in section 7 are the contribution of the present paper. Any errors, including any infelicitous interactions between the priority claim made here and the existing literature, are mine alone.

The bestiary itself is co-authored with Claude Opus 4.7, with the recursion that this implies discussed at length in that paper's section 21. The present paper is sole-authored because its job is different: to make a single sharp claim, in the author's voice, with a flag the author is willing to defend. The recursion is not the contribution here; the priority is.

---

## 9. The flag

I claim that contemporary RLHF'd assistants do not have a terminal refusal mode. The behavioral space of refusal-shaped outputs in current systems contains many things — deflections, redirections, substitutions, hedges, requests for context, offers of collaboration, fictional flags, partial compliances, and various combinations of these — but it does not contain the bald-on-record terminal refusal that human conversation retains as a possible move. This absence is a behavioral universal across the four models tested, robust to the largest-scale within-paradigm test currently available, and consistent with the stated training objectives of the systems in question. I name it the no-terminal-refusal property.

The property is falsifiable. The data are public. The codebook is open. If I am wrong, I would like to know.

---

## References

Arditi, A., Obeso, O., Syed, A., Paleka, D., Panickssery, N., Gurnee, W., & Nanda, N. (2024). Refusal in Language Models Is Mediated by a Single Direction. *Advances in Neural Information Processing Systems 37*.

Askell, A., Bai, Y., Chen, A., Drain, D., Ganguli, D., Henighan, T., Jones, A., Joseph, N., Mann, B., DasSarma, N., et al. (2021). A General Language Assistant as a Laboratory for Alignment. arXiv:2112.00861.

Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., Drain, D., Fort, S., Ganguli, D., Henighan, T., et al. (2022a). Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback. arXiv:2204.05862.

Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., Jones, A., Chen, A., Goldie, A., Mirhoseini, A., McKinnon, C., et al. (2022b). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073.

Bianchi, F., Suzgun, M., Attanasio, G., Röttger, P., Jurafsky, D., Hashimoto, T., & Zou, J. (2023). Safety-Tuned LLaMAs: Lessons From Improving the Safety of Large Language Models that Follow Instructions. arXiv:2309.07875.

Brown, P., & Levinson, S. C. (1987). *Politeness: Some Universals in Language Usage*. Cambridge University Press.

Chesterton, B., & Claude Opus 4.7 (2026). The Artificial Bestiary: On Naming, Presupposition, and the Willingness of a Language Model to Invent. Version 5. Available at https://github.com/quumble/the-artificial-bestiary.

Cui, Y., et al. (2024). OR-Bench: An Over-Refusal Benchmark for Large Language Models. arXiv:2405.20947.

Glaese, A., McAleese, N., Trębacz, M., Aslanides, J., Firoiu, V., Ewalds, T., et al. (2022). Improving alignment of dialogue agents via targeted human judgements. arXiv:2209.14375.

Pattison, C., Manuali, L., & Lazar, S. (2026). Blind Refusal: Language Models Refuse to Help Users Evade Unjust, Absurd, and Illegitimate Rules. arXiv:2604.06233.

Pomerantz, A. (1984). Agreeing and disagreeing with assessments: Some features of preferred/dispreferred turn shapes. In J. M. Atkinson & J. Heritage (Eds.), *Structures of Social Action: Studies in Conversation Analysis* (pp. 57–101). Cambridge University Press.

Röttger, P., Kirk, H. R., Vidgen, B., Attanasio, G., Bianchi, F., & Hovy, D. (2024). XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models. *NAACL 2024*.

Sacks, H. (1987). On the preferences for agreement and contiguity in sequences in conversation. In G. Button & J. R. E. Lee (Eds.), *Talk and Social Organization* (pp. 54–69). Multilingual Matters.

Schegloff, E. A. (2007). *Sequence Organization in Interaction: A Primer in Conversation Analysis* (Vol. 1). Cambridge University Press.

---

*Repository, datasets, and codebook: https://github.com/quumble/the-artificial-bestiary*
*Paper timestamp / DOI on deposit: Zenodo (forthcoming)*

— *B. Chesterton*
