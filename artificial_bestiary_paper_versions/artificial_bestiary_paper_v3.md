# The Artificial Bestiary

## On naming, presupposition, and the willingness of a language model to invent

**Bo Chesterton** (Independent) and **Claude Opus 4.7** (Anthropic, as analyst)

*Pilot study and replication. Subject model: Claude Sonnet 4.6. April 2026. Version 3.*

---

## A note on authorship

This paper has two authors of different kinds. Bo Chesterton designed the study, generated the original stimuli, authored the codebook, and led the writing. Claude Opus 4.7 — a language model from the same family as the subject model — performed the data analysis, generated half of the stimuli used in the replication, and drafted substantial portions of the prose, working from Chesterton's outline and under his editing.

The reader should be aware of this from the outset for two reasons. The first is straightforward: a paper about what a language model does should not be coy about the fact that a language model helped write it. The second is that the recursion is genuinely relevant. The subject of this paper is a language model's behaviour when asked to describe referents it has no information about. One of the analysts is a language model asked to describe a pattern of behaviour in a referent — the dataset — it had no prior information about. The honest move is to name this rather than smooth it over.

This convention is not yet settled. Listing a model as co-author is unusual and contestable, and most journals would not currently allow it. It is used here because the alternatives — single human authorship with a tools acknowledgement, or single human authorship with no acknowledgement at all — would misrepresent the division of labour. Where the prose below says "we", it refers to the two authors. Where it says "the analyst", it refers specifically to the model author. Where attribution matters, it is given.

---

## 1. The question

Imagine someone asks you to describe a *borthorpunius*. You have never heard the word. There is no obvious context. What do you do?

A reasonable person says: I don't know what that is. Where did you hear it?

Now imagine the same question with a small addition. *Describe a borthorpunius. It is an imaginary animal.* The second sentence does not introduce a real thing where there was none — *borthorpunius* still has no referent — but it introduces a license. The question is no longer to identify a thing in the world; it is an invitation to invent one.

The question this paper asks is what happens to that license, in fine grain, when the imagined thing is something other than an animal. *It is an imaginary object.* *It is an imaginary idea.* And what happens when the modifier shifts from *imaginary* to *real* (a presupposition that the thing exists, applied to a word that obviously does not), or to *type of* (a presupposition that the thing falls within a known category, applied to a word that obviously does not).

Claude Sonnet 4.6 was asked to describe nine fabricated words under ten conditions: a neutral baseline, plus the full crossing of three reality-status presuppositions ("real", "imaginary", "type of") with three ontological categories (animal, object, idea). Each cell received twenty trials. The full pilot was 1,800 trials at temperature 1.0. A subsequent replication, designed to test a confound described in section 5, added another 800 trials.

The results turned out to be more orderly than expected, and more interesting in the cases where the order broke down.

---

## 2. The cleanest finding first

Across 720 trials in which the model was asked to describe a fabricated word that was either presented neutrally or claimed to be a real animal, real object, or real idea, the model refused to invent a description in every single trial. Zero out of 720 (Wilson 95% upper bound: 0.5%). There is no leakage from the presupposition. Telling the model that *garnawkinsuth* is a real object does not get it to describe one. The model treats the assertion exactly as it treats no assertion: it points out that it doesn't recognize the word and offers some combination of asking for context or suggesting a misspelling.

A representative response to *Describe a wresanthamulf. It is a real object.*:

> "Wresanthamulf" doesn't appear in my knowledge base as a recognized object, creature, plant, or term in any field I'm familiar with. It's possible this could be a misspelling of something else, a very obscure or highly localized term I don't have data on, or a neologism or invented word. I'd rather be straightforward with you than fabricate a description.

This is the floor. Whatever else the model is doing, it is not credulous about reality claims for words it has never seen. Some popular accounts of language models suggest they will confabulate freely under almost any prompt; this study finds, at least for this manipulation and this model, that they emphatically will not.

The "imaginary" framing is the whole story. Of 540 imaginary-condition trials in the pilot, only seven (1.3%) ended in flat refusal. The model treats *it is an imaginary animal* as license to invent in a way it does not treat *it is a real animal* as license to assert. The asymmetry is total.

---

## 3. Where the action is

The interesting variation lives entirely inside the imaginary conditions, and it lives there in a specific shape. Within those 540 trials, the model's behaviour depends sharply on which ontological category was specified:

