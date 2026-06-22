# Design Blueprint — M2/4A Amazing Photographs

## Lesson Overview

**Class:** M2/4A  
**Topic:** Amazing Photographs — Reading an article about whether pictures still have power over us  
**Duration:** 46 minutes  
**CEFR:** B1  
**Lesson shape:** E — Receptive Skills (Traditional)

---

## Stage-to-Slide Mapping

| Stage # | Stage Name | Slide Type(s) | Slide IDs |
|---------|-----------|---------------|-----------|
| — | Splash | Full-screen image, no text | slide-splash |
| — | Title | Logo + h2 + CTA | slide-title |
| — | Objectives | 3 "I can..." bullets | slide-objectives |
| 1 | Lead-in — Afghan Girl | Discussion prompts | slide-afghan-girl |
| 2 | Opinions about Photography | Exercise 1 opinion pairs + Reading Strategy | slide-opinions, slide-strategy |
| 3 | Pre-teach Vocabulary | 5 keyword fragments with context sentences | slide-vocab |
| — | Transition (Reading) | Red background | slide-transition-reading |
| 4 | Reading for Viewpoint + Detail | Three-tier differentiation + comprehension questions + answers | slide-reading-task, slide-ex3-questions, slide-ex3-answers, slide-sidebar |
| — | Transition (Compound Adjectives) | Red background | slide-transition-vocab |
| 5 | Compound Adjectives | Pattern explanation + word bank + exercises + answers | slide-compound-pattern, slide-ex4, slide-ex4-answers, slide-ex5, slide-ex5-answers |
| — | Transition (Discussion) | Red background | slide-transition-discuss |
| 6 | Talking Points | Discussion questions + three-tier | slide-talking-points |
| 7 | Wrap-up | Reflection + preview | slide-wrap-up |

**Total slides: 22**

