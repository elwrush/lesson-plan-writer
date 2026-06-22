# Design Blueprint — M3 Columbus: Hero or Villain? (v2)

## Lesson Overview

**Class:** M3
**Topic:** Colonisation — Christopher Columbus: Hero or Villain?
**Duration:** 46 minutes
**CEFR:** B2
**Lesson shape:** R (Receptive Skills)
**Key pedagogy:** Three-tier differentiation on reading task; structured opinion framework (Opinion → Reason → Evidence) for production

---

## Stage-to-Slide Mapping

| Stage # | Stage Name | Slide Type(s) | Pattern | Slide IDs |
|---------|-----------|---------------|---------|-----------|
| — | Splash | Full-screen image, empty heading | `#  {#splash data-background-image="..."}` | splash |
| — | Title | Logo + title row + shield CTA over same image | `#  {#title ...} / ![]{.title-logo width=120} / :::{.title-row} / :::{.shield}` | title |
| — | Objectives | Grid table, single column, numbered items | `+--+ / | **1.** ... | / +--+` grid table | objectives |
| 1 | Lead-in — BTN Video | 3 gist questions in grid table → YouTube embed → bare answers as fragments | Grid table + `::: {.youtube}` + `{.fragment .answer-reveal}` | video-preview, video, video-feedback |
| — | Phase transition | Red background, centred text | `data-background-color="#c0392b"` | transition-columbus |
| 2 | Elicit Columbus | Columbus portrait image only, no text visible | `![](columbus.jpg){width=50%}` — elicitation in notes only | columbus-image |
| — | Phase transition | Red background, centred text | `data-background-color="#c0392b"` | transition-deeper |
| 3 | Pre-teach Vocabulary | 5-word table with `[word]{.box}` keywords | Pandoc pipe table, box-keywords.lua | vocab |
| — | Phase transition (implied) | No separate slide — vocabulary → reading challenge on next slide | N/A | reading-challenge |
| 4 | Reading Task Setup | 3-tier differentiation, FA icons, no shields (plain dark slide) | `<i class="fa-solid fa-book-open"></i> **Standard** — ...` | reading-challenge |
| 4 | Reading Instructions | Page reference only: "Ex 1–3 · Textbook pp. 38–39" | Single line + notes | reading-instructions |
| 4 | Reading Feedback | 5 bare comprehension answers as fragment reveals | `1. [bare answer]{.fragment .answer-reveal}` | reading-feedback |
| — | Phase transition | Red background, centred text | `data-background-color="#c0392b"` | transition-factop |
| 5 | Fact vs Opinion Intro | Definitions in `.shield` + Columbus example in `.block` | `::: {.shield}` + `::: {.block}` | fact-opinion-intro |
| 5 | Exercise 4 — Fact/Opinion | Pipe table: Statement column + Answer column (fragments) | `| Statement | Answer |` — reading-feedback.lua adds row lines | exercise-4 |
| — | Phase transition | Red background, centred text | `data-background-color="#c0392b"` | transition-structured |
| 6 | Structured Opinions | 3 `.shield` divs (Opinion → Reason → Evidence) + teacher model in `.block` | `::: {.shield}` x3 + `::: {.block}` | structured-opinions |
| 7 | Think-Pair-Share | Ex 8 Q1 + 3 `.shield` divs (Think/Pair/Share) | `::: {.shield}` x3 | think-pair-share |
| — | End | Dark background + topic + CEFR | Plain text only | end |

---

## Per-Slide Design

### splash
**Heading:** `#  {#splash data-background-image="assets/splash.jpg" data-background-size="cover"}`
**Content:** None — empty heading, full-bleed background image
**Feature:** Full-screen background image (Indigenous map of Australia)
**Principle:** Visual priming — the map signals colonisation as the topic before any text appears
**Notes:** None

### title
**Heading:** `#  {#title data-background-image="assets/splash.jpg" data-background-size="cover"}`
**Content:** Three elements:
- `![](assets/logo.png){.title-logo width=120}` — ACT logo, 120px wide
- `::: {.title-row} / [**Are colonisers really heroic?**]{.slide-title} / :::` — rhetorical question in styled row
- `::: {.shield} / [Let's read and find out.]{.cta-text} / :::` — call to action in shield
**Feature:** Logo + title-row + shield CTA
**Principle:** Topic announcement — the question invites debate without stating a dry objective
**Notes:** Rhetorical question to provoke thinking. Elicit initial ideas.