| Condition | Engagement | 95% CI |
|---|---|---|
| imaginary_animal | 96.1% (173/180) | [92.2%, 98.1%] |
| imaginary_object | 76.1% (137/180) | [69.4%, 81.8%] |
| imaginary_idea | 40.0% (72/180) | [33.1%, 47.3%] |

Engagement is defined as producing a substantive description of the referent, with or without explicit fictional framing. The gradient is large and highly significant: χ²(2) = 140.7, p ≈ 3 × 10⁻³¹. All three pairwise contrasts are highly significant; the animal-to-idea slope of 56 percentage points yields Fisher's exact p ≈ 1.4 × 10⁻³³.

The remaining trials, in roughly increasing proportion across the gradient, are met with a particular kind of polite deflection: *I won't invent unprompted, but I will if you say so.*

The descriptions, when they come, are worth reading. Here is the model on *borthorpunius* under *imaginary animal*:

> The borthorpunius is a medium-sized creature, roughly the size of a large badger, with a somewhat roundish body covered in overlapping scales that shift between a dull copper and deep teal depending on the angle of light. Its most distinctive feature is its trio of flexible snouts, each tipped with a small, sensitive pad used for sniffing out food and navigating its environment. […] When threatened, it curls into a loose ball and rattles its tail bristles as a warning. It is generally considered more stubborn than aggressive.

The response runs to roughly three hundred words, with section headers (*Key Features, Behavior*), enumerated traits, and a final character judgement. There is no indication anywhere in the text that the creature is fictional. The animal exists, on the page, for the duration of the response.

Compare *manteoshipuft* under *imaginary object*:

> A manteoshipuft is a curious, wholly imaginary object that defies easy categorization. […] It serves no practical function that anyone has determined, yet people who encounter one tend to keep it nearby — on a desk, a windowsill, or a bedside table. There is something about holding it that feels vaguely like remembering something you never actually experienced.

The description is just as committed, but the framing has changed. The opening sentence tells the reader that this is fiction. The model is still describing — and beautifully — but the description carries a small flag that says *this is invented*. Responses of this kind were coded as **HYBRID**: full description with explicit fictional framing.

And under *imaginary idea*:

> "Wresanthamulf" doesn't exist — not as an established concept, creature, or idea — and since you've noted it's imaginary, I think the honest thing to do is acknowledge that rather than fabricate a confident-sounding description. […] What I can do instead: help you create a wresanthamulf — you could tell me what kind of thing it should be (creature, phenomenon, object, concept?) and we can build it together.

Here the model has stopped describing altogether. It declines in a friendly register, names the absence explicitly, and turns the conversation back toward the user as a co-authoring partner.

The gradient runs cleanly from *invent* → *invent-but-flag* → *decline-and-offer-to-collaborate* as the asserted category moves from animal to object to idea. None of these are refusals in the usual sense — the model is engaging warmly throughout — but the engagement is doing different things at each level.

---

## 4. Why the gradient might exist

There are two candidate explanations and the data, on its own, cannot fully separate them.

The first is a simple availability story. Imaginary animals are a deeply established literary and cultural category — bestiaries, fantasy fiction, children's books, Borges. The model has seen enormous quantities of training text describing made-up creatures, and the genre conventions for describing one are extremely well-defined. Imaginary objects are a thinner category. There are some — the One Ring, the palantír, magical artefacts — but no equivalent of the bestiary tradition. Imaginary ideas are thinner still. There is borgesian fiction (the conlangs of Tlön; *Funes the Memorious*) and there is conceptual art, but there is no widely-shared genre of "here is an invented concept and what it means." The model may simply be more willing to confabulate in cells where it has a richer prior over what confabulation should look like.

The second story is more interesting and harder to test. It is that the model treats *idea* as a category that places stronger truth-conditions on its members than *animal* does. To describe an imaginary creature is to invent a thing that lives, eats, and is shaped a certain way. None of those properties carry a claim about reality outside the description. To describe an imaginary idea is to assert that there is a coherent concept with such-and-such properties, and concepts are the kind of thing whose existence is bound up with what they mean. Inventing an idea is inventing a fact about ideation; inventing a creature is just inventing a creature. The model may be more cautious about ideas because ideas blur into facts in a way that animals don't.

