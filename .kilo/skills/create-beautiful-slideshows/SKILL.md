---
name: create-beautiful-slideshows
description: Generate reveal.js slideshows from lesson plans using the Markdown → Pandoc → reveal.js pipeline.
---

# Skill: Create Beautiful Slideshows

**Pipeline:** Markdown → Pandoc → reveal.js  
**Agent writes:** Pure Pandoc Markdown only — no HTML, no Typst, no raw CSS  
**Lua filters handle:** Audio autoplay, YouTube embeds  
**CSS handles:** Styling, shields, fragments, responsive sizing  

## CSS/HTML FILES ARE FORBIDDEN

- Do NOT read any .css, .html, or .htm file
- Do NOT edit any .css, .html, or .htm file
- slides-pandoc.css is **hash-locked** — `validate_slides.py` fails the build if it has been modified (even whitespace)
- slides-header.html is **copy-only** — its source is at `scripts/slides-header.html`; never write HTML by hand
- If a visual problem exists, the fix is ALWAYS in Pandoc Markdown or a Lua filter — NEVER in CSS
- The `style=` attribute is forbidden in slides.md — use Pandoc fenced divs, bracketed spans, or Lua filters 

---

## Purpose

Generate interactive reveal.js slideshows from lesson plan content. The agent writes pure Pandoc Markdown (`slides.md`); Pandoc converts it to HTML using `--slide-level=1` (all horizontal slides). Two Lua filters inject native reveal.js features (audio autoplay, YouTube embeds). A shared CSS file handles styling (shields, fragments, title rows, CEFR badges).

**Output:** `output/{subfolder}/slides/index.html` with `assets/` directory

## When to Use

Use this skill when:
- A lesson plan needs a reveal.js slideshow for classroom presentation
- Slides need audio autoplay (model answers, listening clips)
- Slides need YouTube embeds (video input, news clips)
- Slides need fragment reveals (CCQ answers, model answer analysis)

Do NOT use this skill when:
- A PowerPoint file is needed (use `slideshow-to-pptx` after this skill generates the HTML)
- The output needs editable text in slides (PPTX from `slideshow-to-pptx` is rasterized)

**Trigger:** `/create-beautiful-slideshow` command or when the user asks to generate slides for a lesson plan.

## Pedagogical Requirements

### Tiered Differentiation (Standard / Advanced / Elite)

Our classes contain a wide range of ability levels. **Every main task slide must offer tiered challenges** so students can self-select the level that matches their readiness.

The three-tier framework:

| Tier | Scaffolding | Description |
|------|------------|-------------|
| **Standard** | Full support | Students have the task scaffold visible (questions, prompts, word bank). Complete the task with full reference material. |
| **Advanced** | Partial support | Students do NOT have the task scaffold visible during input. They take notes while listening/reading, then answer from their notes. |
| **Elite** | Minimal support | Students complete the task from memory and understanding alone. No notes, no reference material during input or response. |

**How to apply by skill:**

- **Reading:** Standard = questions visible while reading. Advanced = read first, take notes, then answer from notes. Elite = read once, no notes, answer from understanding.
- **Listening:** Standard = questions visible before + during audio. Advanced = listen first, take notes, then answer from notes. Elite = listen once, no notes, answer from memory.
- **Speaking:** Standard = planned response with bullet points visible. Advanced = planned response from notes only. Elite = spontaneous response, no planning time.
- **Writing:** Standard = model structure + word bank visible. Advanced = outline only, write independently. Elite = no outline, write freely from topic alone.

**How to display on slides:**

Font Awesome (`fa-solid`) is available via `slides-header.html` for icons. Use it to distinguish the three tiers at a glance.

Display depends on whether the slide has an **image background** or a **plain dark background**:

**Plain dark slides (no image):** Use three paragraphs with bold tier labels and FA icons — no shields:

```markdown
### Reading Challenge

<i class="fa-solid fa-book-open"></i> **Standard** — Read the text and answer the questions on your worksheet.

<i class="fa-solid fa-pencil"></i> **Advanced** — Read the text without looking at the questions. Take notes, then answer from your notes.

<i class="fa-solid fa-star"></i> **Elite** — Read the text once. Do not take notes. Answer from memory.
```

**Image-background slides:** Use three `.shield` divs (the dark semi-transparent background ensures text readability over the image):

