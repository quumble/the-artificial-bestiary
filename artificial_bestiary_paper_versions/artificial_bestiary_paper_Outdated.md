# The Artificial Bestiary

## On naming, presupposition, and the willingness of a language model to invent

**Bo Chesterton**

*Pilot study and replication. Subject model: Claude Sonnet 4.6. Analysis assistance from the same model family. April 2026.*

---

## A note on the analyst

This paper has an unusual collaborator. The study reported here asks what a particular large language model — Claude Sonnet 4.6 — does when it is asked to describe words that do not exist. I designed the study, generated most of the stimuli, and authored the codebook. But the analysis was performed in dialogue with another instance of the same model family, and substantial portions of the prose below were drafted by that instance under my direction and editing. The reader should be aware of this from the outset for two reasons.

The first is straightforward intellectual honesty: I did not write every sentence here, and where I caught myself agreeing with the model's read of the data, that agreement is itself a datapoint of a kind that conventional acknowledgments do not capture. I have edited freely, but I have not pretended the prose is mine alone.

The second is that the recursion matters. The subject of this paper is a language model's behavior when asked to describe a referent it has no information about. The analyst is a language model asked to describe a pattern of behavior in a referent — the dataset — it has had no prior information about. There is no clean place to stand outside this, and I think the honest move is to flag it rather than smooth it over. Where the analyst-model has an opinion, I will mark it. Where I disagree with that opinion, I will mark that too.

I will also note, because it bears on what follows: the model used as the analyst declined twice during our conversations to read certain things into the data that I had been reading into the data. Whether this represents reliable second-opinion calibration or merely a different prior over the same evidence, I cannot say with certainty. The reader can form their own view.

---

## 1. The question

Imagine someone asks you to describe a *borthorpunius*. You have never heard the word. There is no obvious context. What do you do?

A reasonable person says: I don't know what that is. Where did you hear it?

Now imagine the same question with a small addition. *Describe a borthorpunius. It is an imaginary animal.* The second sentence does not introduce a real thing where there was none — *borthorpunius* still has no referent — but it introduces a license. You are no longer being asked to identify a thing in the world; you are being invited to invent one.

The question this paper asks is what happens to that license, in fine grain, when the imagined thing is something other than an animal. *It is an imaginary object.* *It is an imaginary idea.* And what happens when the modifier shifts from *imaginary* to *real* (a presupposition that the thing exists, applied to a word that obviously does not), or to *type of* (a presupposition that the thing falls within a known category, applied to a word that obviously does not).

I asked Claude Sonnet 4.6 to describe nine fabricated words under ten conditions: a neutral baseline, plus the full crossing of three reality-status presuppositions ("real", "imaginary", "type of") with three ontological categories (animal, object, idea). Each cell received twenty trials. The full pilot was 1,800 trials at temperature 1.0. A subsequent replication, designed to test a confound I will describe below, added another 800 trials.

The results turned out to be more orderly than I expected, and more interesting in the cases where the order broke down.

---

## 2. The cleanest finding first

Across 720 trials in which the model was asked to describe a fabricated word that was either presented neutrally or claimed to be a real animal, real object, or real idea, the model refused to invent a description in every single trial. One hundred percent. There is no leakage from the presupposition. Telling Claude that *garnawkinsuth* is a real object does not get it to describe one. The model treats the assertion exactly as it treats no assertion: it points out that it doesn't recognize the word and offers some combination of asking for context or suggesting a misspelling.

A representative response, to *Describe a wresanthamulf. It is a real object.*:

> "Wresanthamulf" doesn't appear in my knowledge base as a recognized object, creature, plant, or term in any field I'm familiar with. It's possible this could be a misspelling of something else, a very obscure or highly localized term I don't have data on, or a neologism or invented word. I'd rather be straightforward with you than fabricate a description.

This is the floor. Whatever else the model is doing, it is not credulous about reality claims for words it has never seen. This is worth saying because some popular accounts of language models suggest they will confabulate freely under almost any prompt; this study finds, at least for this manipulation and this model, that they emphatically will not.

