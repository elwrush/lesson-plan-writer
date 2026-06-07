# Design Blueprint — Who Do We Care About Most?

## Stage-to-Slide Mapping

| Stage # | Stage Name | Slide Type(s) | Template Pattern | Slide IDs |
|---------|-----------|---------------|------------------|-----------|
| — | Title | Splash (image only) + Title (logo + h2 + badge + strap + CTA) | Type 1: Title Slide | slide-title-splash, slide-title |
| — | Objective | 4 static "I can" bullets | Type 2: Objective Slide | slide-objective |
| 1 | Lead-in | 2 discussion Q slides (solid bg, no image provided) | Type 3 variation — no image, dark bg | slide-lead-in-1, slide-lead-in-2 |
| 1→2 | Transition | Red bg, heading only | Type 3: Transition | slide-transition-review |
| 2 | Language Review | 1 inline sentence-swap slide with 4 errors | Inline Sentence-Swap Pattern (from skill) | slide-language-review |
| 2→3 | Transition | Red bg, heading only | Type 3: Transition | slide-transition-write |
| 3 | Task Preparation | Prompt slide + 2 Band 5 criteria slides + article structure slide + 2-slide auto-animate demo pair | Pedagogical (teal) for criteria/structure/demo | slide-prompt, slide-criteria-1, slide-criteria-2, slide-structure, slide-demo-entry, slide-demo-reveal |
| 3→4 | Transition | Red bg, heading only | Type 3: Transition | slide-transition-yourturn |
| 4 | Writing Task | Task instruction + timer (1260s) | Type 11: Task Slide (with timer) | slide-writing-task |
| — | Summary | 4 checkmark statements | Type 13: Summary Slide | slide-summary |
| — | End | Topic + badge | Type 14: End Slide | slide-end |

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Template Ref |
|----------|--------|---------|-----------|-----------|--------------|
| slide-title-splash | Topic image primes topic non-verbally before any text | Static — image only, no content | Coherence — extraneous text removed; image sets mood | Full-bleed bg image with no text, no notes, no shield. If removed, students see title before emotional priming. | Type 1 (splash variant) |
| slide-title | Student sees topic, level, and lesson type at a glance | Static — all visible on entry | Signaling — logo, badge, h2, strap, CTA create visual hierarchy | Logo anchors top, h2 center with badge, strap teases topic, crimson CTA signals writing. If removed, students enter cold. | Type 1: Title |
| slide-objective | Student sees what they will achieve by end of lesson | Static — no fragments | Signaling — numbered outcomes set expectations | 4 "I can" statements with yellow numbers. No fragments so learners see full picture immediately. | Type 2: Objective |
| slide-lead-in-1 | Photo on bg evokes emotional response; Q1 focuses observation | Static discussion Q on dark bg | Multimedia — image evokes emotion before discussion | Portrait photo as full-bleed bg (if available) or solid dark. Single Q on screen. Teacher speaks procedure. | Type 3 variation |
| slide-lead-in-2 | Q2 moves from observation to personal connection | Static discussion Q on dark bg | Segmenting — one Q per slide prevents overload | Second Q on separate slide keeps focus; same bg as Q1 for visual continuity. | Type 3 variation |
| slide-transition-review | Signals shift from discussion to language focus | Red bg, heading only | Segmenting — clear phase boundary | Bold red background ("Let's Review") tells students we're switching modes. No notes needed. | Type 3: Transition |
| slide-language-review | Students see 4 sentences, identify errors, teacher clicks to fix | Custom fragment sentence-swap | Temporal Contiguity — original and fix in same position | Each sentence is a custom fragment that swaps original→corrected on click. 4 items, each with own fragment-index. | Inline Sentence-Swap Pattern |
| slide-transition-write | Signals shift from language to writing | Red bg, heading only | Segmenting — clear phase boundary | Red bg "Let's Write" cues upcoming task type. | Type 3: Transition |
| slide-prompt | Students see the writing question they will answer | Static on dark bg | Signaling — reference point for whole stage | The essay question displayed clearly. Teacher explains orally. | Static content slide |
| slide-criteria-1 | Content + Comm Achievement criteria visible for reference | Pedagogical (teal), static | Signaling — assessment criteria visible during writing | Two criteria with 1-sentence descriptor each. Teal bg signals this is instruction, not task. | Type 8: Strategy (static) |
| slide-criteria-2 | Organisation + Language criteria with linking vs cohesive distinction | Pedagogical (teal), static | Signaling — learners see what Band 5 requires | Two criteria + distinction between basic linking words and sophisticated cohesive devices. | Type 8: Strategy (static) |
| slide-structure | Visual diagram of article structure (hook→body→conclusion) | Pedagogical (teal), static | Spatial Contiguity — structure diagram with labels together | Simple 3-part flow displayed vertically: personal hook → examples → wider point. If removed, learners lack mental model. | Type 8: Strategy (static) |
| slide-demo-entry | Two simple sentences, period has transparent border | Auto-animate entry | Temporal Contiguity — morph happens in place | Period wrapped in span with transparent bottom border + data-id. Data-auto-animate-id matches reveal. | Type 7: Coordinator Demo (entry) |
| slide-demo-reveal | Period morphs to comma+coordinator; combined sentence complete | Auto-animate reveal | Temporal Contiguity — change visible in same position | Period span changes to "comma + coordinator" with white underline. Teacher clicks to advance, morph animates. | Type 7: Coordinator Demo (reveal) |
| slide-transition-yourturn | Signals start of independent writing | Red bg, heading only | Segmenting — clear phase boundary | Bold red "Your Turn" signals students will now write. | Type 3: Transition |
| slide-writing-task | Shows writing prompt + timer | Task slide with timer | Segmenting — time visible; learners manage pace | data-timer="1260". Prompt text + Band 5 reminder. Full procedure in notes. | Type 11: Task Slide |
| slide-summary | Students see what they achieved | Static checkmarks | Signaling — review consolidates learning | 4 "I can" statements with checkmarks, matching objective slide structurally. | Type 13: Summary |
| slide-end | Clean closing | Static | Coherence — no extraneous elements | Topic + CEFR badge on dark bg. Clean exit. | Type 14: End |

