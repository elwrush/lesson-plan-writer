# Feature: Lesson Plan Slides Converter

## Feature Summary

Convert lesson plan JSON to Pandoc Markdown for reveal.js slide generation. `json_to_markdown.py` reads the lesson plan JSON (validated against `LessonPlan` model), extracts stages, generates slide-level Markdown with heading attributes, speaker notes via `::: notes`, fenced divs for shields/title rows, and embeds image assets. Output is `slides.md` in the lesson's output subfolder.

## User Scenarios

### User Story 1 — Convert lesson to slides (P1)
`python scripts/json_to_markdown.py output/subfolder/lesson-plan.json` → validates JSON, generates slides.md with splash slide, objective table, strategy/instruction slides per stage, answer slides, and wrap-up.

**Why this priority:** Core conversion pipeline for classroom materials.

### User Story 2 — Differentiation tiers (P2)
Main task slides include three-tier differentiation (Standard/Advanced/Elite) with Font Awesome icons (`fa-book-open`, `fa-pencil`, `fa-star`) and optional `.shield` wrapper for image-background slides.

**Why this priority:** Required by pedagogical framework in AGENTS.md.

## Technical Approach

`json_to_markdown.py` reads lesson JSON, validates fields (eventually via `LessonPlan.model_validate()`), iterates stages, generates per-stage slide content using Pandoc fenced divs `:::{.class}`, bracketed spans `[text]{.class}`, and heading attributes `{#slide-id data-background="..."}`. Differentiation follows the skill template: bare paragraphs on dark slides, stacked `.shield` divs on image backgrounds.

CSS files (`slides-pandoc.css`) are hash-locked and cannot be modified. Inline `style=` attributes are forbidden by the validation gate. All visual styling (font size, colour) is consolidated into a single `presentation-defaults.lua` filter that:

| Styling Need | Implementation |
|-------------|---------------|
| Base font size (48px) | Injects `.reveal { font-size: 48px; } .reveal h1 { font-size: 1.4em; } .reveal h2 { font-size: 1.2em; }` |
| Vocab slide enlargement (+15%) | Injects `[id^="slide-vocab-"] { font-size: 1.15em }` |
| Yellow `<span class="highlight">` text | `Span` handler sets `color: #ffd700` |
| Yellow Font Awesome icons in differentiation tiers | `RawInline` handler injects `style="color: #ffd700"` into `fa-*` class attributes |
| White text on `.white-reveal` fragments | Injects `.fragment.white-reveal.visible { color: white !important }` |

**Consolidation:** This single filter replaces four separate filters (`slide-font-size.lua`, `fa-yellow.lua`, `white-reveal.lua`, `vocab-size.lua`). Build command reduced from 9 to 6 filters. The old 4 filters remain in `scripts/` for backward compatibility but are not used in new builds.

Output: `output/{subfolder}/slides/slides.md`

## Validation Rules

| Module | Check | Rule |
|--------|-------|------|
| Input | JSON fields | All REQUIRED_FIELDS present (teacher, duration, date, topic, materials, lesson_plan) |
| Input | lesson_plan fields | shape, shape_name, cefr_level, class, stages |
| Input | Stage fields | stage_number, stage, stage_aim, procedure, time, interaction |
| Output | slide headings | Each slide starts with `# ` |
| Output | speaker notes | Each slide has `::: notes` block |
| Output | transition slide styling | Red background slides (`data-background-color="#c0392b"`) must have heading wrapped in `[text]{.highlight}` for yellow output. Body text in plain bold (white). `presentation-defaults.lua` filter handles the yellow colour. |
| Output | vocabulary slide pattern | Each vocab slide: phonemic script visible on entry (British Council `/slashes/`, yellow via `.highlight`), English word as 1st fragment `.answer-reveal` (yellow bold), context sentence as 2nd fragment `.white-reveal` (white). Font size 1.15em via `presentation-defaults.lua`. No dictionary definitions. |
| Output | auto-slide sequence | Auto-advance slides use `data-autoslide="2500" data-transition="slide-in slide-out"`. Global `autoSlide=999999` required in config (high default enables per-slide `data-autoslide` without advancing non-auto slides). |

## Test Coverage

`tests/test_json_to_markdown.py`: JSON parsing, output structure validation. (Existing tests.)

## Acceptance Criteria

| ID | Criterion | Validation Method |
|----|-----------|-------------------|
| AC1 | Valid JSON produces valid slides.md | Parse output, check headings |
| AC2 | Missing required field raises error | Error message printed, script exits 1 |
| AC3 | Differentiation tiers rendered | Output contains fa-book-open/fa-pencil/fa-star |
| AC4 | Transition slides have yellow heading, white body | `.highlight` span on heading, plain bold on body |
| AC5 | `presentation-defaults.lua` filter in build command | Build command includes `--lua-filter="./presentation-defaults.lua"` (replaces old fa-yellow, white-reveal, slide-font-size, vocab-size filters) |
| AC6 | Vocab slides: phonetic script on entry, 2 fragments (word → context) | Phonetic script is visible on entry, word is `.answer-reveal`, context is `.white-reveal` |
| AC7 | Auto-slide slides have `data-autoslide="2500"` and `data-transition` | Present on 6 sequential section tags |
| AC8 | Filter count in build command | Exactly 6 `--lua-filter` flags (presentation-defaults, reading-feedback, box-keywords, shield-block, youtube-embed, audio-autoplay, timer-inject) |

## Constraints

- Input JSON must match LessonPlan model (or be validated before conversion)
- Output must pass validate_slides.py before build
- Image asset paths relative to slides output directory
- `presentation-defaults.lua` must be copied to the slides directory and included in the build command (replaces old `slide-font-size.lua`, `fa-yellow.lua`, `white-reveal.lua`, `vocab-size.lua`)
- Red transition slides follow: yellow `.highlight` heading + white bold body
- Build command must include `-V autoSlide=999999` for auto-advance to function
- Build command runs exactly 6 Lua filters: presentation-defaults, reading-feedback, box-keywords, shield-block, youtube-embed, audio-autoplay, timer-inject
- `timer-plugin.js` and `timer-plugin.css` must be copied to the slides directory for countdown timers to work
- `blip.mp3` and `BELL.mp3` must exist in `assets/` for timer audio alerts
- Infrastructure files must be re-copied after any edit to `slide-helper.lua` or `*.lua` filters