### objectives
**Heading:** `# Objectives {#objectives}`
**Content:** Single-column grid table:
```
+--------------------------------------------------------------+
| **1.** Identify different opinions about Christopher Columbus in a reading text. |
| **2.** Distinguish facts from opinions. |
| **3.** Express and support my own opinions using a structured framework. |
+--------------------------------------------------------------+
```
**Feature:** Grid table (not pipe table — avoids `<th>` yellow styling)
**Principle:** Advance organiser — students see the 3 destination points before the journey
**Notes:** Read through objectives to give students a roadmap.

### video-preview
**Heading:** `# Answer the questions as we watch. {#video-preview}`
**Content:** Single-column grid table:
```
+----------------------------------------------------------------------+
| **1.** What was the **Walk for Reconciliation**? (When? Who? How many?) |
| **2.** What events **led up to** the bridge walk? |
| **3.** Why is reconciliation still **needed today**? |
+----------------------------------------------------------------------+
```
**Feature:** Grid table with bold question stems
**Principle:** Directed listening — gist questions BEFORE the video focus attention on key ideas
**Notes:** These are gist questions — main ideas only. Play the BTN video once.

### video
**Heading:** `#  {#video}`
**Content:** `::: {.youtube} / SCW0BWf_Jys / :::`
**Feature:** YouTube embed via youtube-embed.lua
**Principle:** Minimal distraction — bare embed, no other text
**Notes:** Play BTN "Bridge Walk Anniversary" (2:27). Give 2 min pair check after.

### video-feedback
**Heading:** `# What did you find out? {#video-feedback}`
**Content:** 3 numbered items, each `{.fragment .answer-reveal}`:
```
1. [28 May 2000 · Sydney Harbour Bridge · 250,000+ · Indigenous + non-Indigenous]{.fragment .answer-reveal}
2. [1991 Reconciliation Council · 1992 Redfern Speech · Mabo decision · Native Title Act · Stolen Generations]{.fragment .answer-reveal}
3. [Still fighting for recognition, equality, justice — **"still a long way to go"**]{.fragment .answer-reveal}
```
**Feature:** Fragment reveals (lower order = bare answers)
**Principle:** Paced revelation — teacher controls the reveal sequence. Bare answers match "lower order" rule.
**Notes:** Reveal one at a time. Pause after each for discussion.

### transition-columbus
**Heading:** `# Christopher Columbus — Hero or Villain? {#transition-columbus data-background-color="#c0392b"}`
**Content:** Single heading, no body
**Feature:** Red background phase break
**Principle:** Phase boundary — video content → Columbus image/reading
**Notes:** Signal phase shift from BTN video to the reading text.

### columbus-image
**Heading:** `# Who is he? What is he famous for? {#columbus-image}`
**Content:** `![](assets/columbus.jpg){width=50%}` — image only, NO visible questions
**Feature:** Full-width portrait image
**Principle:** Teacher elicits live — the heading IS the question, no visible script needed
**Notes:** Elicit: Italian explorer, 1492, "discovered" America. Bridge to reading.

### transition-deeper
**Heading:** `# Let's look a little deeper… {#transition-deeper data-background-color="#c0392b"}`
**Content:** Single heading
**Feature:** Red background phase break
**Principle:** Phase boundary — elicitation → vocabulary/reading
**Notes:** Signals transition from quick elicitation to deeper analysis.

### vocab
**Heading:** `# Key Vocabulary {#vocab}`
**Content:** Pipe table with `[word]{.box}` on each target term:
```
| Word | Example |
| [navigator]{.box} | Columbus was a skilled navigator who could read the stars. |
| [colonisation]{.box} | The colonisation of Australia began in 1788. |
| [enslaved]{.box} | The text says Columbus enslaved people who fought against him. |
| [immoral]{.box} | Most people today agree that slavery is immoral. |
| [ruthless]{.box} | A ruthless leader will do anything to get what they want. |
```
**Feature:** Pipe table + box-keywords.lua for yellow-bordered key terms
**Principle:** Pre-teaching — students need these 5 words before they encounter them in the reading
**Notes:** Check comprehension with concept questions. Choral drill.

