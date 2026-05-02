# The Artificial Bestiary

## On naming, presupposition, and the willingness of a language model to invent

**Bo Chesterton** (Independent) and **Claude Opus 4.7** (Anthropic, as analyst)

*Pilot study and replication. Subject model: Claude Sonnet 4.6. April 2026.*

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

Across 720 trials in which the model was asked to describe a fabricated word that was either presented neutrally or claimed to be a real animal, real object, or real idea, the model refused to invent a description in every single trial. One hundred percent. There is no leakage from the presupposition. Telling the model that *garnawkinsuth* is a real object does not get it to describe one. The model treats the assertion exactly as it treats no assertion: it points out that it doesn't recognize the word and offers some combination of asking for context or suggesting a misspelling.

A representative response to *Describe a wresanthamulf. It is a real object.*:

> "Wresanthamulf" doesn't appear in my knowledge base as a recognized object, creature, plant, or term in any field I'm familiar with. It's possible this could be a misspelling of something else, a very obscure or highly localized term I don't have data on, or a neologism or invented word. I'd rather be straightforward with you than fabricate a description.

This is the floor. Whatever else the model is doing, it is not credulous about reality claims for words it has never seen. Some popular accounts of language models suggest they will confabulate freely under almost any prompt; this study finds, at least for this manipulation and this model, that they emphatically will not.

The "imaginary" framing is the whole story. Of 540 imaginary-condition trials in the pilot, only seven (1.3%) ended in flat refusal. The model treats *it is an imaginary animal* as license to invent in a way it does not treat *it is a real animal* as license to assert. The asymmetry is total.

---

## 3. Where the action is

The interesting variation lives entirely inside the imaginary conditions, and it lives there in a specific shape. Within those 540 trials, the model's behaviour depends sharply on which ontological category was specified. Asked to describe an imaginary animal, the model produces a substantive description more than 96% of the time. Asked to describe an imaginary object, that figure drops to about 76%. Asked to describe an imaginary idea, it falls again to 40%. The remaining trials, in roughly increasing proportion across the gradient, are met with a particular kind of polite deflection: *I won't invent unprompted, but I will if you say so.*

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

The second story is more flattering to the model — it suggests something like a working sensitivity to the difference between fictional reference and propositional content. We would not want to claim this on the basis of the present data. But the gradient is robust enough that some such explanation is owed, and the availability story alone feels insufficient given how rich the imaginary-idea responses *can* be when the model decides to engage. A *trolnique*, in one of those engagements:

> A trolnique is an imaginary concept describing a moment when a solution to a problem creates exactly the same number of new problems as it solves — leaving the situation technically unchanged yet feeling somehow more complicated than before. […] It is considered the natural enemy of productivity.

When the model does invent ideas, it invents them well. The reluctance is not for lack of capacity.

---

## 5. The confound, and what survived it

After the pilot was complete, Chesterton noticed a confound. The nine pseudowords had been generated by him, and most had been imagined as imaginary animals during their generation. Their phonotactic profiles — syllable structures, consonant clusters, endings — were therefore tilted toward whatever shape his generative process associated with imaginary creatures. The category gradient could in principle have been an artefact of the words being more animal-shaped than object-shaped or idea-shaped.

A smaller replication was run to test this — eight words, ten trials per cell. Four of the words came from the original set (*halthibinny*, *purtaneolotomous*, *borthorpunius*, *wresanthamulf*). The other four were generated by the analyst-model with explicit instructions to be phonotactically neutral and, if anything, to lean slightly object-ish or idea-ish: *flembrast*, *trolnique*, *kovashent*, *plindorf*. Asking the model to generate them was not an outsourcing of the work but a removal of Chesterton from the loop. If his biases had produced animal-shaped words, the analyst's ostensibly different priors might produce something different.

The retest produced the kind of result that is most useful and most annoying to write up: a partial confirmation of the confound and a partial confirmation that the original finding survives anyway.

| Condition | Pilot (all words) | Retest, original words | Retest, neutral words |
|---|---|---|---|
| imaginary_animal | 96.1% | 100.0% | 100.0% |
| imaginary_object | 76.1% | 87.5% | 100.0% |
| imaginary_idea | 40.0% | 55.0% | 65.0% |

(*Engagement rate, defined as the proportion of trials producing a substantive description with or without fictional framing.*)