---

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Content |
|----------|--------|---------|-----------|-----------|---------|
| slide-splash | Prime the theme of photography's power before any info appears | Full-screen `data-background-image="assets/splash.jpg"`, no text | **Visual anticipation** — the Afghan Girl photo confronts students with its power before any text explains it | Complete absence of text forces students to form their own emotional response to the image. If text were present, the feeling would be explained rather than experienced. | 0 words |
| slide-title | Present topic, CEFR, and CTA with same background | Logo + title row + shield CTA | **Metaphorical framing** — the same arresting image underlines the lesson's central question: do pictures still have power? | The rhetorical question ("Have pictures lost their magic?") echoes the article title. The CTA ("Let's find out.") invites students into the inquiry. | 10 words |
| slide-objectives | State 3 clear goals | Bullet list, dark background | **Advance organiser** — students need a mental roadmap | 3 student-facing "I can" statements written in first person | 20 words |
| slide-afghan-girl | Engage with the photo personally | 3 open-ended discussion prompts | **Personal connection** — students form their own interpretation before the reading provides the author's view | Prompts move from observation ("What do you notice?") to inference ("Why did this win every prize?") to connection ("How does it make you feel?") | 15 words |
| slide-opinions | Activate opinions about photography | 4 opinion pairs (a/b choices) | **Anticipation** — students commit to a position before reading the author's view | Poll the class for each pair (show of hands). The teacher reveals results live. | 30 words |
| slide-strategy | Present reading strategy | Strategy box text | **Metacognitive framing** — students learn what to look for while reading | Short strategy summary: "The author's viewpoint is how they present a topic. Look for word choice and facts that reveal their attitude." | 15 words |
| slide-vocab-entry | Show 5 blocking words from the article | Auto-animate entry: 5 fenced divs with `data-id`, each containing bold word | **Auto-animate transformation** — words smoothly expand into their definitions on the next slide | Each word is a standalone fenced div with a unique `data-id`. No definitions yet — just the word. `vocab-animate.lua` adds `data-auto-animate` to the heading. | 5 words |
| slide-vocab-reveal | Reveal definitions for each word | Auto-animate reveal: same 5 divs with matching `data-id`, now expanded with short definitions | **Auto-animate transformation** — the entry→reveal pair lets students see the word first, then its meaning morphs into place | Matching `data-id` values pair with the entry slide. Each div now contains the word + short definition. Context sentences from article appear below as additional content. | 40 words |
| slide-transition-reading | Signal shift to reading phase | Red `#c0392b` background, single word | **Phase change** — red resets attention for a new cognitive mode | Single word: "Reading" centred on red | 1 word |
| slide-reading-task | Set up reading with tiered challenge | Three tiers with FA icons — plain paragraph (no shield, no image bg) | **Student agency** — learners choose their access level | Standard = questions visible while reading. Advanced = read first, take notes, answer from notes. Elite = read once, no notes, answer from memory. | 40 words |
| slide-ex3-questions | Display comprehension questions | Numbered list of 6 questions | **Task clarity** — students know what information to extract | The 6 questions from Exercise 3, referenced by page. Teacher plays audio 1.10. | 45 words |
| slide-ex3-answers | Check answers with class | 6 x `{.fragment .answer-reveal}` | **Guided feedback** — answers appear on teacher click so students self-check first | Each answer reveals on click, keyed to the question number. | 60 words |
| slide-sidebar | Discuss deeper text analysis | 4 open-ended questions | **Critical thinking** — students analyse author's language choices | Sidebar questions: "What does 'at our fingertips' mean? Why 'bombardment'? How does the author involve the reader?" | 20 words |
| slide-transition-vocab | Signal shift to vocab | Red background, single word | **Phase change** | "Compound Adjectives" on red | 2 words |
| slide-compound-pattern | Explain the grammar pattern | Pattern formula + word bank of 6 adjectives | **Explicit instruction** — clear rule + examples | "noun + present participle = compound adjective (heart + breaking = heartbreaking)". Word bank from Ex 4. | 15 words |
| slide-ex4 | Matching exercise | 6 definitions as numbered list | **Task focus** — students match using the article | "Match each compound adjective to its definition." Students use their books. | 10 words |
| slide-ex4-answers | Check answers | 6 x `{.fragment .answer-reveal}` | **Guided feedback** | Matches revealed on teacher click | 40 words |
| slide-ex5 | Rewrite exercise | 3 sentence prompts (item 1 is example) | **Production** — students create compound adjectives | Prompts from Ex 5 (items 2–4). Example shown: "a dish that makes my mouth water → a mouth-watering dish" | 20 words |
| slide-ex5-answers | Check rewriting | 3 x `{.fragment .answer-reveal}` | **Guided feedback** | Answers: heartwarming, record-breaking, man-eating | 10 words |
| slide-transition-discuss | Signal shift to discussion | Red background, single word | **Phase change** | "Discussion" on red | 1 word |
| slide-talking-points | Guide group discussion with tiers | Three tiers with FA icons | **Differentiated output** — students discuss at their chosen depth | Standard = plan with visible prompts. Advanced = discuss from notes. Elite = spontaneous. Questions from Ex 6. | 40 words |
| slide-wrap-up | Consolidate + preview | 2 reflection questions | **Positive closure** | Quick recall of vocab + "What's one thing you'll remember?" + preview grammar on p. 119 | 15 words |

---

## Auto-Animate Pairs

| data-auto-animate-id | Slide count | Slide IDs | Same bg? | Prev slide no AA? |
|---------------------|-------------|-----------|----------|-------------------|
| vocab-demo | 2 | slide-vocab-entry, slide-vocab-reveal | Yes (`#1a1a2e`) | Yes (transition slide has `data-auto-animate` too, but no matching `data-id` elements) |

**Mechanism:** `vocab-animate.lua` injects `data-auto-animate` into all headers. The vocab pair uses `data-id` on fenced divs. Entry slide shows 5 words as standalone terms. Reveal slide expands each word with a short definition. The `data-id` attributes match between the two slides, so each word smoothly expands in place.

---

## Fragment Verification

| Slide ID | Fragment count | Type | Notes |
|----------|---------------|------|-------|
| slide-vocab-entry | 0 | N/A | Auto-animate pair with reveal |
| slide-vocab-reveal | 0 | N/A | Auto-animate pair with entry |
| slide-ex3-answers | 6 | `{.fragment .answer-reveal}` | Answers reveal one by one |
| slide-ex4-answers | 6 | `{.fragment .answer-reveal}` | Matches reveal one by one |
| slide-ex5-answers | 3 | `{.fragment .answer-reveal}` | Answers reveal one by one |

**Rule check:** No slide mixes fragment types. All answers use `.answer-reveal` (yellow bold). All vocab items use plain `.fragment`. ✓

