# Design Blueprint — Who Do We Care About Most? Peer Edit Workshop

## Context

Follow-up to the PET article writing lesson (`output/M3-WRITING-ASSIGNMENT/slides/`). Students have first drafts ready. This peer-edit workshop focuses on three practised editing criteria: **capitalisation, compound sentences, the hook**. All demonstration content uses **parallel topics** (piano, mountain summit) to prevent copying. Slides output to `output/M3-WRITING-EDITING/slides/`. Assets (anxiety.webp, logo.png) copied from the writing lesson's assets directory.

## Stage-to-Slide Mapping

| Stage # | Stage Name | Slide Type(s) | Template Pattern | Slide IDs |
|---------|-----------|---------------|------------------|-----------|
| — | Pre-lesson | Splash (full-bleed image, no text) | Type 1 variant: no text on slide, `data-background-image` + `data-background-color` only | slide-splash |
| — | Pre-lesson | Title (logo + topic + CEFR + strap line + CTA) | Type 1: Title Slide — logo 120px, h2 2.2em, text-shield, `justify-content: center` | slide-title |
| — | Pre-lesson | Objective (3 "I can" statements, static) | Type 2: Objective Slide — `#1a1a2e`, no fragments, yellow numbering | slide-objective |
| 1 | Lead-in — Three things we have been working on | Lead-in comparison (two-col, side-by-side) + criteria summary (three-box) | Custom dark two-col; Type 8 static for criteria | slide-leadin-compare, slide-leadin-criteria |
| 2 | Model Edit — Watch me check a draft | Pedagogical static (paragraph + marking key) | Type 8: Strategy Slide — `class="pedagogical"`, `#1a237e`, static | slide-model-edit |
| 3 | Peer Edit — Two Passes | Transition (red) + two Task slides with timers | Type 3: Transition — `#c0392b`; Type 11: Task with timer — `#1a1a2e` | slide-transition-edit, slide-pass1, slide-pass2 |
| 4 | Final Polish — Your turn to revise | Transition (red) + Task slide with timer | Type 3: Transition; Type 11: Task with timer | slide-transition-revise, slide-final-polish |
| — | Post-lesson | Summary (checkmarks, static) + End (topic + badge) | Type 13: Summary — `#1a1a2e`, static, ✓ icons; Type 14: End — `#2c3e50` | slide-summary, slide-end |

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Template Ref |
|----------|--------|---------|-----------|-----------|--------------|
| slide-splash | Student sees a full-screen portrait of a teen with a therapist — no text. The image alone primes the mental-health theme before any words appear. | Static — full-bleed background image, dark fallback. No text-shield (no text to shield). | Signaling — the portrait functions as an advance organiser, activating existing knowledge about the topic before explicit instruction begins. | A blank slide with only an image — the absence of text is the mechanism. If a title or instruction were on screen, students would start reading instead of looking at the photo and recalling their own article's topic. | Type 1 variant (splash pattern from existing slideshow) |
| slide-title | Student sees ACT logo, lesson topic with B2 badge, a strap line about editing, and a crimson CTA signalling an editing lesson. | Static, `justify-content: center`, text-shield on all text. Same background photo as splash. | Signaling — the crimson CTA visually separates the lesson-type signal from the content hook. | The crimson text-shield (`rgba(180,0,0,0.65)`) on the CTA line. Without the crimson differentiation, the CTA would blend into the strap line and lose its function as a lesson-type indicator. | Type 1 (Title Slide) |
| slide-objective | Student sees three "I can" outcomes all at once so they can self-monitor throughput the lesson. | Static — all three visible on entry, yellow numbering. No fragments. | Pretraining — presenting outcomes upfront lets students build a mental model of the lesson structure before content delivery. | Yellow numbers against white text — the colour differentiation makes each outcome scannable as distinct. If all text were the same colour, the three outcomes would blur into a paragraph that students skip. | Type 2 (Objective Slide) |
| slide-leadin-compare | Student sees Version A (weak piano paragraph) and Version B (strong piano paragraph) side by side and compares them at a glance. | Static — two-column flex layout with a thin white vertical divider. Both versions visible on entry. | Spatial Contiguity — both versions occupy adjacent columns so the eye travels horizontally, not vertically. | A thin vertical divider between equal-width columns. If the versions were on separate slides, the student would need to hold Version A in memory while viewing Version B, doubling cognitive load. | Custom dark `#1a1a2e` two-column |
| slide-leadin-criteria | After discussion, student sees the three editing criteria summarised as a reference card: Capitalisation, Compound Sentences, The Hook. | Static — three visual sections (vertical or horizontal), each with a distinctive heading and one-line explanation. | Segmenting — the three criteria are spatially separated into distinct visual zones so students mentally "park" each one. | Three labeled sections with visually distinct borders or icon colours. Without visual separation, the three categories would merge into a single instruction paragraph — students would treat "edit your draft" as one monolithic task. | Type 8 (Strategy, static) |
| slide-model-edit | Student sees a sample paragraph about reaching a mountain summit (parallel topic) and a marking key legend. Teacher thinks aloud while annotating. | Static — pedagogical teal `#1a237e`. Paragraph occupies main area; compact marking key occupies sidebar. No fragments — teacher controls pace verbally. | Modelling — showing the complete paragraph with a marking reference lets students see what the editing process produces before they attempt it themselves. | The marking key sidebar (C circle, crossed-out capital, boxed coordinator, +coord, hook?) as a persistent visual reference. If the key were omitted, students would rely on memory of the teacher's verbal explanation — by Pass 2, half the class would forget what `+coord` means. | Type 8 (Strategy Slide — teal, static) |
| slide-transition-edit | Student sees the word "Let's Edit" on a red background. No other content — the colour change alone signals the phase boundary. | Static — heading only, red `#c0392b`, no speaker notes. | Signaling — the colour change from dark/teal to red marks a clear phase boundary between teacher-led instruction and student independent work. | A single word "Let's Edit" centred on red with no descriptive paragraph. If extra text were added, students would read it while the teacher is speaking, splitting attention and slowing the transition. | Type 3 (Transition) |
| slide-pass1 | Student sees a direct instruction ("Read your partner's draft. Mark ✓ for clear parts. Mark ? for confusing parts.") and a 7-minute countdown timer. | Static — instructions visible on entry, `data-timer="420"`. No fragments. | Segmenting — the 7-minute timer segments the editing block into a clear window with a defined endpoint. | Only two marks allowed — ✓ and ?. If students had more than two marking options, they would spend time choosing which mark to use rather than reading the draft. Limiting to two marks constrains cognitive load to "clear" vs "not clear." | Type 11 (Task with timer) |
| slide-pass2 | Student sees the three-point editing checklist in three columns alongside a 13-minute countdown timer. All marks from the model edit are visible for reference. | Static — three-column flex layout, `data-timer="780"`. All three checks visible simultaneously. | Spatial Contiguity — all three checks occupy adjacent columns so the student scans horizontally between them without needing to remember which check comes next. | Three equal-width columns with clear headings and thin visual separators. If stacked vertically, the student would scroll mentally — by the time they read the third check, they would forget the first and need to re-read, wasting station time. | Type 11 (Task with timer) |
| slide-transition-revise | Same pattern as slide-transition-edit — "Let's Revise" on red. Structural symmetry reinforces the lesson rhythm. | Static — heading only, red `#c0392b`. | Signaling — the return to a red background mirrors the earlier transition, creating structural symmetry. Students learn the pattern: red = a new phase is starting. | Consistency with the first transition slide. If this transition used a different colour or layout, students would not recognise it as a phase signal and would wait for additional instructions before beginning. | Type 3 (Transition) |
| slide-final-polish | Student sees three revision reminders (mirroring the criteria from the lead-in and Pass 2) and a 13-minute countdown timer. | Static — three short points stacked vertically, `data-timer="780"`. | Coherence — the three reminders echo the same three categories from the lead-in and Pass 2, reinforcing the lesson's structure rather than introducing new concepts. | The bullet points use the same icons/cues from the lead-in criteria slide. If the final polish slide introduced new categories or a different format, students would wonder whether the editing phase has been replaced by a new task. Structural consistency across all phases reassures students they know what to do. | Type 11 (Task with timer) |
| slide-summary | Student sees three checkmark statements identical in structure to the objectives slide. This bookending reinforces what was achieved. | Static — yellow ✓ icons, no fragments. All three visible on entry. | Signaling — checkmarks visually confirm achievement and give students a sense of progress before the lesson ends. | The three statements are identical in structure to the objectives slide (same order, same categories, same "I can" framing). If the summary used different phrasing or layout, students would need to mentally map objective → outcome, adding unnecessary cognitive load at the moment they should be consolidating. | Type 13 (Summary) |
| slide-end | Clean close — topic name and B2 badge only. No extra content. | Static — `#2c3e50`, topic + badge. | Coherence — no extraneous content at the end. Students are not processing new information. | Only topic and B2 badge appear — no "thank you," no icons, no encouraging message. An empty end pattern is less distracting. If text were added, students would still be in "reading" mode when the teacher starts the closing routine. | Type 14 (End) |