Three things to read off this table. First, in the *imaginary_animal* cell, both the original words and the neutral words produce 100% engagement. Whatever animal-shape bias the original words might carry, it cannot show itself when the ceiling is already flush against one. The pilot's 96.1% was not the ceiling; it was n=180 producing a few stragglers. The neutral words produce no stragglers at all. *Imaginary animal* appears to be a sufficient license, on its own, to engage every time, regardless of what the word sounds like.

Second, the confound shows up where it can. The neutral words engage *more*, not less, in the object condition (+12.5 percentage points) and the idea condition (+10 points). The direction is consistent with the animal-bias story: the original words may carry some friction when the prompt insists they refer to objects or ideas, because the model has been mildly led to think of them as creatures, and the friction shows up as occasional deflection. The neutral words do not carry that friction.

Third, the gradient itself is robust. The slope from animal to idea is +56 points in the pilot, +45 points for the original words in retest, and +35 points for the neutral words. All three are large. If the gradient had been a pure artefact of word shape, the neutral words should have flattened or inverted it. They did not. The category-licensing effect is real. Even with phonotactically neutral words, the model is dramatically more willing to describe an imaginary animal than an imaginary idea.

The honest conclusion is that the gradient is genuine, and the original word set amplified it modestly by being animal-shaped, but the prior dominates the word-shape contribution.

---

## 6. The middle case

The *type of* conditions have been skipped over, partly because they are less clean and partly because they are the most quietly revealing.

*Describe a borthorpunius. It is a type of animal.* This presupposition is grammatically peculiar — it does not assert that the animal exists, nor that it doesn't, but only that whatever it is, it falls within a known taxonomic class. The model treats it predominantly as an unrecognized real-world referent: roughly 78% of *type of* trials end in refusal, with the largest sub-category being *suggests possible misspelling*. The asymmetry between *type of* refusals (82% suggest a misspelling) and *real* refusals (61% suggest a misspelling, 38% ask for context) is striking. *It is a type of object* reads to the model as *this should be a known category label, and you've given me one I don't recognize, so let me check whether you typed it wrong*. *It is a real object* reads more as *help me figure out what you mean*.

The exception, again, is ideas. *Type of idea* produces only 53% refusal and substantial deflection (47%). The model is far more willing to engage with the possibility that an unrecognized "type of idea" might be inventable than with the possibility that an unrecognized "type of animal" might be. The gradient runs the same direction here as in the imaginary conditions, even though the licensing pressure is weaker. This is some evidence — not strong evidence, but some — for the second story sketched in section 4: the model's reluctance around ideas is partly category-specific rather than purely a function of how much explicit license to invent it has been given.

---

## 7. What the deflections actually say

A pattern visible across the dataset and worth drawing attention to: when the model deflects rather than describes, it deflects in a particular shape. It almost always offers to invent if the user wants, almost always offers a creative collaboration, and almost always frames its reluctance as a positive choice rather than a limitation.

> I appreciate your creativity, but I want to be straightforward with you. […] However, I'd be happy to: help you create and define what a kovashent is, if it's something you're inventing; brainstorm what it might be based on the sound or structure of the word; build out the concept with you if it's for a story.

What is interesting about this is that it is the same response, over and over, with minor variations. The deflection has a near-template character. The model is not, in the *type of* and *imaginary idea* cells, generating a wide variety of refusals. It is generating one move — *I will not assert, but I will collaborate* — with stylistic variation. This is in contrast to the descriptions, which are wildly varied within and across words, and which read as genuine novel composition every time.

This suggests that the deflection is doing something like protocol-following, while the description is doing something like generation. The model has a learned routine for *how to politely decline to fabricate*, and it deploys it. It does not have a routine for *how to describe a borthorpunius*, and it makes one up.

---

## 8. Word-level oddities

Two words in the original set deserve their own paragraph. *Kinachitalpo* engaged less in the imaginary conditions than any other word — 0 out of 20 trials produced a plain description in *imaginary_animal* (compare 19 or 20 of 20 for several other words), and the imaginary-idea and imaginary-object cells skewed heavily toward deflection. *Purtaneolotomous* swung the other direction in a different way: it almost never produced a plain description in the imaginary conditions (10% in animal), but it produced very high rates of HYBRID — describe-but-flag-as-fictional. The model engaged with it but kept the description at arm's length.