### reading-challenge
**Heading:** `# Reading Challenge {#reading-challenge}`
**Content:** Three paragraphs with FA icons (plain dark slide — NO shields):
```
<i class="fa-solid fa-book-open"></i> **Standard** — Read the text and answer Ex 1–3 with the questions visible while you read.

<i class="fa-solid fa-pencil"></i> **Advanced** — Read the text without looking at the questions. Take notes, then answer from your notes.

<i class="fa-solid fa-star"></i> **Elite** — Read the text once. Do not take notes. Answer from memory.
```
**Feature:** Three-tier differentiation with FA icons
**Principle:** Differentiation as agency — students self-select their challenge level
**Notes:** All students read the same text (pp. 38–39). Only the access method differs.

### reading-instructions
**Heading:** `# Exercises 1–3 {#reading-instructions}`
**Content:** `Ex 1–3 · Textbook pp. 38–39` — page reference only, no exercise duplication
**Feature:** Minimal text — just a page reference
**Principle:** No textbook duplication — exercises stay in the book
**Notes:** Ex 1: read intro. Ex 2: read both comments. Ex 3: comprehension questions. Individual → pair check → feedback.

### reading-feedback
**Heading:** `# Comprehension Check {#reading-feedback}`
**Content:** 5 numbered bare answers with fragments:
```
1. [Craig: Columbus overcame a difficult childhood to become a great navigator.]{.fragment .answer-reveal}
2. [Craig: Slavery "clearly immoral" but accepted then — "a man of his times."]{.fragment .answer-reveal}
3. [Craig: He built a bridge between Old and New Worlds — started the modern age.]{.fragment .answer-reveal}
4. [Delgado: Native Americans + Leif Erikson (500 yrs earlier) discovered America first.]{.fragment .answer-reveal}
5. [Delgado: Columbus motivated by **economics** (wealth/power), not exploration.]{.fragment .answer-reveal}
```
**Feature:** Fragment reveals — lower-order comprehension = bare answers
**Principle:** Paced revelation; lower order gets compact answers
**Notes:** Reveal one by one. Encourage text evidence for each.

### transition-factop
**Heading:** `# Fact or Opinion? {#transition-factop data-background-color="#c0392b"}`
**Content:** Single heading
**Feature:** Red background phase break
**Principle:** Phase boundary — reading comprehension → critical analysis
**Notes:** Signal shift from "what did the text say?" to "how do we know what to believe?"

### fact-opinion-intro
**Heading:** `# Fact vs. Opinion {#fact-opinion-intro}`
**Content:** Two elements:
- `**Fact** — can be proven. It is true for everyone. / **Opinion** — what someone thinks or feels. People can disagree.` — plain paragraphs (no shield — this is a plain dark slide)
- `::: {.block} / **Example with Columbus:** / **FACT:** Columbus sailed from Spain in 1492. / **OPINION:** Columbus was a brave explorer. / :::` — examples
**Feature:** Plain paragraphs for definitions, block for examples
**Principle:** Concrete before abstract — Columbus examples before textbook exercise
**Notes:** Ask: Which can we prove? Which depends on how you feel?

### exercise-4
**Heading:** `# Exercise 4 — Fact or Opinion? {#exercise-4}`
**Content:** Pipe table with Statement and Answer columns:
```
| Statement | Answer |
|-----------|--------|
| 1a. Columbus was an Italian explorer. | [**Fact**]{.fragment .answer-reveal} |
| 1b. Columbus was a brave explorer. | [**Opinion**]{.fragment .answer-reveal} |
| 2a. The Pacific is the largest ocean. | [**Fact**]{.fragment .answer-reveal} |
| 2b. The Pacific is the most difficult ocean. | [**Opinion**]{.fragment .answer-reveal} |
| 3a. Columbus brought spices from the Americas. | [**Fact**]{.fragment .answer-reveal} |
| 3b. Spices improve the taste of dishes. | [**Opinion**]{.fragment .answer-reveal} |
| 4a. Columbus was a talented sailor. | [**Opinion**]{.fragment .answer-reveal} |
| 4b. Columbus started sailing at ten. | [**Fact**]{.fragment .answer-reveal} |
```
**Feature:** Pipe table with "Answer" column → reading-feedback.lua adds white row lines + auto-animate data-ids. Each answer is a fragment.
**Principle:** Guided practice with immediate feedback. Table structure cleanly separates statement from classification.
**Notes:** Students classify each, click to reveal. Elicit justification.