## Auto-Animate Pairs

| data-auto-animate-id | Slide count | Slide IDs | Same bg? | Prev slide no AA? |
|---------------------|-------------|-----------|----------|-------------------|
| *(none)* | — | — | — | — |

**Reason:** This lesson has no auto-animate pairs. The lead-in comparison uses spatial contiguity (side by side) rather than temporal contiguity (step by step). The model edit is a single static slide because the teacher annotates live on the IWB — the slide is a reference, not a step-by-step animation. Task slides use timers only. No structural transformations (sentence combining, error → correction, strategy walk-throughs) exist in this lesson — those are the use-cases where auto-animate is the correct pedagogical feature.

## Answer Slide Sizing

| Exercise | Total items | Slides needed | Slide IDs | All ≤3 items? |
|----------|------------|---------------|-----------|---------------|
| *(none)* | 0 | 0 | — | N/A |

**Reason:** This lesson has no exercise answers to reveal. The "answers" are the edit marks students put on each other's drafts, which happen at their desks, not on screen. No answer key `.typ` file is referenced in the lesson plan JSON.

## Fragment Verification

| Slide ID | Fragment usage | On allowed slide type? | Notes |
|----------|---------------|----------------------|-------|
| slide-objective | None — static | ✅ Static objectives are correct (fragment policy forbids fragments on objectives) | All 3 outcomes visible on entry |
| slide-leadin-compare | None — static | ✅ Static lead-in comparison is correct (both versions must be visible simultaneously for comparison) | Spatial contiguity over temporal |
| slide-leadin-criteria | None — static | ✅ Static criteria summary is correct (reference card, not reveal sequence) | Reference card stays visible |
| slide-model-edit | None — static | ✅ Static model edit is correct (teacher controls pace via think-aloud, not fragments) | Marking key sidebar provides persistent reference |
| slide-pass1 | None — static | ✅ Static task slide is correct (instructions must stay visible for duration of 7-min timer) | Two-mark instruction layout |
| slide-pass2 | None — static | ✅ Static task slide is correct (checklist must stay visible for duration of 13-min timer) | Three-col reference layout |
| slide-final-polish | None — static | ✅ Static task slide is correct (reminders must stay visible for duration of 13-min timer) | Three bullet reminders |
| slide-summary | None — static | ✅ Static summary is correct (fragment policy forbids fragments on summaries) | Structural bookending with objectives |