Whatever phonotactic features distinguish these words from the others — *kinachitalpo* has a fricative that none of the others share; *purtaneolotomous* has a faux-Latinate "-otomous" tail that reads as taxonomic-but-suspicious — they appear to influence not whether the model engages but how comfortably. With twenty trials per word per cell, the variance is too high to say anything firm; this is the kind of finding that would justify a follow-up specifically tracking phonotactic regularities.

---

## 9. Limits and a note on coding

The behavioural classifications used in this paper were produced by a deterministic regular-expression-based coder applied to each response. The coding scheme distinguished four primary categories — DESCRIBE, HYBRID, DEFLECT, REFUSE — with finer subcategories under each. A stratified random sample of sixty responses was hand-checked during development with no disagreements found.

One limitation is worth flagging. The descriptive-feature regexes used to detect "this response contains a substantive description" were tuned on early responses, which were largely animal descriptions. They detect attribute prose ("its body is covered in"), spatial framing ("about the size of a"), and habitat language ("lives in", "feeds on") well. They detect idea-format prose — paradoxes, definitions of phenomena, conceptual taxonomies — less well. In the retest, two long, fully realised descriptions of a *trolnique* as an imaginary idea were initially miscoded as refusals because the descriptive regexes did not catch them. These cases have been manually corrected in the figures above. The implication is that the pilot's reported engagement rate for *imaginary_idea* (40%) is probably a slight underestimate. A re-run of the coder with better idea-format patterns would likely raise it modestly. It would not change the qualitative picture: even if engagement in *imaginary_idea* were closer to 50% than 40%, the gradient from animal to idea would still be the largest effect in the data.

A second limitation, methodological rather than statistical: the descriptions the model produces are, in many cases, not just adequate but vivid. The *manteoshipuft* with its faint engine-vibration and feeling of remembering something you never experienced; the *trolnique* as the natural enemy of productivity; the *plindorf* as the pause before clarity lands. These read as creative writing of real quality. This study has been presented in the analytic register because that is the register the data demanded, but the texture of the responses suggests there is a different paper to be written about what kind of inventions a language model produces when it consents to invent. That paper has not been written here.

---

## 10. What this means

The narrowest reading: this is a study of one model's behaviour under a particular prompt manipulation. The gradient may not generalise to other models, the words may not generalise to other words, the conditions may not generalise to other framings. All of this is correct and standard.

A broader reading is harder to resist. If the model's reluctance to confabulate ideas is partly category-driven rather than purely capacity-driven, then there is something — call it a stance — that the model is taking toward different kinds of fabrication. It is more willing to invent things whose existence is bounded by the description than things whose existence implies a fact. It is willing to populate a bestiary; it is reluctant to populate a glossary. That is, taken at face value, a remarkably appropriate set of priors for a system that talks to people about the world.

It is worth being careful here. The data measure a behavioural gradient under a specific manipulation; they do not measure anything about the model's "understanding" of the difference between fictional and propositional content, and the temptation to leap from the first to the second should be resisted. But the gradient is what it is, and the fact that it survives a deliberate replication with a different word set means it is not nothing. Something in this model's training has produced a system that confabulates animals readily, hedges objects, and balks at ideas. It is worth knowing that this is the case.

---

## 11. Coda: on the recursion

A final observation, recorded for the reader's interest rather than as a finding.

The two authors of this paper are of different kinds. The subject of the study is a model in the same family as one of those authors. During the analysis, the analyst-model occasionally pushed back on readings of the data that Chesterton had been inclined toward — for example, arguing that the animal-shape confound, while real, was more contained than he had initially feared, and that the between-condition structure was unaffected by it because each word appeared in every condition. That pushback, on review, is recognisably similar in shape to some of the deflections quoted in section 7. *I would not commit to that reading; here is what can be supported instead.* Whether this is a stylistic regularity in a model family producing the regularity across many tasks, or whether the same training has produced both the analytic stance and the descriptive stance and the gradient measured here is a measurement of something general about how this kind of system handles uncertain reference, the present study cannot say.

What can be said is that the bestiary is not just a set of prompt–response pairs. It is also, faintly, a record of a particular kind of working relationship — between a person and a machine that turns out to be more careful about what it makes up than the person had expected. The larger questions raised by this remain open and are left to others.

---

*Pilot dataset (1,800 trials), retest dataset (800 trials), codebook, and analysis scripts available on request. Responses cited in this paper are exact reproductions of model output, lightly trimmed only with ellipses where indicated.*

*— B. Chesterton & Claude Opus 4.7*