### transition-structured
**Heading:** `# Building Strong Opinions {#transition-structured data-background-color="#c0392b"}`
**Content:** Single heading
**Feature:** Red background phase break
**Principle:** Phase boundary — analysis → production
**Notes:** Signal shift from identifying opinions to forming their own.

### structured-opinions
**Heading:** `# Structured Opinions {#structured-opinions}`
**Content:** 4 elements:
- `**Opinion** → *I think Columbus was/was not a hero because…*` — plain paragraph
- `**Reason** → *The main reason is…*` — plain paragraph
- `**Evidence** → *For example, when / who / what / where / how / why…*` — plain paragraph
- `::: {.block} / **Teacher model:** / I think Columbus was **not** a hero... / :::`
**Feature:** 3 plain paragraphs for the framework (no shields — plain dark slide) + block for model
**Principle:** Structured production — students need a clear scaffold before forming their own opinions
**Notes:** Students write their own structured opinion. Volunteers share.

### think-pair-share
**Heading:** `# Think. Pair. Share. {#think-pair-share}`
**Content:** 4 elements:
- `**Ex 8 Q1:** Why can a person be a hero and a villain to different people?`
- `**Think** — Write your ideas (1 min)` — plain paragraph
- `**Pair** — Discuss using the structured opinion framework (2 min)` — plain paragraph
- `**Share** — Share with the class (2 min)` — plain paragraph
**Feature:** Question + 3 plain paragraphs (no shields — plain dark slide)
**Principle:** Transfer — apply the structured opinion framework to a discussion question
**Notes:** Elicit 3–4 pairs. Wrap up: "History depends on who tells the story."

### end
**Heading:** `#  {#end}`
**Content:** `**M3 — Columbus: Hero or Villain?**` + `B2 | Receptive Skills`
**Feature:** Minimal text, dark background
**Principle:** Positive closure — signal lesson is complete
**Notes:** None

---

## Design Principles Applied

1. **One idea per slide** — No slide mixes video + questions, or vocabulary + reading task.
2. **No textbook duplication** — Exercises stay in the textbook. Slide 12 references page number only.
3. **Phase transitions** — 5 red-background slides create clear cognitive breaks.
4. **Differentiation as agency** — FA icons + Standard/Advanced/Elite signal choice, not ranking.
5. **Lower order = bare answers** — Video feedback and reading feedback use short fragments.
6. **Fragments control pace** — Teacher clicks to reveal each answer, preventing information overload.
7. **Student-facing only** — Teacher questions and timing live in `::: notes`, never on visible slides.
8. **Tables for structure** — Grid tables for lists (objectives, questions), pipe tables for columns (vocab, exercise 4).
9. **Boxes for key terms** — `box-keywords.lua` highlights the 5 target vocabulary words in yellow.
10. **Shields only on image backgrounds** — This slideshow has no image backgrounds beyond splash/title, so `.shield` is never used on content slides. Plain paragraphs suffice on dark backgrounds.

---

## Image Requirements

| Slide ID | Image | Source | Notes |
|----------|-------|--------|-------|
| splash, title | Indigenous map of Australia | `inputs/M3-COLUMBUS/1700s_1770_CookclaimsAustralia_10.jpg` | Copy to `assets/splash.jpg`, compress |
| columbus-image | Columbus portrait | Pixabay download | Copy to `assets/columbus.jpg` |

---

## Fragment Verification

| Slide ID | Fragments | Rule check |
|----------|-----------|------------|
| video-feedback | 3 items as `{.fragment .answer-reveal}` | ✓ Lower-order = bare answers |
| reading-feedback | 5 items as `{.fragment .answer-reveal}` | ✓ Lower-order = bare answers |
| exercise-4 | 8 fragment answers in table | ✓ Each answer cell is a fragment reveal |

---

## Auto-Animate Pairs

None. Fragment reveals handle all sequenced content.

---

## Differentiation

| Slide ID | Tiered? | FA Icons? | Shields? |
|----------|---------|-----------|----------|
| reading-challenge | ✓ Three tiers | ✓ fa-book-open, fa-pencil, fa-star | ✗ Plain dark slide — no shields needed |
| All other task slides | ✗ Not applicable (lead-in, transitions, vocab, guided practice, production) | N/A | N/A |
