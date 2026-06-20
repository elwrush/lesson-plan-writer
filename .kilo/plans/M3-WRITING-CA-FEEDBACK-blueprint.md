# Design Blueprint — M3 Writing CA: Feedback to Final Draft

## Lesson Overview

**Class:** M3-3A  
**Topic:** Writing feedback assimilation — students receive their PET Writing Feedback Reports and rewrite their articles to achieve the highest possible score.  
**Duration:** 40 minutes (5 min teach → 25 min write → 5 min wrap)  
**CEFR:** B1  
**Lesson shape:** Feedback workshop (non-standard)

---

## Stage-to-Slide Mapping

| Stage # | Stage Name | Slide Type(s) | Template Pattern | Slide IDs |
|---------|-----------|---------------|------------------|-----------|
| — | Splash | Single image, no text | Title splash pattern | slide-splash |
| — | Title | Logo + h2 + strap + CTA | Title slide pattern | slide-title |
| — | Objective | Bullet list (3 items) | Objective slide pattern | slide-objective |
| 1 | Common Errors — Punctuation | Auto-animate pair (×2): entry → reveal | Type 4: Lead-in Error auto-animate pair (reference-slideshow.html) | slide-punct-entry, slide-punct-reveal |
| 2 | Common Errors — Fragments | Auto-animate pair (×2): entry → reveal | Type 4: Lead-in Error auto-animate pair | slide-frag-entry, slide-frag-reveal |
| 3 | Your Turn: Rewrite | Transition (red) | Transition slide | slide-rewrite-transition |
| 4 | Independent Writing | Task slide with timer | Task slide pattern | slide-rewrite-task |
| — | End | "Good luck!" (dark blue-gray) | End slide | slide-end |

---

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Template Ref |
|----------|--------|---------|-----------|-----------|--------------|
| slide-splash | Prime the theme of balance/meticulousness before any info appears | Full-screen `data-background-image`, no content | **Visual anticipation** — the image of an athlete on the balance beam communicates subliminally that small adjustments lead to big results, which mirrors the feedback→rewrite process | The complete absence of text forces students to form their own connection to the image; once the title slide appears, the metaphor clicks into place. If text were present, the metaphor would be explained rather than felt. | Title splash (reference-slideshow.html) |
| slide-title | Present topic + CEFR level with evocative metaphor | Logo + h2 + strap line + CTA, all text-shielded over the same beam image | **Metaphorical framing** — the balance beam is a visual analogy for the precision needed in editing | The strap line ("One small shift can change everything") directly echoes the balance beam image, linking the physical act of balancing to the intellectual act of editing. If the image were a generic classroom photo, the metaphor would be lost. | Title slide (SKILL.md Step 3) |
| slide-objective | State 3 clear goals for the lesson | 3 bullets, dark background | **Advance organiser** — students need to know what they will achieve in the session | Three specific outcomes (receive feedback, learn 2 error types, rewrite) give students a mental roadmap. An objective slide prevents the "what are we doing today?" confusion. | Objective slide (base template) |
| slide-punct-entry | Show a real student punctuation error with invisible markers | Sentence with `border-bottom: transparent` on the space-before-comma error | **Error salience** — the erroneous spacing is highlighted by the teacher's spoken comment but visually neutral on entry | Transparent borders reserve visual space so the correction in the next slide pops without layout shift. If only the correction were shown, students wouldn't see *what* changed. | Auto-animate entry (SKILL.md auto-animate section) |
| slide-punct-reveal | Reveal the corrected punctuation with white underlines | Same sentence with `border-bottom: 2px solid #fff` on correctly placed punctuation | **Contrastive demonstration** — seeing the error and correction in the same position makes the rule immediately visible | The white underline on the *correct* placement (comma right after word, no space before) teaches the rule visually. If both versions were on separate slides, students would lose the spatial comparison. | Auto-animate reveal (SKILL.md auto-animate section) |
| slide-frag-entry | Show a real sentence fragment from the PDF | Fragment text in yellow, transparent borders on the incomplete parts | **Error salience** — the fragment is seen as it appeared in a student's essay | Using *actual* text from the PDF ("raised and taught differently...") makes the error real — students recognise their own or their classmates' writing. A made-up example would feel less urgent. | Auto-animate entry |
| slide-frag-reveal | Transform the fragment into a complete sentence | Same text elements with white borders on added subject/verb to show what was missing | **Structural transformation** — the fragment visually expands into a full sentence, showing exactly what was missing (subject + verb) | The added words appear with white underlines (via `border-bottom: 2px solid #fff`), making the repair mechanism explicit. If the fix were on a separate line, students wouldn't see how the fragment "grows." | Auto-animate reveal |
| slide-rewrite-transition | Signal the shift from teaching to independent work | Red background, single heading | **Phase change** — red signals a boundary between input and output | The red background resets attention. Students know the teaching is done and their turn is starting. | Transition (SKILL.md Four-Slide Exercise Block) |
| slide-rewrite-task | Instructions for the rewrite phase | Task number + brief instruction + timer | **Focused independent practice** — students apply feedback to their own writing | The timer (25 min) creates urgency and a clear endpoint. The instruction is minimal ("Read your feedback. Rewrite your article.") because the feedback reports themselves contain the detailed guidance. | Task slide (SKILL.md) |
| slide-end | Close the lesson | "Good luck!" + CEFR badge | **Positive closure** — ends the session on an encouraging note | The dark background signals completion. No further instruction needed. | End slide (base template) |