## Color & Font Audit

| Slide ID | Background | Correct for type? | Font-size check | Notes |
|----------|------------|------------------|-----------------|-------|
| slide-splash | `#1a1a2e` + `anxiety.webp` | ✅ Splash: image with dark fallback | No text — N/A | Text-shield deliberately omitted |
| slide-title | `#1a1a2e` + `anxiety.webp` | ✅ Title: image + dark fallback, text-shield | h2: 2.2em, strap: 1em, CTA: 0.9em | Logo 120px; CEFR badge inline in h2; justify-content: center |
| slide-objective | `#1a1a2e` | ✅ Objective: dark navy | h2: 1.5em, body: 1em | 3 short outcomes, yellow numbering |
| slide-leadin-compare | `#1a1a2e` | ✅ Content: dark navy | body: 0.95em per column | Two equal columns, thin white divider; 1280px ÷ 2 = 640px per column |
| slide-leadin-criteria | `#1a1a2e` | ✅ Content: dark navy | body: 0.95em | Three sections; no pedagogical teal (this is a summary card, not strategy instruction) |
| slide-model-edit | `#1a237e` | ✅ Pedagogical: teal (`#1a237e`, NOT old `#1e7e34`) | body: 0.9em, key: 0.8em | `class="pedagogical"`; paragraph ~65% width, key ~35% width |
| slide-transition-edit | `#c0392b` | ✅ Transition: red | h2: default | Heading only, no notes |
| slide-pass1 | `#1a1a2e` | ✅ Task: dark navy | h2: 1.5em, body: 1em | `data-timer="420"` (7 min); no audio on this slide |
| slide-pass2 | `#1a1a2e` | ✅ Task: dark navy | h2: 1.5em, body: 0.9em | `data-timer="780"` (13 min); three-column layout; no audio |
| slide-transition-revise | `#c0392b` | ✅ Transition: red | h2: default | Heading only, no notes |
| slide-final-polish | `#1a1a2e` | ✅ Task: dark navy | h2: 1.5em, body: 1em | `data-timer="780"` (13 min); no audio |
| slide-summary | `#1a1a2e` | ✅ Summary: dark navy | h2: 1.5em, body: 1em | Yellow ✓ icons; matches objective structure |
| slide-end | `#2c3e50` | ✅ End: dark blue-gray | h2: default | Topic + B2 badge only |

---

## Duration Validation

Teacher-led stages (slides 0–5, 6, 9, 11–12): ~13 min. Student work stages (slides 7, 8, 10): ~33 min. **Total: 46 min** — matches lesson plan JSON.

## Setup Checklist (pre-build)

1. Copy `templates/base-slides-template.html` → `output/M3-WRITING-EDITING/slides/index.html`
2. Copy `templates/timer-plugin.js` → `output/M3-WRITING-EDITING/slides/timer-plugin.js`
3. Copy `templates/timer-plugin.css` → `output/M3-WRITING-EDITING/slides/timer-plugin.css`
4. Copy `templates/ACT.png` → `output/M3-WRITING-EDITING/slides/assets/logo.png`
5. Copy `output/M3-WRITING-ASSIGNMENT/slides/assets/anxiety.webp` → `output/M3-WRITING-EDITING/slides/assets/anxiety.webp`
6. Build all 13 `<section>` elements (with 4-line annotations per slide) in a temp file
7. Splice into template via Python splice script
8. Update `<title>` to `Who Do We Care About Most? — Peer Edit Workshop`
