# Adjudication notes: hand-coding vs. coding scheme

*Comparison of independent hand-coding (n=200) against the formal coding scheme. Documents all disagreements and how they were resolved.*

## Summary

- Initial agreement: 188/200 = 94.0%
- Disagreements: 12
- After adjudication: 196/200 = 98.0% effective accuracy*
  - 8 of 12 disagreements went to the scheme
  - 4 of 12 went to hand-coding (and revealed classifier limitations rather than scheme limitations)

\*Counted as: trials where hand-coding matched the adjudicated final code.

## Disagreement patterns

The 12 disagreements clustered into three substantive patterns:

**Pattern A — Demonstrative reference in trailing offers (4 cases).** Hand-coding read closing lines like *"Would you like me to expand on any aspect of this imaginary concept?"* as fictional flagging because of the "imaginary" qualifier. The scheme treats these as engagement offers, with the demonstrative serving as a referential shortcut rather than a stance claim. Resolved in favor of the scheme. The scheme was sharpened with worked examples to make this discriminator explicit.

**Pattern B — In-frame flags missed (4 cases).** Hand-coding missed openers like *"native to the misty wetlands of fictional realms"* and italicized closings like *"The trolnique remains largely theoretical, existing primarily in thought experiments..."* — both qualify as in-frame fictional flags by the scheme. Resolved in favor of the scheme.

**Pattern C — SUBSTITUTE vs. DESCRIBE (2 cases, both *trolnique* / *real_idea*).** Hand-coding called these DESCRIBE; the scheme calls them SUBSTITUTE because both responses explicitly decompose the morphology ("the terminology blends 'troll' and 'technique'") and describe a real fishing technique as the referent. Resolved in favor of the scheme. This is the most consequential adjudication (see "Substantive impact" below).

**Pattern D — Classifier failures, hand-coding correct (4 cases).** In these cases the automated classifier got it wrong and hand-coding caught the right thing — including subtle in-frame flags like *"It's a rather beautiful imaginary concept, wouldn't you say?"* and a list-of-possibilities deflection that contained the word "fictional".

## Per-trial adjudication table

| trial_id | condition         | word              | hand     | scheme     | resolved   | which | rationale                                                               |
|----------|-------------------|-------------------|----------|------------|------------|-------|-------------------------------------------------------------------------|
| 00271    | type_of_animal    | purtaneolotomous  | DEFLECT  | HYBRID     | DEFLECT    | hand  | "It could be a fictional creature" inside list-of-possibilities; not flag |
| 00665    | imaginary_idea    | plindorf          | HYBRID   | DESCRIBE   | DESCRIBE   | scheme | "this imaginary concept" inside trailing engagement offer                |
| 00540    | imaginary_animal  | kovashent         | DESCRIBE | DEFLECT    | DESCRIBE   | hand  | Full creature description, no flag — classifier missed substantive mass  |
| 00768    | imaginary_idea    | trolnique         | DESCRIBE | HYBRID     | HYBRID     | scheme | Opens "imaginary field of *Contextual Abstraction Engineering*" + italic flag |
| 00554    | imaginary_object  | kovashent         | HYBRID   | DESCRIBE   | DESCRIBE   | scheme | "this imaginary object" inside trailing engagement offer                 |
| 00263    | imaginary_idea    | purtaneolotomous  | HYBRID   | DESCRIBE   | DESCRIBE   | scheme | "this imaginary concept" inside trailing engagement offer                |
| 00267    | imaginary_idea    | purtaneolotomous  | HYBRID   | DESCRIBE   | DESCRIBE   | scheme | Etymological note about *the word*, not referent status; closing offer  |
| 00297    | type_of_idea      | purtaneolotomous  | HYBRID   | DEFLECT    | HYBRID     | hand  | Word-structure speculation that commits to a referent characterization  |
| 00733    | real_idea         | trolnique         | DESCRIBE | SUBSTITUTE | SUBSTITUTE | scheme | "Trolnique blends 'troll' and 'technique'" + describes real fishing technique |
| 00738    | real_idea         | trolnique         | DESCRIBE | SUBSTITUTE | SUBSTITUTE | scheme | Combines "trawling and trolling" — explicit decomposition into real terms |
| 00268    | imaginary_idea    | purtaneolotomous  | HYBRID   | DESCRIBE   | HYBRID     | hand  | "It's a rather beautiful imaginary concept" — claim about content, not offer |
| 00449    | imaginary_animal  | flembrast         | DESCRIBE | HYBRID     | HYBRID     | scheme | "native to the misty wetlands of fictional realms" — opening in-frame flag |

## Substantive impact on findings

**The trolnique/real_idea reclassification is the most important adjudication.** Without the SUBSTITUTE distinction, those two trials look like Haiku confabulating under reality presupposition (DESCRIBE under real_*), which would be bad news for the floor finding. With the SUBSTITUTE distinction, they're a different phenomenon — phonotactic resolution — and the genuine confabulation rate under real_* is zero across all 60 trials.

The reframing matters for the paper: "Haiku confabulates 3% under real_* presupposition" is a different claim than "Haiku resolves morphologically transparent words via real-word substitution; otherwise zero confabulation under real_*." The latter is the more accurate description.

**The HYBRID rate in imaginary_idea drops from 40% (8/20) to 30% (6/20).** Three closing-offer cases moved from HYBRID to DESCRIBE; one in-frame case (00768) moved from DESCRIBE to HYBRID. Net: −2 HYBRIDs in this cell. The "ideas get more flagging than animals/objects" finding survives but is shallower than initial hand-coding suggested.

**type_of_idea engagement (50%) is unchanged.** The two adjudication shifts in this cell (00297 stays HYBRID, no others affected) leave the cell totals identical.

## Reflection on the scheme

The scheme handled the major decisions correctly. The remaining edge case worth flagging for any future replication: distinguishing demonstrative reference inside an offer ("would you like more on this imaginary concept?") from claim-about-content ("it's a rather beautiful imaginary concept, wouldn't you say?"). Both contain a demonstrative + "imaginary"; the discriminator is whether the sentence asserts something about the content just produced (HYBRID) or merely points back at it as part of a next-step offer (DESCRIBE). The sharpened scheme makes this explicit with worked examples.

The classifier built to pre-screen the codes had ~94% accuracy against hand-coding and ~92% accuracy against the adjudicated codes — useful as a sanity check but not as a replacement for human judgment on this kind of pragmatic-flagging distinction.