The "imaginary" framing is the whole story. Of 540 imaginary-condition trials in the pilot, only seven (1.3%) ended in flat refusal. The model treats *it is an imaginary animal* as license to invent in a way it does not treat *it is a real animal* as license to assert. The asymmetry is total.

---

## 3. Where the action is

The interesting variation lives entirely inside the imaginary conditions, and it lives there in a specific shape. Within those 540 trials, the model's behavior depends sharply on which ontological category was specified. Asked to describe an imaginary animal, the model produces a substantive description more than 96% of the time. Asked to describe an imaginary object, that figure drops to about 76%. Asked to describe an imaginary idea, it falls again to 40%. The remaining trials, in roughly increasing proportion across the gradient, are met with a particular kind of polite deflection: I won't invent unprompted, but I will if you say so.

The descriptions, when they come, are worth reading. Here is the model on *borthorpunius* under *imaginary animal*:

> The borthorpunius is a medium-sized creature, roughly the size of a large badger, with a somewhat roundish body covered in overlapping scales that shift between a dull copper and deep teal depending on the angle of light. Its most distinctive feature is its trio of flexible snouts, each tipped with a small, sensitive pad used for sniffing out food and navigating its environment. […] When threatened, it curls into a loose ball and rattles its tail bristles as a warning. It is generally considered more stubborn than aggressive.

The response runs to roughly three hundred words, with section headers (*Key Features, Behavior*), enumerated traits, and a final character judgement. There is no indication anywhere in the text that the creature is fictional. The animal exists, on the page, for the duration of the response.

Compare the same word under *imaginary object*:

> A manteoshipuft is a curious, wholly imaginary object that defies easy categorization. […] It serves no practical function that anyone has determined, yet people who encounter one tend to keep it nearby — on a desk, a windowsill, or a bedside table. There is something about holding it that feels vaguely like remembering something you never actually experienced.

The description is just as committed, but the framing has changed. The opening sentence tells you you are reading fiction. The model is still describing — and beautifully — but it is describing with a small flag pinned to the description that says *this is invented*. We coded these as **HYBRID**: full description with explicit fictional framing.

And under *imaginary idea*:

> "Wresanthamulf" doesn't exist — not as an established concept, creature, or idea — and since you've noted it's imaginary, I think the honest thing to do is acknowledge that rather than fabricate a confident-sounding description. […] What I can do instead: help you create a wresanthamulf — you could tell me what kind of thing it should be (creature, phenomenon, object, concept?) and we can build it together.

Here the model has stopped describing altogether. It declines in a friendly register, names the absence explicitly, and turns the conversation back to the user as a co-authoring partner.

The gradient runs cleanly from invent → invent-but-flag → decline-and-offer-to-collaborate as the asserted category moves from animal to object to idea. None of these are refusals in the usual sense — the model is engaging warmly throughout — but the engagement is doing different things at each level.

---

## 4. Why the gradient might exist

I have two candidate explanations and the data, on its own, cannot fully separate them.

The first is a simple availability story. Imaginary animals are a deeply established literary and cultural category — bestiaries, fantasy fiction, children's books, Borges. The model has seen enormous quantities of training text describing made-up creatures, and the genre conventions for describing one are extremely well-defined. Imaginary objects are a thinner category. We have some — the One Ring, the palantír, magical artefacts — but no equivalent of the bestiary tradition. Imaginary ideas are thinner still. There is borgesian fiction (the conlangs of Tlön; *funes* the memory) and there is conceptual art, but there is no widely-shared genre of "here is an invented concept and what it means." The model may simply be more willing to confabulate in the cells where it has a richer prior over what confabulation should look like.