---

## Auto-Animate Pairs

| data-auto-animate-id | Slide count | Slide IDs | Same bg? | Prev slide no AA? |
|---------------------|-------------|-----------|----------|-------------------|
| punct-demo | 2 | slide-punct-entry, slide-punct-reveal | Yes (`#1a237e`) | Yes (slide-objective has no auto-animate) |
| frag-demo | 2 | slide-frag-entry, slide-frag-reveal | Yes (`#1a237e`) | Yes (slide-punct-reveal has auto-animate, BUT its `data-auto-animate-id` is different → OK) |

**Rule check:** Each auto-animate pair has a unique `data-auto-animate-id`. The previous slide before each pair does NOT share the same `data-auto-animate-id`. Background is identical within each pair. ✓

---

## Answer Slide Sizing

Not applicable — no exercise answers in this lesson. Students work on their own drafts with individualised feedback.

---

## Fragment Verification

No fragments used on any slide. Teaching uses auto-animate (cross-slide transitions), not within-slide fragments.

| Slide ID | Fragment usage | Allowed? | Notes |
|----------|---------------|----------|-------|
| All | None | N/A | Punctuation and fragment correction uses auto-animate between slides. |

---

## Color & Font Audit

| Slide ID | Background | Correct for type? | Font-size check | Notes |
|----------|------------|------------------|-----------------|-------|
| slide-splash | Image via `data-background-image` | Yes (splash has image only) | No text | — |
| slide-title | Image via `data-background-image` | Yes | h2=2.2em, sub=1em, CTA=0.9em | All text uses `.text-shield` |
| slide-objective | `#1a1a2e` | Yes (general content) | ≥1em | — |
| slide-punct-entry | `#1a237e` | Yes (pedagogical) | ≥1em | No fragments |
| slide-punct-reveal | `#1a237e` | Yes (pedagogical) | ≥1em | No fragments |
| slide-frag-entry | `#1a237e` | Yes (pedagogical) | ≥1em | No fragments |
| slide-frag-reveal | `#1a237e` | Yes (pedagogical) | ≥1em | No fragments |
| slide-rewrite-transition | `#c0392b` | Yes (transition) | ≥1em | — |
| slide-rewrite-task | `#1a1a2e` | Yes (task) | ≥1em | Timer on this slide |
| slide-end | `#2c3e50` | Yes (end) | ≥1em | — |

---

## Real Error Examples Harvested from M3-3A Feedback PDF

### Punctuation errors (space before comma / period / question mark)

From Fuji's writing:
> "friends at school , so if you be that how would you feel ?"

The comma has a space before it; the question mark has a space before it. Both should have no space before, one space after.

### Sentence fragments

From Elenna's feedback (explicitly called out by Teacher Ed):
> "raised and taught differently and inspired or influenced differently"

This is a dependent clause fragment with no subject and no finite verb. The teacher's suggestion is to make it a full sentence: "These teenagers were raised differently, taught differently, and inspired or influenced by different things."

I'll use this as the fragment example since it's the one explicitly labelled as a "sentence fragment" by the teacher.

---

## Pedagogical Narrative

Here is how the lesson flows, slide by slide:

**Splash → Title → Objective (3 slides, ~1 min)**

We open with a full-screen image of Suni Lee on the balance beam at the Tokyo Olympics. No text — just the image. The teacher says nothing for a moment, letting students take in the focus and concentration on the athlete's face. Then we advance to the title slide, where the same image now has text overlaid: "Feedback to Final Draft" with a strap line "One small shift can change everything." This creates the metaphor: just as a gymnast makes tiny adjustments to stay on the beam, students will make small corrections to their writing based on their feedback. The objective slide lists three clear goals: receive your feedback report, learn two common errors, rewrite your article.

**Common Errors: Punctuation (2 slides, ~1.5 min)**

The first teaching slide shows a sentence from a student's essay with punctuation errors: a space before a comma and a space before a question mark. The errors have transparent borders — the teacher can point to them but they don't visually shout. On the next click (auto-animate), the same sentence appears with white underlines under the *correctly placed* punctuation: the comma is flush against the word, with a space after it; the question mark is flush against the end of the sentence. Students see the error and its fix in the same screen position — no eye travel needed. This takes about 90 seconds.

**Common Errors: Sentence Fragments (2 slides, ~1.5 min)**

Now we show a real sentence fragment from the feedback PDF — Elenna's "raised and taught differently and inspired or influenced differently." The teacher reads it aloud, and students can hear it's incomplete: it starts with a verb and has no subject. On the next auto-animate click, the fragment transforms into a complete sentence: "These teenagers were raised differently, taught differently, and inspired or influenced by different things." The added subject and verbs appear with white underlines so students can see exactly what was missing.

**Rewrite Phase: Transition + Task (2 slides, ~25 min)**

A red transition slide signals the shift: "Your Turn: Rewrite." The teacher hands out the printed feedback reports. The task slide shows simple instructions: "Read your feedback. Then rewrite your article." A 25-minute timer starts, with blips in the final minute and a bell at the end. The teacher circulates and gives one-on-one support while students work.

**End (1 slide)**

We close with a "Good luck!" slide. The teacher collects the final drafts.

---

**This is the design blueprint. Do you approve before I build the HTML slides?**