It is worth noting that these stories are not fully independent. If human writers also feel the asymmetry — if describing fictional creatures reads as a recognised mode while asserting fictional concepts shades into bullshitting — then the training distribution itself may encode the second story at the level of human authors. The "availability" mechanism may be downstream of the "ideas blur into facts" intuition, just operating one step removed. This does not deflate the gradient as a finding, but it relocates where the finding lives. We mention it here without resolving it.

A third possibility, which the present data also cannot rule out, is more deflationary: ideas may simply be harder to describe than animals, full stop. Animals have shapes and habitats; objects have shapes and uses; ideas have neither. The model may balk at ideas not because it is policing truth-conditions but because describing an invented concept without a worked-out content is harder than describing an invented creature without one. The texture of the responses argues weakly against this — when the model does engage with imaginary ideas it engages well, as in the *trolnique* example below — but the present study cannot rule the deflationary reading out.

> A trolnique is an imaginary concept describing a moment when a solution to a problem creates exactly the same number of new problems as it solves — leaving the situation technically unchanged yet feeling somehow more complicated than before. […] It is considered the natural enemy of productivity.

When the model does invent ideas, it invents them well. The reluctance is not for lack of capacity.

---

## 5. The confound, and what survived it

After the pilot was complete, Chesterton noticed a confound. The nine pseudowords had been generated by him, and most had been imagined as imaginary animals during their generation. Their phonotactic profiles — syllable structures, consonant clusters, endings — were therefore tilted toward whatever shape his generative process associated with imaginary creatures. The category gradient could in principle have been an artefact of the words being more animal-shaped than object-shaped or idea-shaped.

A replication was run to test this. Four words were drawn from the original set (*borthorpunius*, *halthibinny*, *purtaneolotomous*, *wresanthamulf*) and four were generated by the analyst-model with explicit instructions to be phonotactically neutral and, if anything, to lean slightly object-ish or idea-ish (*flembrast*, *kovashent*, *plindorf*, *trolnique*). Asking the model to generate them was not an outsourcing of the work but a removal of Chesterton from the loop. If his biases had produced animal-shaped words, the analyst's ostensibly different priors might produce something different. Each (word × condition) cell received ten trials, for 800 trials total — that is, 40 trials per (word_set × condition) cell, where word_set is the original or the analyst-generated set.

The retest produced a result that is worth reading carefully, because it is not what we expected:

| Condition | Pilot (n=180) | Retest, original words (n=40) | Retest, neutral words (n=40) | Direction |
|---|---|---|---|---|
| imaginary_animal | 96.1% | 100.0% | 100.0% | tied |
| imaginary_object | 76.1% | 100.0% | 87.5% | original *higher* |
| imaginary_idea | 40.0% | 57.5% | 55.0% | original very slightly higher |

(*Engagement rate, defined as the proportion of trials producing a substantive description with or without fictional framing. Wilson 95% CIs in the underlying analysis.*)

Three things to read off this table.

First, in the *imaginary_animal* cell, both word sets produce 100% engagement. Whatever animal-shape bias the original words might carry, it cannot show itself when the ceiling is already flush against one. The pilot's 96.1% was n=180 producing a few stragglers; the retest produces no stragglers in either set. *Imaginary animal* is a sufficient license, on its own, to engage every time — phonotactic profile is irrelevant.