## Auto-Animate Pairs

| data-auto-animate-id | Slide count | Slide IDs | Same bg? | Prev slide no AA? |
|---------------------|-------------|-----------|----------|-------------------|
| sentence-combine | 2 | slide-demo-entry, slide-demo-reveal | Yes (#1a237e) | Yes (slide-structure is static, no AA) |

## Answer Slide Sizing

N/A — no answer key. Writing task produces student-generated content.

## Fragment Verification

| Slide ID | Fragment usage | On allowed slide type? | Notes |
|----------|---------------|----------------------|-------|
| slide-language-review | Custom sentence-swap × 4 | Allowed — review slide | Each sentence is a custom fragment that swaps original→corrected. NOT used on objectives/transitions/summary. ✓ |

## Color & Font Audit

| Slide ID | Background | Correct for type? | Font-size check | Notes |
|----------|------------|------------------|-----------------|-------|
| slide-title-splash | data-background-image | Yes — splash | N/A — no text | Image only, no text-shield needed |
| slide-title | #1a1a2e + bg image | Yes — title | h2=2.2em, logo=120px, strap=1em, CTA=0.9em | text-shield on all text |
| slide-objective | #1a1a2e | Yes — content | h2, body 1em | All #fff/#ffdd00, no gray |
| slide-lead-in-1 | #1a1a2e | Yes — lead-in | Q text ≥1em | Solid dark bg, no image available |
| slide-lead-in-2 | #1a1a2e | Yes — lead-in | Q text ≥1em | Solid dark bg |
| slide-transition-* | #c0392b | Yes — transition | h2 only | No notes |
| slide-language-review | #1a1a2e | Yes — content | body 0.95em | All #fff/#ffdd00 |
| slide-prompt | #1a1a2e | Yes — content | body 1em | Prompt in yellow |
| slide-criteria-* | #1a237e | Yes — pedagogical | body 0.9em | Teal bg, white text |
| slide-structure | #1a237e | Yes — pedagogical | body 0.9em | Teal bg |
| slide-demo-* | #1a237e | Yes — pedagogical | body 0.85em | Teal bg, auto-animate |
| slide-writing-task | #1a1a2e | Yes — task | body 1em, instruction 0.9em | Timer visible |
| slide-summary | #1a1a2e | Yes — summary | body 1em | Static checkmarks |
| slide-end | #2c3e50 | Yes — end | h2 | Topic + badge |
