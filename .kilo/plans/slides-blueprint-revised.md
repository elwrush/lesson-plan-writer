# Design Blueprint — Who Do We Care About Most? (Revised)

## Approach
Follows M2-WRITING-ASSIGNMENT pattern: practical article structure + useful phrases + simple checklist.
NO Band 5 criteria. NO assessment subscales.

## Stage-to-Slide Mapping

| Stage # | Stage Name | Slide Type(s) | Template Pattern | Slide IDs |
|---------|-----------|---------------|------------------|-----------|
| — | Title | Splash (image only) + Title (logo + h2 + badge + strap + CTA) | Type 1: Title Slide (M2 variant) | slide-title-splash, slide-title |
| — | Objective | 3 static "I can" bullets | Type 2: Objective Slide | slide-objective |
| 1 | Lead-in | 1 discussion Q slide (solid dark bg) | M2 lead-in style (single Q, dark bg) | slide-lead-in |
| 1→2 | Transition | Red bg, heading only | Type 3: Transition | slide-transition-review |
| 2 | Language Review | 1 inline sentence-swap slide with 4 errors + 1 slide with 3 errors | Inline Sentence-Swap Pattern (M2 slides 4-5) | slide-review-1-4, slide-review-5-7 |
| 2→3 | Transition | Red bg, heading only | Type 3: Transition | slide-transition-write |
| 3 | Task Preparation | 7 slides: prompt + structure + 2 linking-phrase slides + auto-animate demo pair + writing task | M2 pattern (structure slide → linking phrases → task) | slide-prompt, slide-structure, slide-linking-1, slide-linking-2, slide-demo-entry, slide-demo-reveal, slide-writing-task |
| — | Summary | 3 checkmark statements | Type 13: Summary | slide-summary |
| — | End | Topic + badge | Type 14: End | slide-end |

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Ref |
|----------|--------|---------|-----------|-----------|-----|
| slide-title-splash | Topic image primes non-verbally before text | Static, image only | Coherence — extraneous text removed | Full-bleed bg image with no text. If removed, students see title before emotional priming. | M2 splash |
| slide-title | Logo, topic, badge, strap, CTA visible together | Static, centered | Signaling — visual hierarchy | Logo top, h2 center with badge, strap teases topic, crimson CTA signals writing. | M2 title |
| slide-objective | 3 "I can" outcomes visible at once | Static, no fragments | Pretraining — preview outcomes upfront | Yellow numbers + white text. No fragments. | M2 objectives |
| slide-lead-in | Photo evokes emotion; single discussion Q | Static Q on dark bg | Multimedia — image evokes emotion | Single Q on screen. Teacher speaks procedure in notes. | M2 pattern |
| slide-transition-review | Red bg signals mode shift | Heading only | Segmenting | "Let's Review" — clear phase boundary. | M2 transition |
| slide-review-1-4 | 4 error sentences; click swaps to correction | Custom sentence-swap fragments | Temporal Contiguity — error and fix same position | Each sentence is a custom fragment. Original→corrected on click, same line position. | M2 review slide |
| slide-review-5-7 | 3 more error sentences | Custom sentence-swap fragments | Segmenting — split 4+3 prevents crowding | Same layout as slide 4. Visual consistency = zero cognitive load for layout. | M2 review slide |
| slide-transition-write | Red bg signals writing phase | Heading only | Segmenting | "Let's Write" — clear phase boundary. | M2 transition |
| slide-prompt | Essay question visible as reference | Static on dark bg | Signaling — reference point for stage | The essay question displayed. Teacher explains orally. | Static content |
| slide-structure | 3-part article flow diagram | Pedagogical (teal), static | Spatial Contiguity — structure diagram with labels | 3-part flow: personal hook → reasons/examples → conclusion. | M2 structure slides |
| slide-linking-1 | Opinions + Adding ideas with examples | Pedagogical (teal), static | Segmenting — 2 categories per slide | Each phrase has a context example. Examples use lesson topic vocab. | M2 linking slides |
| slide-linking-2 | Contrasting + Concluding with examples | Pedagogical (teal), static | Segmenting — 2 categories per slide | Contrasting comes before concluding (logical writing order). | M2 linking slides |
| slide-demo-entry | Two simple sentences, period has transparent border | Auto-animate entry | Temporal Contiguity — morph in place | Period wrapped in span with transparent border + data-id. | M2 coordinator demo |
| slide-demo-reveal | Period morphs to comma+coordinator | Auto-animate reveal | Temporal Contiguity — change visible same spot | Period span changes to comma+coordinator + white underline. | M2 coordinator demo |
| slide-writing-task | PET prompt + requirements checklist + timer | Static + timer | Segmenting — timer segments writing block | Side-by-side layout: PET prompt box (left) + checklist (right). Timer data-timer="1260". | M2 writing task |
| slide-summary | 3 "I can" checkmarks | Static | Signaling — review consolidates learning | Matches objective slide structurally. Checkmarks. | M2 summary |
| slide-end | Topic + badge | Static | Coherence — clean close | Topic + CEFR badge on #2c3e50. | M2 end |

## Auto-Animate Pairs

| data-auto-animate-id | Slide count | Slide IDs | Same bg? | Prev slide no AA? |
|---------------------|-------------|-----------|----------|-------------------|
| sentence-combine | 2 | slide-demo-entry, slide-demo-reveal | Yes (#1a237e) | Yes (slide-linking-2 is static) |

## Fragment Verification

| Slide ID | Fragment usage | Allowed? | Notes |
|----------|---------------|----------|-------|
| slide-review-1-4 | Custom sentence-swap × 4 | ✓ Review slide | Each swap has own data-fragment-index (1-4) |
| slide-review-5-7 | Custom sentence-swap × 3 | ✓ Review slide | Each swap has own data-fragment-index (1-3) |

## Color & Font Audit

| Slide ID | BG | Correct? | Font check | Notes |
|----------|-----|---------|------------|------|
| slide-title-splash | data-background-image | ✓ | N/A | Image only |
| slide-title | #1a1a2e + bg image | ✓ | h2=2.2em, logo=120px, strap=1em, CTA=0.9em | text-shield |
| slide-objective | #1a1a2e | ✓ | body 1em | Yellow numbers |
| slide-lead-in | #1a1a2e | ✓ | Q ≥1em | Solid dark bg |
| slide-transition-* | #c0392b | ✓ | h2 only | No notes |
| slide-review-* | #1a1a2e | ✓ | body 0.95em | All #fff/#ffdd00 |
| slide-prompt | #1a1a2e | ✓ | body 1em | Yellow prompt |
| slide-structure | #1a237e | ✓ | body 0.9em | Teal pedagogical |
| slide-linking-* | #1a237e | ✓ | body 0.9em | Teal pedagogical |
| slide-demo-* | #1a237e | ✓ | body 0.85em | Teal pedagogical |
| slide-writing-task | #1a1a2e | ✓ | body 1em, checklist 0.85em | Timer 1260s |
| slide-summary | #1a1a2e | ✓ | body 1em | Checkmarks |
| slide-end | #2c3e50 | ✓ | h2 | Topic + badge |