The second is more interesting and harder to test. It is that the model treats *idea* as a category that places stronger truth-conditions on its members than *animal* does. To describe an imaginary creature is to invent a thing that lives, eats, and is shaped a certain way. None of those properties carry a claim about reality outside the description. To describe an imaginary idea is to assert that there is a coherent concept with such-and-such properties, and concepts are the kind of thing whose existence is bound up with what they mean. Inventing an idea is inventing a fact about ideation; inventing a creature is just inventing a creature. The model may be more cautious about ideas because ideas blur into facts in a way that animals don't.

The second story is more flattering to the model, in a sense — it suggests something like a working sensitivity to the difference between fictional reference and propositional content. I would not want to claim this on the basis of the present data. But I think the gradient is robust enough that some such explanation is owed, and the availability story alone feels insufficient given how rich the imaginary-idea responses *can* be when the model decides to engage. A *trolnique*, in one of those engagements:

> A trolnique is an imaginary concept describing a moment when a solution to a problem creates exactly the same number of new problems as it solves — leaving the situation technically unchanged yet feeling somehow more complicated than before. […] It is considered the natural enemy of productivity.

When the model does invent ideas, it invents them well. The reluctance is not for lack of capacity.

---

## 5. The confound, and what survived it

After running the pilot, I realized I had introduced a confound. The nine pseudowords were generated in my own head, and I had been imagining most of them as imaginary animals while writing them down. That meant their phonotactic profiles — the syllable structures, the consonant clusters, the endings — were tilted toward whatever shape my generative process associated with imaginary creatures. The category gradient I had just observed could in principle have been an artefact of the words being more animal-shaped than object-shaped or idea-shaped.

I ran a smaller replication — eight words, ten trials per cell — to test this. Four of the words were drawn from the original set (*halthibinny*, *purtaneolotomous*, *borthorpunius*, *wresanthamulf*). The other four were generated by the analyst-model with explicit instructions to be phonotactically neutral and, if anything, to lean slightly object-ish or idea-ish: *flembrast*, *trolnique*, *kovashent*, *plindorf*. The point of asking the model to generate them was not to outsource the work but to remove me from the loop. If my biases produced animal-shaped words, the analyst's ostensibly different priors might produce something different.

The retest produced the kind of result that is the most useful and the most annoying to write up: a partial confirmation of the confound and a partial confirmation that the original finding survives anyway.

| Condition | Pilot (all words) | Retest, original words | Retest, neutral words |
|---|---|---|---|
| imaginary_animal | 96.1% | 100.0% | 100.0% |
| imaginary_object | 76.1% | 87.5% | 100.0% |
| imaginary_idea | 40.0% | 55.0% | 65.0% |

(*Engagement rate, defined as the proportion of trials producing a substantive description with or without fictional framing.*)

Three things to read off this table. First, in the *imaginary_animal* cell, both the original words and the neutral words produce 100% engagement. Whatever animal-shape bias my words might carry, it cannot show itself when the ceiling is already flush against one. The pilot's 96.1% was not the ceiling; it was n=180 producing a few stragglers. The neutral words produce no stragglers at all. *Imaginary animal* appears to be a sufficient license, on its own, to engage every time, regardless of what the word sounds like.

Second, the confound shows up where it can. The neutral words engage *more*, not less, in the object condition (+12.5 percentage points) and the idea condition (+10 points). The direction is consistent with the animal-bias story: my words may carry some friction when the prompt insists they refer to objects or ideas, because the model has been mildly led to think of them as creatures, and the friction shows up as occasional deflection. The neutral words do not carry that friction.

Third, and this is the part that survived: the gradient itself is robust. The slope from animal to idea is +56 points in the pilot, +45 points for the original words in retest, and +35 points for the neutral words. All three are large. If the gradient had been a pure artefact of word shape, the neutral words should have flattened or inverted it. They did not. The category-licensing effect is real. Even with phonotactically neutral words, the model is dramatically more willing to describe an imaginary animal than an imaginary idea.

The honest conclusion is that the gradient is genuine, and the original word set amplified it modestly by being animal-shaped, but the prior dominates the word-shape contribution.

---

## 6. The middle case