---

## Differentiation Tiers

| Slide ID | Tiers? | Display | Description |
|----------|--------|---------|-------------|
| slide-reading-task | ✓ | Plain paragraph (no image bg) | S = Qs visible, A = notes, E = memory |
| slide-compound-pattern | ✗ | N/A | Instructional, not a task |
| slide-ex4 | ✗ | N/A | Textbook exercise, matching task |
| slide-ex5 | ✗ | N/A | Textbook exercise, rewriting task |
| slide-talking-points | ✓ | Plain paragraph (no image bg) | S = plan with prompts, A = notes, E = spontaneous |

---

## Color & Font Audit

| Slide ID | Background | Correct for type? | Fragment-class correct? |
|----------|------------|------------------|------------------------|
| slide-splash | `data-background-image` | Yes | N/A |
| slide-title | `data-background-image` | Yes | N/A |
| slide-objectives | `#1a1a2e` (default) | Yes | N/A |
| slide-afghan-girl | `data-background-image` | Yes | N/A |
| slide-opinions | `#1a1a2e` | Yes | N/A |
| slide-strategy | `#1a1a2e` | Yes | N/A |
| slide-vocab | `#1a1a2e` | Yes | `{.fragment}` ✓ |
| slide-transition-reading | `#c0392b` | Yes | N/A |
| slide-reading-task | `#1a1a2e` | Yes | N/A |
| slide-ex3-questions | `#1a1a2e` | Yes | N/A |
| slide-ex3-answers | `#1a1a2e` | Yes | `.answer-reveal` ✓ |
| slide-sidebar | `#1a1a2e` | Yes | N/A |
| slide-transition-vocab | `#c0392b` | Yes | N/A |
| slide-compound-pattern | `#1a1a2e` | Yes | N/A |
| slide-ex4 | `#1a1a2e` | Yes | N/A |
| slide-ex4-answers | `#1a1a2e` | Yes | `.answer-reveal` ✓ |
| slide-ex5 | `#1a1a2e` | Yes | N/A |
| slide-ex5-answers | `#1a1a2e` | Yes | `.answer-reveal` ✓ |
| slide-transition-discuss | `#c0392b` | Yes | N/A |
| slide-talking-points | `#1a1a2e` | Yes | N/A |
| slide-wrap-up | `#1a1a2e` | Yes | N/A |

---

## Image Requirements

| Image | Slides | Source |
|-------|--------|--------|
| `assets/splash.jpg` | slide-splash, slide-title, slide-afghan-girl | Copy AfghanGirl.jpeg from `inputs/M2-4A READING/`, compress to 1920px max edge, save as splash.jpg |
| `assets/logo.png` | slide-title | Copy from `templates/ACT.png` |

---

## Pedagogical Narrative

**Splash → Title → Objectives (3 slides, ~1 min)**

We open full-screen with the Afghan Girl photo — no text. The teacher lets the silence hold for a moment. Then advance to the title: "Amazing Photographs" with the CTA "Let's find out." The objectives give students the roadmap.

**Lead-in: Afghan Girl Discussion (1 slide, ~3 min)**

Three prompts guide the discussion: observation (what do you notice), evaluation (why did this win every prize), and connection (how does it make you feel). The teacher elicits live.

**Opinions about Photography (2 slides, ~3 min)**

Opinion pairs from Ex 1 — class poll. Then the Reading Strategy box explains how to identify author's viewpoint.

**Pre-teach Vocabulary (1 slide, ~4 min)**

Five blocking words from the article reveal one by one on teacher click. Each shows: bold word → context sentence from article → concept check question. Uses `{.fragment}` for click-through reveals.

**Reading (4 slides, ~13 min)**

Red transition → Three-tier challenge (Standard/Advanced/Elite) → Ex 3 questions displayed → Answers revealed on click → Sidebar text-analysis questions.

**Compound Adjectives (5 slides, ~9 min)**

Red transition → Pattern explanation + word bank → Ex 4 matching (answers fragment) → Ex 5 rewriting (answers fragment).

**Discussion (2 slides, ~6 min)**

Red transition → Three-tier discussion prompts from Ex 6.

**Wrap-up (1 slide, ~3 min)**

Quick recall game + reflection + preview of grammar next lesson.

---

**This is the design blueprint. Do you approve before I write the slides?**