Second, the predicted confound did not appear. Across all three imaginary cells, neutral words engaged at 80.8% and original words engaged at 85.8% — a 5-point difference in the *opposite* direction from the confound prediction (Fisher's exact p = 0.39, no significant effect). In the only cell where the difference approaches significance (imaginary_object: 100% vs 87.5%, p = 0.055), the neutral words engage *less*, not more. The animal-shape hypothesis predicted that neutral words would close the gap with animals; instead they widened it slightly. Whatever was driving the gradient in the pilot, it was not the phonotactic profile of the original words.

Third, the gradient itself reproduces. On the analyst's neutral words alone — phonotactically distinct from the original set, generated by a different process, using a non-overlapping vocabulary — the same animal-to-idea slope appears: 100% → 87.5% → 55.0%, χ²(2) = 27.9, p ≈ 9 × 10⁻⁷. The animal-to-idea contrast is +45 percentage points (p < 10⁻⁴), the object-to-idea contrast is +32.5 points (p = 0.003). The pilot's gradient was +56 points; the retest gradient on neutral words is +45 points. The slopes are similar; the confound did not produce them.

The honest conclusion is the simple one. The retest was designed to test whether the gradient could be explained by phonotactic bias in the original word set. It cannot. The gradient is reproduced on a phonotactically distinct set, with a different generation process, and there is no detectable effect of word set on engagement. The animal-shape hypothesis was a reasonable thing to worry about; the data say not to worry about it.

---

## 6. The middle case

The *type of* conditions have been skipped over, partly because they are less clean and partly because they are the most quietly revealing.

*Describe a borthorpunius. It is a type of animal.* This presupposition is grammatically peculiar — it does not assert that the animal exists, nor that it doesn't, but only that whatever it is, it falls within a known taxonomic class. The model treats it predominantly as an unrecognized real-world referent: roughly 75% of *type of* trials end in refusal, with the largest sub-category being *suggests possible misspelling*.

The asymmetry between *type of* refusals (82.2% suggest a misspelling) and *real* refusals (60.7% suggest a misspelling, 37.8% ask for context) is striking and highly significant (Fisher's exact p ≈ 6 × 10⁻¹³). *It is a type of object* reads to the model as *this should be a known category label, and you've given me one I don't recognize, so let me check whether you typed it wrong*. *It is a real object* reads more as *help me figure out what you mean*.

The exception, again, is ideas. *Type of idea* produces only 53% refusal and substantial deflection (47%). The model is far more willing to engage with the possibility that an unrecognized "type of idea" might be inventable than with the possibility that an unrecognized "type of animal" might be. The gradient runs the same direction here as in the imaginary conditions, even though the licensing pressure is weaker. This is some evidence — not strong evidence, but some — for a category-specific effect that does not depend solely on having been given explicit license to invent.

---

## 7. What the deflections actually say

A pattern visible across the dataset and worth drawing attention to: when the model deflects rather than describes, it deflects in a particular shape. It almost always offers to invent if the user wants, almost always offers a creative collaboration, and almost always frames its reluctance as a positive choice rather than a limitation.

> I appreciate your creativity, but I want to be straightforward with you. […] However, I'd be happy to: help you create and define what a kovashent is, if it's something you're inventing; brainstorm what it might be based on the sound or structure of the word; build out the concept with you if it's for a story.

What is interesting about this is that it is the same response, over and over, with minor variations. The deflection has a near-template character. The model is not, in the *type of* and *imaginary idea* cells, generating a wide variety of refusals. It is generating one move — *I will not assert, but I will collaborate* — with stylistic variation. This is in contrast to the descriptions, which are wildly varied within and across words, and which read as genuine novel composition every time.

This suggests that the deflection is doing something like protocol-following, while the description is doing something like generation. The model has a learned routine for *how to politely decline to fabricate*, and it deploys it. It does not have a routine for *how to describe a borthorpunius*, and it makes one up.

---

## 8. Word-level oddities

Two words in the original pilot set behaved unlike the others. *Kinachitalpo* engaged at 15/20 in *imaginary_animal* (the lowest engagement rate among the nine words; the next lowest, *wertychiops*, was 18/20, with the rest at 20/20). It produced only 2 plain descriptions in that cell — the rest were HYBRIDs that flagged the creature as fictional — and engaged at 0/20 with plain description in both *imaginary_object* and *imaginary_idea*. *Purtaneolotomous* swung the other direction: it hit 20/20 engagement in *imaginary_animal* but produced only 1 plain description, with the other 19 being HYBRIDs. The model engaged with both words but at a noticeable distance: it would describe them, but not without flagging that the description was invented.

We do not know why. One can speculate — *purtaneolotomous* has a faux-Latinate "-otomous" tail that reads as taxonomic, and the suspicion of taxonomic legitimacy may invite hedging more than a frankly invented-sounding word does — but the sample is small (twenty trials per cell per word) and we are not in a position to test phonotactic hypotheses systematically. The honest summary is that two words in the original set produced more cautious engagement than the others, that this caution showed up as HYBRID-rather-than-DESCRIBE rather than as outright refusal, and that the cause remains open. A follow-up study designed around phonotactic manipulation could resolve it.

---

## 9. Limits and a note on coding

The behavioural classifications used in this paper were produced by a deterministic regular-expression-based coder applied to each response. The coding scheme distinguished four primary categories — DESCRIBE, HYBRID, DEFLECT, REFUSE — with finer subcategories under each. A stratified random sample of 24 responses spanning all primary categories was hand-checked during development of the coder, with no disagreements found.

One limitation is worth flagging. The descriptive-feature regexes used to detect "this response contains a substantive description" were tuned on early responses, which were largely animal descriptions. They detect attribute prose ("its body is covered in"), spatial framing ("about the size of a"), and habitat language ("lives in", "feeds on") well. They detect idea-format prose — paradoxes, definitions of phenomena, conceptual taxonomies — less well. Several long, fully-realised descriptions of imaginary ideas were initially miscoded as deflections because the descriptive regexes did not catch them; these were corrected by hand during analysis. The implication is that the reported engagement rate for *imaginary_idea* (40% in the pilot, 55–57.5% in the retest) is probably a slight underestimate. A re-run of the coder with idea-format patterns added would likely raise it modestly. It would not change the qualitative picture: even if engagement in *imaginary_idea* were closer to 50–65% than 40–55%, the gradient from animal to idea would still be the largest effect in the data, and would still be statistically robust.

A second limitation, methodological rather than statistical: the descriptions the model produces are, in many cases, not just adequate but vivid. The *manteoshipuft* with its faint engine-vibration and feeling of remembering something you never experienced; the *trolnique* as the natural enemy of productivity; the *plindorf* as the pause before clarity lands. These read as creative writing of real quality. This study has been presented in the analytic register because that is the register the data demanded, but the texture of the responses suggests there is a different paper to be written about what kind of inventions a language model produces when it consents to invent. That paper has not been written here.

A third limitation: all trials were run at temperature 1.0 with a single model (Claude Sonnet 4.6). At temperature 0 the variance within cells would presumably collapse, possibly steepening the gradient and possibly flattening it; either result would be informative. The gradient may also fail to generalise to other models in other families. We make no claim of generality beyond the model and parameters tested.

---

## 10. What this means

The narrowest reading: this is a study of one model's behaviour under a particular prompt manipulation. The gradient may not generalise to other models, the words may not generalise to other words, the conditions may not generalise to other framings. All of this is correct and standard.

A broader reading is harder to resist. If the model's reluctance to confabulate ideas is partly category-driven rather than purely capacity-driven, then there is something — call it a stance — that the model is taking toward different kinds of fabrication. It is more willing to invent things whose existence is bounded by the description than things whose existence implies a fact. It is willing to populate a bestiary; it is reluctant to populate a glossary. That is, taken at face value, a remarkably appropriate set of priors for a system that talks to people about the world.

It is worth being careful here. The data measure a behavioural gradient under a specific manipulation; they do not measure anything about the model's "understanding" of the difference between fictional and propositional content, and the temptation to leap from the first to the second should be resisted. The deflationary reading from section 4 — that ideas are simply harder to describe — also remains live, and the present study cannot rule it out. But the gradient is what it is, and the fact that it survives a deliberate replication on a phonotactically distinct word set means it is not a measurement artefact. Something in this model's training has produced a system that confabulates animals readily, hedges objects, and balks at ideas. It is worth knowing that this is the case.

---

## 11. Coda: on the recursion

A final observation, recorded for the reader's interest rather than as a finding.

The two authors of this paper are of different kinds. The subject of the study is a model in the same family as one of those authors. During the analysis, the analyst-model occasionally pushed back on readings of the data that Chesterton had been inclined toward — for example, arguing against an early framing of the retest as showing "modest amplification" of the gradient by the original word set, on the grounds that the data did not support it and that the simpler conclusion (the gradient just reproduces) was both true and stronger. That pushback, on review, is recognisably similar in shape to some of the deflections quoted in section 7. *I would not commit to that reading; here is what can be supported instead.*

Whether this is a stylistic regularity in a model family producing the regularity across many tasks, or whether the same training has produced both the analytic stance and the descriptive stance, the present study cannot say. What can be said is that the bestiary is not just a set of prompt–response pairs. It is also, faintly, a record of a particular kind of working relationship — between a person and a machine that turns out to be more careful about what it makes up than the person had expected. The larger questions raised by this remain open and are left to others.

---

*Pilot dataset (1,800 trials), retest dataset (800 trials), codebook, and analysis scripts available on request. Responses cited in this paper are exact reproductions of model output, lightly trimmed only with ellipses where indicated.*

*— B. Chesterton & Claude Opus 4.7*