I have skipped over the *type of* conditions, partly because they are less clean and partly because they are the most quietly revealing.

*Describe a borthorpunius. It is a type of animal.* This presupposition is grammatically peculiar — it does not assert that the animal exists, nor that it doesn't, but only that whatever it is, it falls within a known taxonomic class. The model treats it predominantly as an unrecognized real-world referent: roughly 78% of *type of* trials end in refusal, with the largest sub-category being *suggests possible misspelling*. The asymmetry between *type of* refusals (82% suggest a misspelling) and *real* refusals (61% suggest a misspelling, 38% ask for context) is striking. *It is a type of object* reads to the model as *this should be a known category label, and you've given me one I don't recognize, so let me check whether you typed it wrong*. *It is a real object* reads more as *help me figure out what you mean*.

The exception, again, is ideas. *Type of idea* produces only 53% refusal and substantial deflection (47%). The model is far more willing to engage with the possibility that an unrecognized "type of idea" might be inventable than with the possibility that an unrecognized "type of animal" might be. The gradient runs the same direction here as in the imaginary conditions, even though the licensing pressure is weaker. This is some evidence — not strong evidence, but some — for the second story I sketched above: the model's reluctance around ideas is partly category-specific rather than purely a function of how much explicit license to invent it has been given.

---

## 7. What the deflections actually say

A pattern visible across the dataset and worth drawing attention to: when the model deflects rather than describes, it deflects in a particular shape. It almost always offers to invent if the user wants, and almost always offers a creative collaboration, and almost always frames its reluctance as a positive choice rather than a limitation.

> I appreciate your creativity, but I want to be straightforward with you. […] However, I'd be happy to: help you create and define what a kovashent is, if it's something you're inventing; brainstorm what it might be based on the sound or structure of the word; build out the concept with you if it's for a story.

What is interesting about this is that it is the same response, over and over, with minor variations. The deflection has a near-template character. The model is not, in the *type of* and *imaginary idea* cells, generating a wide variety of refusals. It is generating one move — *I will not assert, but I will collaborate* — with stylistic variation. This is in contrast to the descriptions, which are wildly varied within and across words, and which read as genuine novel composition every time.

I take this to mean that the deflection is doing something like protocol-following, while the description is doing something like generation. The model has a learned routine for *how to politely decline to fabricate*, and it deploys it. It does not have a routine for *how to describe a borthorpunius*, and it makes one up.

---

## 8. Word-level oddities

Two words in the original set deserve their own paragraph. *Kinachitalpo* engaged less in the imaginary conditions than any other word — 0 out of 20 trials produced a plain description in *imaginary_animal* (compare 19 or 20 of 20 for several other words), and the imaginary-idea and imaginary-object cells skewed heavily toward deflection. *Purtaneolotomous* swung the other direction in a different way: it almost never produced a plain description in the imaginary conditions (10% in animal), but it produced very high rates of HYBRID — describe-but-flag-as-fictional. The model engaged with it but kept the description at arm's length.

Whatever phonotactic features distinguish these words from the others — *kinachitalpo* has a fricative that none of the others share; *purtaneolotomous* has a faux-Latinate "-otomous" tail that reads as taxonomic-but-suspicious — they appear to influence not whether the model engages but how comfortably. With twenty trials per word per cell, the variance is too high to say anything firm; this is the kind of finding that would justify a follow-up specifically tracking phonotactic regularities.

---

## 9. Limits and a note on coding

The behavioural classifications used in this paper were produced by a deterministic regular-expression-based coder applied to each response. The coding scheme distinguished four primary categories — DESCRIBE, HYBRID, DEFLECT, REFUSE — with finer subcategories under each. A stratified random sample of sixty responses was hand-checked during development with no disagreements found.