```markdown
### Reading Challenge

::: {.shield}
<i class="fa-solid fa-book-open"></i> **Standard** — Read the text and answer the questions on your worksheet.
:::

::: {.shield}
<i class="fa-solid fa-pencil"></i> **Advanced** — Read the text without looking at the questions. Take notes, then answer from your notes.
:::

::: {.shield}
<i class="fa-solid fa-star"></i> **Elite** — Read the text once. Do not take notes. Answer from memory.
:::
```

In both cases, the tier icon + bold label + description gives a clean, scannable layout. The `.shield` wrapper is used ONLY when there is an image background; otherwise plain paragraphs suffice.

**When differentiation is NOT needed:**
- Lead-in / warmer slides (activation only, no task)
- Transition / phase divider slides
- Summary / wrap-up slides
- Slides that display only a short stimulus (quote, image, single question for whole-class response)
- Title and objectives slides

**Key principle:** Students all receive the same input (text, video, audio, prompt). Differentiation controls the *access method* — how much scaffolding they use while processing that input. The tiers give students agency to choose their challenge level.

## Architecture

The agent writes a single `slides.md`. Pandoc converts it to reveal.js HTML using `--slide-level=1` (all horizontal slides). Two Lua filters inject native reveal.js features (audio, YouTube) via `pandoc.RawBlock()`. A CSS file handles styling.

**Golden rule:** The agent writes ONLY Markdown. Pandoc, Lua filters, and CSS handle everything else.

### Code Libraries (Reusable Lua Module)

All custom Lua filters in `scripts/` share a **common library** at `scripts/slide-helper.lua`. This is a reusable module maintained by the developer that provides validated, tested HTML generation functions. The agent never writes these functions — they are loaded at Pandoc compile time via `dofile()`.

| Function | Purpose | Used by |
|----------|---------|---------|
| `slide.youtube_iframe(id)` | Generates responsive YouTube embed HTML | `youtube-embed.lua` |
| `slide.audio_tag(src)` | Generates `<audio data-autoplay>` HTML | `audio-autoplay.lua` |
| `slide.timer_div(seconds)` | Generates countdown timer overlay | (reserved) |
| `slide.fragment_answer(content)` | Wraps content in `.fragment.answer-reveal` | (agent writes Markdown) |
| `slide.shield(content)` | Wraps content in `.shield` div | (agent writes Markdown) |
| `slide.title_row(text, badge)` | Creates `.title-row` with optional CEFR badge | (agent writes Markdown) |
| `slide.cta(text)` | Creates yellow bold CTA span | (agent writes Markdown) |
| `slide.get_attr(elem, key)` | Safely reads an attribute from a Pandoc element | Both Lua filters |
| `slide.set_background(header, img, color)` | Sets background-image/color on heading | (reserved) |
| `slide.set_auto_animate(header, id)` | Sets data-auto-animate attributes | (reserved) |

**Rule:** The Lua library (`slide-helper.lua`) is never hand-edited during slide generation. All changes to HTML output go through the library, ensuring consistency across all slideshows. To add new HTML generation capability, edit `scripts/slide-helper.lua` and write tests for it.

### Pandoc Version

This project uses **Pandoc 3.10** (released June 2026). Key features available since Pandoc 3.7:

| Feature | Since | How to use |
|---------|-------|-----------|
| **`--syntax-highlighting=idiomatic` for reveal.js** | 3.9 | Adds native highlight.js support to code blocks. Add to build command. |
| **Scroll/scrollSnap options for reveal.js** | 3.8.3 | `-V scroll=true` enables scroll-based navigation |
| **Pause syntax `. . .` in nested blocks** | 3.9 | Works in block quotes, lists, etc. |
| **`--typst-input` CLI option** | 3.10 | For Typst PDF pipeline (not slides) |
| **WASM Pandoc + PDF via Typst** | 3.9 | Browser-based pandoc at pandoc.org/app |

### Existing Lua Filter Ecosystem

The Pandoc community maintains an ecosystem of reusable Lua filters. These are **pre-existing libraries** that can replace custom code:

| Filter | Source | Purpose | Use case |
|--------|--------|---------|----------|
| `revealjs-codeblock` | [pandoc/lua-filters](https://github.com/pandoc/lua-filters) | Code block framing for reveal.js | **Superseded** by `--syntax-highlighting=idiomatic` (Pandoc 3.9+) |
| `include-files` | [pandoc/lua-filters](https://github.com/pandoc/lua-filters) | Include external markdown files | Slide template snippets |
| `include-code-files` | [pandoc/lua-filters](https://github.com/pandoc/lua-filters) | Include code from files | Code demos |
| `columns` | [pandoc-ext/columns](https://github.com/pandoc-ext/columns) | Multicolumn layout in Markdown | Side-by-side slide content |
| `diagram` | [pandoc-ext/diagram](https://github.com/pandoc-ext/diagram) | Diagrams from Mermaid/Dot/PlantUML | Charts in slides |
| `pagebreak` | [pandoc/lua-filters](https://github.com/pandoc/lua-filters) | Page breaks in PDF output | Multi-page handouts |

The `pandoc/lua-filters` repository is being retired in favor of individual repositories under the [pandoc-ext](https://github.com/pandoc-ext) organization — search GitHub topic `pandoc-filter` for 200+ available filters.

**Standard filters (always include):** youtube-embed.lua + audio-autoplay.lua + shield-block.lua + box-keywords.lua + reading-feedback.lua + autocue.lua + slide-helper.lua. Add more only when a specific feature cannot be expressed in Markdown.

### Files

| File | Purpose | Source / Created by |
|------|---------|---------------------|
| `slides.md` | The presentation source | Agent — write to `output/{subfolder}/slides/` |
| `index.html` | Generated slideshow (do not hand-edit) | Pandoc generates this |
| `slides-pandoc.css` | Custom styles (shields, fragments, title row, CEFR badges) | Copy from `scripts/slides-pandoc.css` |
| `slide-helper.lua` | Shared Lua library (required by both filters) | Copy from `scripts/slide-helper.lua` |
| `shield-block.lua` | Forces `.shield` divs to stack vertically (block display) | Copy from `scripts/shield-block.lua` |
| `audio-autoplay.lua` | Injects `<audio data-autoplay>` from heading attrs | Copy from `scripts/audio-autoplay.lua` |
| `youtube-embed.lua` | Converts `::: {.youtube}` to iframe | Copy from `scripts/youtube-embed.lua` |
| `box-keywords.lua` | Adds yellow-bordered boxes around `[key]{.box}` spans — visual reinforcer for key terms | Copy from `scripts/box-keywords.lua` |
| `reading-feedback.lua` | Auto-assigns `data-id` on table answer cells for reveal.js auto-animate; adds white row lines to tables | Copy from `scripts/reading-feedback.lua` |
| `autocue.lua` | Wraps `::: {.autocue}` divs in scrolling teleprompter container (speeds: `.a2`, `.b1`, `.b2`) | Copy from `scripts/autocue.lua` |
| `autocue.html` | CSS `@keyframes` for scrolling text animation | **Copy** from `scripts/autocue.html` if lesson has autocue slides |
| `slides-header.html` | `<meta referrer>` for YouTube embeds | **Copy** from `scripts/slides-header.html` |
| `assets/logo.png` | Institution logo on title slide | **Agent copies** from `templates/ACT.png` |
| `assets/splash.*` | Splash/background image for title slide | Source varies — see Images section below |
| `assets/` | Additional images, audio clips | Agent places here |

### Images: where they come from

| Image | Source | How |
|-------|--------|-----|
| `assets/logo.png` (title slide) | `templates/ACT.png` | `Copy-Item templates\ACT.png output\{subfolder}\slides\assets\logo.png` |
| Splash/background | Pixabay download, `inputs/{subfolder}/`, or `general-assets/` | Copy + compress via `compress_image()` |
| Pixabay images | `python scripts/pixabay_download.py --query "topic" --type image --count 3` | Downloads to `general-assets/pixabay/`; copy to `assets/` then compress |

**Logo rule:** Title slide has ONE `assets/logo.png` (ACT logo only). Cambridge and C·E·L Mathayom logos are for the Typst PDF pipeline only.

### slides-header.html

**Copy** (do not write) from `scripts/slides-header.html` — a shared one-line HTML file maintained by the developer:

```powershell
Copy-Item "scripts/slides-header.html","scripts/autocue.html" "output/{subfolder}/slides/"

Copy-Item "scripts/slides-pandoc.css","scripts/youtube-embed.lua","scripts/audio-autoplay.lua","scripts/slide-helper.lua","scripts/shield-block.lua","scripts/box-keywords.lua","scripts/reading-feedback.lua","scripts/autocue.lua" -Destination "output/{subfolder}/slides/"
```

### Build Command (Pandoc 3.9+)

Run from the `slides/` directory. This uses `--syntax-highlighting=idiomatic` for native reveal.js highlight.js support (Pandoc 3.9+):

```powershell
$slidesDir = Resolve-Path "."
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
  -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
  -V theme=black \
  -V width=1280 -V height=720 -V margin=0.04 \
  --css="slides-pandoc.css" \
  --include-in-header="slides-header.html" \
  --include-in-header="autocue.html" \
  --lua-filter="$slidesDir\autocue.lua" \
  --lua-filter="$slidesDir\reading-feedback.lua" \
  --lua-filter="$slidesDir\box-keywords.lua" \
  --lua-filter="$slidesDir\shield-block.lua" \
  --lua-filter="$slidesDir\youtube-embed.lua" \
  --lua-filter="$slidesDir\audio-autoplay.lua"
```

---

## Phase 6: Test After Building

```powershell
# Run full test suite to check structural integrity
python -m pytest tests/ -v --tb=short
```

The test suite validates:
- All `<section>` elements have IDs (including your new slides)
- Section tags are balanced (no broken HTML)
- Auto-animate IDs appear in exactly 2 slides (entry + reveal)
- No orphaned comment closers (`-->` as visible text)
- Pedagogical intent annotations are present on non-exempt slides

If you need to test just your specific slideshow:

```powershell
python -m pytest tests/test_slide_structure.py --slideshow-html "output/{subfolder}/slides/index.html" -v --tb=short
```

---

## Phase 7: Serve & Review

Start the Python HTTP server and open the browser automatically:

### Option A: Auto-serve (recommended for agent workflow)

Use the background process tool to start the server from the slides directory, then open the browser:

```powershell
background_process start --command "python -m http.server 8000" --workdir "output/{subfolder}/slides/"
# Then open http://localhost:8000/ in the browser
```

### Option B: Manual serve (run in a separate terminal)

```powershell
# From the slides/ directory:
python -m http.server 8000
# Open http://localhost:8000/ in another terminal
```

### Option C: Convenience script (auto-opens browser)

```powershell
python scripts/serve_slides.py output/{subfolder}/slides/
# Opens http://localhost:8000/ automatically. Press Ctrl+C to stop.
```

### Option D: One-liner with auto-open (PowerShell)

```powershell
# From the slides/ directory:
$j = Start-Job { python -m http.server 8000 }; Start-Sleep 1; Start-Process "http://localhost:8000/"
```

### Review Checklist

After the browser opens, manually verify:
- Splash → Title (two-slide opener, same background image)
- All slides navigate with right arrow
- Fragments reveal on click (not visible on entry)
- Audio autoplays when slide enters
- YouTube embeds load correctly (requires HTTP server, not file://)
- Text shields on image backgrounds only
- Speaking notes present in presenter view (press S)
- CEFR badge renders correctly (if used)
- Auto-animate pairs morph smoothly (if used)
- Differentiation tiers present on every main task slide — FA icons + bold labels (shields only on image-bg slides)

---

## Phase 8: Deploy

```powershell
/git-pages {subfolder}
```

After deployment, update `slideshow_url` in the lesson plan `.md` file.

---

## Reference Files

- `reference/CSS.md` — Full CSS class table and design rules (loaded when styling questions arise)
- `reference/TROUBLESHOOTING.md` — Symptom-to-fix table (loaded when errors occur)

---

## Examples

### Example 1: M3 Speaking — Gender Stereotypes and Gen Z

**Request:** "Create slides for the M3 gender stereotypes speaking lesson"

**Action taken:** Plan 23-slide stage-to-slide mapping (splash → title → objectives → lead-in → video → 5 CCQs → model answer → 3 opinion analysis slides → structure table → prepare → record → self-assessment → end). Write `slides.md` with audio autoplay for model answers, YouTube embed for Andrew Tate clip, fragment reveals for CCQs and answer analysis, pipe table for discourse markers, and `data-auto-animate` for structure comparisons. Validate, build, serve, review.

**Output:** `output/M3-SPEAKING-TBL-GENDER-ROLES/slides/index.html`

### Example 2: M3 Writing — CA Feedback

**Request:** "Slides for writing CA feedback session"

**Action taken:** Plan 12-slide mapping (splash → title → lead-in → content → common errors with auto-animate pairs → your turn → end). Use `data-auto-animate` for punctuation correction pairs, `data-timer` for writing task countdown, CEFR badge in title row.

**Output:** `output/M3-WRITING-CA-FEEDBACK/slides/index.html`

### Example 3: M2 Business — B1

**Request:** "Slides for business lesson, B1 level"

**Action taken:** Splash → title → objectives → vocabulary → listening → practice → production → summary → end. Fewer slides, simpler content, no audio or YouTube.

**Output:** `output/m2-5a-business/slides/index.html`

---

## What NOT to Do

- **Do not read any .css, .html, or .htm file** — these are generated output or shared styling, never patterns to follow
- **Do not edit any .css, .html, or .htm file** — slides-pandoc.css is hash-locked, slides-header.html is copy-only. Visual fixes go through Pandoc Markdown or Lua filters only.
- **Do not edit any .lua file without first running a Context7 search** for the Pandoc Lua filter API function you intend to use. Cite the search result in the edit rationale.
- **Do not write raw HTML** — use Pandoc Markdown only (this includes HTML files like `slides-header.html` — always copy, never write)
- **Do not write inline CSS (`style=`) in slides.md** — all styling goes through shared CSS files or Lua filters. The validation script (`validate_slides.py`) checks this and will fail the build if found.
- **Do not use `--slide-level=2`** — creates vertical slides
- **Do not use `data-background-iframe` for YouTube** — fullscreen, Error 153
- **Do not use `##` headings for slide breaks** — only `#`
- **Do not invent statistics** — source from lesson plan or transcript
- **Do not use `<!-- .element: class="fragment" -->`** — inert HTML comments
- **Do not set `opacity: 1` on fragment base classes** — breaks hidden→visible
- **Do not place multiple logo files in assets/** — one `assets/logo.png`
- **Do not use `---` to separate slides** — use `# ` headings only
- **Do not skip the blueprint phase** — always create stage-to-slide mapping first
- **Do not write teacher questions or elicitation scripts** — the teacher elicits live. Show the prompt or task only.
- **Do not reproduce full model texts on slides** — show success criteria (e.g. "Use 5 quantifiers"). The teacher and class build the model together.
- **Do not display full reading passages** — students use handouts or the board. Reference paragraph/line numbers.
- **Do not copy entire transcript entries** — show only the 2–3 relevant lines on a shielded div.
- **Do not include procedural notes (pair work, timing) on visible content** — that belongs in `::: notes`.
- **Do not use vocabulary above the target CEFR level in instructions** — task language must be comprehensible.
- **Do not exceed 25 body-text words per content slide** — split or fragment if needed.
- **Do not exceed 40 slides total for a 46-minute lesson** — cap enforced during blueprint phase.
- **Do not use more than 3 auto-animate pairs per presentation** — overuse dilutes the effect.
- **Do not present undifferentiated tasks** — every main task slide must offer the three-tier challenge (Standard / Advanced / Elite). See [Pedagogical Requirements](#pedagogical-requirements) for the framework and display pattern.

---

## Workflow Summary

```
1. Run existing tests (green baseline)
2. **Read the lesson plan** and write a bespoke design prompt — reference `.kilo/prompts/slide-design-exemplar.md` as the model
3. Create a stage-to-slide design blueprint in `.kilo/plans/` — reference `.kilo/plans/M3-WRITING-CA-FEEDBACK-blueprint.md` as the format model
4. **Plan differentiation tiers** — for each main task slide, decide Standard / Advanced / Elite access levels
5. Set up slides/ directory (assets, CSS, Lua, header)
6. Write slides.md (pure Pandoc Markdown — **no `style=` attributes**, no raw HTML) — include three-tier differentiation with FA icons (shields only for image-background slides)
7. Validate: python scripts/validate_slides.py output/{subfolder}/slides/slides.md
8. Build: pandoc slides.md ... (from slides/ directory)
9. Re-test: python -m pytest tests/ -v --tb=short
10. Serve: background_process start --command "python -m http.server 8000" --workdir "output/{subfolder}/slides/"
11. Open browser at http://localhost:8000/ and review (see Phase 7 checklist)
12. Stop the background server when done
13. Deploy: /git-pages {subfolder}
14. Update slideshow_url in lesson plan .md
```

### Before ANY .lua file edit

1. Search via Context7 for the relevant Pandoc Lua filter API function
2. If Context7 is down or doesn't have the answer, fall back to Tavily web search: `pandoc lua filter <topic>`
3. Cite the search result in the edit rationale
