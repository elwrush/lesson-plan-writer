# Key Design Rules — Slides

## Slide Types

| Slide type | Background | Content |
|---|---|---|
| Splash | `#1a1a2e` + image | Full-bleed image only, no text |
| Title | `#1a1a2e` + image | Logo 120px, h2 2.2em, CEFR badge, rhetorical Q (1em), CTA (0.9em, crimson shield) |
| Objective | `#1a1a2e` | 4 "I can" statements, static, numbered |
| Transition | `#c0392b` | Heading only, no notes, no fragments |
| Pedagogical | `#1a237e`, class="pedagogical" | One concept per slide, static, teal bg |
| Vocabulary | `#1a1a2e`, class="vocab-slide" | Phonemic script → word + TTS → 1 context sentence |
| Task | `#1a1a2e` | Exercise number + brief instruction only. Students have workbook. |
| Answer | `#052e0d`, class="answer-slide" | h2 + aim-label + answer-list with a-ans.a-cor + a-why |
| Summary | `#1a1a2e` | "I can" checkmarks, matches objectives |
| End | `#2c3e50` | Topic + CEFR badge |

## Color Rules (STRICT)

- **Only `#fff` (white) and `#ffdd00` (yellow)** for ALL visible CSS properties: font color, borders, underlines, highlights
- No `#888`, `#666`, `#ddd`, `#222` gray text anywhere
- No `rgba(255,255,255,X)` with X < 1 — invisible at projection distance
- No `box-shadow` on any slide (title slide text-shield uses it internally, but don't add it explicitly)
- Answer green = `#052e0d`. Pedagogical teal = `#1a237e`. Transition red = `#c0392b`. Never `#1e7e34` or `#1a6b5a`.

## Font Size Minimums

- Body text: ≥1em
- Labels/annotations: ≥0.9em
- Title h2: 2.2em
- Logo: 120px
- Subheader: 1em
- POS markers: ≥0.6em (relative to parent)
- Never go below 0.85em on any text (0.6em POS is allowed because base is 2.2em → rendered 1.32em)

## Fragment Rules

- Fragments reserved for answer reveal and vocabulary word reveal
- NO fragments on: objectives, summaries, transitions, strategy steps, pedagogical slides
- Use `data-fragment-index` for per-click control
- Answer rows: `class="a-row fragment fade-up"` — entire row reveals on one click

## Answer Slides

- One item per slide for comprehension answers (Q visible on entry, answer reveals)
- Standard pattern: h2 → `p class="aim-label"` → `div.answer-list` → `div.a-row.fragment` → `span.a-ans.a-cor` + `span.a-why`
- Answers in yellow (`#ffdd00` via `.a-ans.a-cor`), explanations in white (`#a-why`)
- Checkmark: `<i class="fa-solid fa-check"></i>` (never unicode)
- No `a-num` span when h2 already numbers the question

## Vocabulary Slides

- Phonemic script visible on entry (Times New Roman for IPA)
- Word + TTS audio on first fragment reveal
- Audio at section level with `data-vocab-audio` (not inside fragment)
- `fragmentshown` handler checks `data-vocab-trigger` and plays audio
- Single context sentence with target word in `<span class="vocab-word">`
- IPA must follow British Council phonemic chart (`docs/british-council-phonemic-chart.md`)

## Auto-Animate

- Use only for structural transformations (empty→filled, error→correction)
- Entry: transparent borders on changed elements
- Reveal: white `#fff` or yellow `#ffdd00` borders
- Both need matching `data-auto-animate-id`
- Previous slide must NOT have `data-auto-animate`

## Transitions

- NO speaker notes
- NO fragments
- Heading only, no descriptive paragraphs
- Red background `#c0392b` with `data-background-transition="none"`

## Audio/TTS Rules

- Vocab TTS: `data-vocab-audio` at section level, `data-vocab-trigger` on word fragment
- Timer SFX: copy `blip.mp3` and `BELL.mp3` from `C:\PROJECTS\SFX\` to assets
- Never put `data-timer` on a slide with audio or video
- `RevealAudioSlideshow` must be removed from plugins when using vocab TTS