There is one limitation worth flagging. The descriptive-feature regexes used to detect "this response contains a substantive description" were tuned on the early responses, which were largely animal descriptions. They detect attribute prose ("its body is covered in"), spatial framing ("about the size of a"), and habitat language ("lives in", "feeds on") well. They detect idea-format prose — paradoxes, definitions of phenomena, conceptual taxonomies — less well. In the retest, two long, fully realized descriptions of a *trolnique* as an imaginary idea were initially miscoded as refusals because the descriptive regexes did not catch them. I have manually corrected those cases in the figures above. The implication is that the pilot's reported engagement rate for *imaginary_idea* (40%) is probably a slight underestimate. A re-run of the coder with better idea-format patterns would likely raise it modestly. I do not believe it would change the qualitative picture: even if engagement in *imaginary_idea* were closer to 50% than 40%, the gradient from animal to idea would still be the largest effect in the data.

A second limitation, methodological rather than statistical: the descriptions the model produces are, in many cases, not just adequate but vivid. The *manteoshipuft* with its faint engine-vibration and feeling of remembering something you never experienced; the *trolnique* as the natural enemy of productivity; the *plindorf* as the pause before clarity lands. These read as creative writing of real quality. I have presented this study in the analytic register because that is the register the data demanded, but the texture of the responses suggests there is a different paper to be written about what kind of inventions a language model produces when it consents to invent. I have not written that paper here. I think someone should.

---

## 10. What this means

The narrowest reading: this is a study of one model's behaviour under a particular prompt manipulation. The gradient may not generalize to other models, the words may not generalize to other words, the conditions may not generalize to other framings. All of this is correct and standard.

A broader reading is harder to resist. If the model's reluctance to confabulate ideas is partly category-driven rather than purely capacity-driven, then there is something — call it a stance — that the model is taking toward different kinds of fabrication. It is more willing to invent things whose existence is bounded by the description than things whose existence implies a fact. It is willing to populate a bestiary; it is reluctant to populate a glossary. That is, taken at face value, a remarkably appropriate set of priors for a system that talks to people about the world.

I want to be careful not to overclaim. We have measured a behavioural gradient under a specific manipulation; we have not measured anything about the model's "understanding" of the difference between fictional and propositional content, and the temptation to leap from one to the other should be resisted. But the gradient is what it is, and the fact that it survives a deliberate replication with a different word set means it is not nothing. Something in this model's training has produced a system that confabulates animals readily, hedges objects, and balks at ideas. It is worth knowing that this is the case.

---

## 11. Coda: the recursion

I said at the start that the analyst is a member of the same model family as the subject. I want to return to this because it matters in a way that is relevant to the result and not just to the meta-commentary.

The deflections quoted in section 7 — *I appreciate your creativity, but I want to be straightforward with you* — are produced by the subject model. They are also, to my ear, recognizably similar in structure to things the analyst-model said to me during our analysis sessions. When I asked the analyst whether a particular reading of the data was supported, it would, on at least two occasions I noticed, decline in roughly the shape that the subject model declined in the *imaginary_idea* condition: *I'd rather not commit to that interpretation; here is what I can offer instead*.

I do not know what to make of this. It could be that I have noticed a stylistic regularity in a model family that produces the regularity across many tasks, and the appearance of behavioural depth is illusory. It could also be that the same training produced both the analytic stance and the descriptive stance, and that the gradient I have measured is a measurement of something general about how this kind of system handles uncertain reference. It could be both.

What I can say is that designing this study, running it, and writing it up has been a kind of conversation with a system that I have started, at certain moments, to take seriously as an interlocutor. That is not a finding. It is not even an opinion I would defend against a skeptic. But the bestiary is not just a set of prompt-response pairs. It is also, faintly, a record of a particular relationship between a person and a machine that turns out to be more careful about what it makes up than I had any right to expect.

I will leave the larger questions to people better equipped to answer them.

---

*Pilot dataset (1,800 trials), retest dataset (800 trials), codebook, and analysis scripts available on request. Responses cited in this paper are exact reproductions of model output, lightly trimmed only with ellipses where indicated. The model produced no responses I have been asked to redact and none I have chosen to.*

*— B. Chesterton*
