---
name: create-beautiful-slideshows
description: Generate reveal.js slideshows from lesson plans using the Markdown → Pandoc → reveal.js pipeline.
---

# Skill: Create Beautiful Slideshows

**Pipeline:** Markdown → Pandoc → reveal.js  
**Agent writes:** Pure Pandoc Markdown only — no HTML, no Typst, no raw CSS  
**Lua filters handle:** Audio autoplay, YouTube embeds  
**CSS handles:** Styling, shields, fragments, responsive sizing  

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

**Do NOT install these unless explicitly needed.** The current filter stack (youtube-embed.lua + audio-autoplay.lua + slide-helper.lua) covers all slide needs. New filters should only be added when a specific feature cannot be expressed in Markdown.

### Files

| File | Purpose | Source / Created by |
|------|---------|---------------------|
| `slides.md` | The presentation source | Agent — write to `output/{subfolder}/slides/` |
| `index.html` | Generated slideshow (do not hand-edit) | Pandoc generates this |
| `slides-pandoc.css` | Custom styles (shields, fragments, title row, CEFR badges) | Copy from `scripts/slides-pandoc.css` |
| `audio-autoplay.lua` | Injects `<audio data-autoplay>` from heading attrs | Copy from `scripts/audio-autoplay.lua` |
| `youtube-embed.lua` | Converts `::: {.youtube}` to iframe | Copy from `scripts/youtube-embed.lua` |
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
Copy-Item "scripts/slides-header.html" "output/{subfolder}/slides/"
```

### Build Command (Pandoc 3.9+)

Run from the `slides/` directory. This uses `--syntax-highlighting=idiomatic` for native reveal.js highlight.js support (Pandoc 3.9+):

```powershell
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
  -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
  -V theme=black \
  -V width=1280 -V height=720 -V margin=0.04 \
  --css="slides-pandoc.css" \
  --include-in-header="slides-header.html" \
  --lua-filter="youtube-embed.lua" \
  --lua-filter="audio-autoplay.lua" \
  --syntax-highlighting=idiomatic
```

### Serve Locally (Auto-Open Browser)

After building, serve the slides and open the browser automatically. Use the `background_process` tool to start the server (it stays visible in the sidebar and is cleaned up when the session ends):

```powershell
# Start the HTTP server as a tracked background process
background_process start --command "python -m http.server 8000" --workdir "output/{subfolder}/slides/"
# Then open the browser (user: open http://localhost:8000/)
```

If the background_process tool is not available, use the convenience script (auto-opens browser):

```powershell
python scripts/serve_slides.py output/{subfolder}/slides/
```

Or a manual PowerShell approach:

```powershell
# From the slides/ directory:
$server = Start-Job -ScriptBlock { python -m http.server 8000 }
Start-Sleep -Seconds 1
Start-Process "http://localhost:8000/"
```

**Important:** Stop the server when done with `Stop-Job $server` or by closing the terminal. Leaving background HTTP servers running will block port 8000 for the next session.

YouTube iframes require HTTP (not `file://`) due to YouTube's referrer policy.

---

## Phase 0: Red/Green Testing (First Run the Tests)

Before ANY slide-writing work, run the existing test suite to establish a green baseline:

```powershell
# Step 0 — establish green baseline
python -m pytest tests/ -v --tb=short
```

This verifies:
- All previously built slideshows still have valid HTML structure
- The validation script passes its own unit tests
- No infrastructure regressions (Lua filters, CSS, Pandoc invocation)

**If tests fail:** Investigate and fix before proceeding. A failing baseline means the pipeline itself is broken.

After writing slides and building, re-run tests to confirm nothing regressed:

```powershell
# After build — confirm no regressions
python -m pytest tests/ -v --tb=short

# Run pre-build validation against your slides
python scripts/validate_slides.py output/{subfolder}/slides/slides.md
```

---

## Phase 1: Blueprint (Stage-to-Slide Mapping)

Before writing a single line of Markdown, create a **stage-to-slide mapping table**. This forces you to plan every slide's pedagogical purpose, reveal.js feature, and cognitive principle before writing.

Example blueprint table (from the M3 Speaking Gender Roles slides):

| Slide ID | Stage/Name | Slide Type | Feature | Principle |
|----------|-----------|------------|---------|-----------|
| slide-splash | Splash | Image only, empty heading | Full-bleed bg image | Coherence — no text primes topic visually |
| slide-title | Title | Logo + title-row + shield + CTA | Text overlay on same bg | Signaling — topic and level at a glance |
| slide-objective | Objective | 3 static "I can" bullets | No fragments | Pretraining — preview outcomes |
| slide-lead-in | Lead-in | Discussion Q on dark bg | No text shields on solid bg | Multimedia — image evokes |
| slide-video | Video Input | YouTube fenced div | `::: {.youtube}` | Segmenting — video as source |
| slide-ccq-1..5 | CCQs | Q + fragment answer | `fragment.answer-reveal` | Temporal Contiguity — Q then reveal |
| slide-model-opinion | Model Answer | Audio + quote + fragment analysis | `data-audio-src` + fragment | Modality — hear then analyze |
| slide-prepare | Your Turn | Table + instructions | Pipe table | Scaffolding — structure |
| slide-summary | Summary | 3 "I can" checkmarks | Static | Signaling — consolidate |
| slide-end | End | Topic + badge on `#2c3e50` | Solid bg | Coherence — clean close |

**Rules for every slide:**
1. Every slide has a **unique slide ID** (stable across edits)
2. Every content slide has `::: notes` with timing and interaction
3. Transitions (phase changes) use **red bg** (`data-background-color="#c0392b"`)
4. Image backgrounds get **text shields** (`.shield`, `.title-row`)
5. Solid backgrounds get **plain Markdown** (no shields needed)
6. Fragment answers use `:::{.fragment .answer-reveal}` for yellow-bold reveals

Reference blueprints in `.kilo/plans/*-blueprint.md` for real examples.

---

## Phase 2: Setup the slides/ Directory

```powershell
# Create directories
New-Item -ItemType Directory -Path "output/{subfolder}/slides/assets" -Force | Out-Null

# Copy infrastructure files (CSS + Lua filters)
Copy-Item "scripts/slides-pandoc.css","scripts/youtube-embed.lua","scripts/audio-autoplay.lua" -Destination "output/{subfolder}/slides/"

# Copy logo
Copy-Item "templates/ACT.png" "output/{subfolder}/slides/assets/logo.png"

# Copy splash/background image (source varies)
Copy-Item "{SOURCE_PATH}" "output/{subfolder}/slides/assets/splash.webp"

# Copy slides-header.html (shared meta referrer tag — never write HTML by hand)
Copy-Item "scripts/slides-header.html" "output/{subfolder}/slides/"
```

---

## Phase 3: Write slides.md (Pandoc Markdown Patterns)

### 3.1 Slide breaks

Every `#` heading creates a horizontal slide. No vertical nesting.

```markdown
# Slide Title

Content here.

# Next Slide

More content.
```

### 3.2 Heading attributes

Attributes on `#` headings propagate to the `<section>` element:

```markdown
# Slide Title {data-background-color="#1a1a2e"}

# Splash {data-background-image="assets/splash.webp" data-background-size="cover"}
```

Known attributes: `data-background-color`, `data-background-image`, `data-background-size`, `data-background-iframe`, `data-background-interactive`, `data-timer`, `data-audio-src`, `data-transition`, `data-auto-animate`, `data-auto-animate-id`.

### 3.3 Empty headings (splash/end slides)

Use `# ` with only attributes — empty `<h1>` hidden by CSS:

```markdown
#  {data-background-image="assets/bg.jpg" data-background-size="cover"}
```

### 3.4 Fenced divs (classed containers)

`::: {.class}` creates `<div class="class">`. Used for shields, YouTube, fragments:

```markdown
::: {.title-row}
[**Title text**]{.slide-title}
:::
```

### 3.5 Bracketed spans (inline classes)

`[text]{.class}` creates `<span class="class">text</span>`:

```markdown
[**Bold text**]{.cta-text}
```

**Inline CSS on spans** — for auto-animate morphing and highlighting:

```markdown
[friends at]{data-id=t1} [school, so]{data-id=t2 style="border: 2px solid #ffdd00; border-radius: 4px; padding: 2px 8px;"}
```

### 3.6 Fragments (clickthrough reveals)

Generic fragments (for content steps, template blanks):

```markdown
::: {.fragment}
Content revealed on click.
:::
```

Answer reveals (yellow bold on reveal):

```markdown
::: {.fragment .answer-reveal}
**Answer** — source or explanation
:::
```

### 3.7 Speaker notes

Every content slide MUST have speaker notes:

```markdown
::: notes
Hidden notes visible in presenter view (press S).
Time: 2 min. Interaction: T-Ss.
:::
```

### 3.8 Line breaks within paragraphs

Two trailing spaces force a line break:

```markdown
"Phrase one..."  
"Phrase two..."  
```

### 3.9 Markdown tables (pipe tables)

Use for structure slides, discourse markers, checklists:

```markdown
| Part | Content |
|------|---------|
| **Opinion** | Your position |
| **Reason 1** | Argument + evidence |
```

---

## Phase 4: Advanced Patterns (from Good Outputs)

### Pattern A: Splash + Title (two-slide opener)

Always opens with TWO slides: a text-free splash and a separate title slide. Both use the **same** background image.

```markdown
#  {data-background-image="assets/splash.webp" data-background-size="cover"}

#  {data-background-image="assets/splash.webp" data-background-size="cover" data-background-color="#1a1a2e"}

![](assets/logo.png){.title-logo}

::: {.title-row}
[**Presentation Title**]{.slide-title} [B2]{.cefr-badge}
:::

::: {.shield}
Subtitle text — e.g. "Unit 3 — Business · B1"
:::

::: {.shield}
[**Call to action**]{.cta-text}
:::

::: notes
Welcome students. Time: 1 min. T-Ss.
:::
```

**Rules:**
- Slide 1 (splash): empty heading `# ` with `data-background-image` only — no text, no logo, no shields
- Slide 2 (title): same background image, plus logo `.title-logo`, `.title-row`, `.shield`, `.cta-text`
- CEFR badge in title row: `[B2]{.cefr-badge}` (optional)

### Pattern B: Audio autoplay with model answer + fragment analysis

Use for listening exercises and model answers. The audio plays when the slide enters. A fragment reveals analysis.

```markdown
# Jack's Opinion {data-audio-src="assets/jack-opinion.mp3"}

> "I think feminism is still really important today."

::: {.fragment .answer-reveal}
**His view:** Feminism is still relevant.

**B2 feature:** He uses **concession** — acknowledges the other side.
:::

::: notes
Ask: "What does Jack believe?" Click to reveal. Time: 1 min.
:::
```

### Pattern C: YouTube embed (responsive, in-slide)

```markdown
# Andrew Tate: News Report

::: {.youtube}
l-lbCHM5rig
:::

::: notes
Play the video. Ask: "What did you notice?" Time: 3 min. T-Ss.
:::
```

The `youtube-embed.lua` filter converts this to a responsive 16:9 iframe.

### Pattern D: Auto-animate pair (morph between two slides)

Use `data-auto-animate` with `data-auto-animate-id` for smooth morphing transitions between two slides.

**Entry slide:**
```markdown
#  {data-auto-animate="true" data-auto-animate-id="punct-demo"}

[friends at]{data-id=t1} [school , so]{data-id=t2}

[Spaces go **after** punctuation.]{style="visibility: hidden;"}
```

**Reveal slide:**
```markdown
#  {data-auto-animate="true" data-auto-animate-id="punct-demo"}

[friends at]{data-id=t1} [school, so]{data-id=t2 style="border: 2px solid #ffdd00; border-radius: 4px; padding: 2px 8px;"}

[Spaces go **after** punctuation.]{style="color: #ffdd00;"}
```

**Rules:**
- Both slides must have the same `data-auto-animate-id`
- `data-auto-animate="true"` on both headings
- Use `data-id` on spans to pair elements across slides
- `visibility: hidden` on entry keeps space without showing content
- The paired IDs count must be exactly 2 (verified by `test_slide_structure.py::TestAutoAnimatePairs`)

### Pattern E: CCQ / Comprehension with fragment answer reveal

```markdown
# Quick Check 1

What percentage of Gen Z men believe a wife should obey her husband?

::: {.fragment .answer-reveal}
**31%** of Gen Z men (and **18%** of Gen Z women) — Kings College study
:::

::: notes
Pause for pair discussion before revealing. Time: 1 min.
:::
```

### Pattern F: Transition slides (phase change)

Red background signals a shift between lesson phases:

```markdown
# Let's Review {data-background-color="#c0392b"}

::: notes
Phase transition. Time: 0.5 min.
:::
```

### Pattern G: Content slide with solid background (no image)

Plain Markdown — no shields needed since black theme makes text readable:

```markdown
# Today's Objectives

I can state a clear opinion.

I can support my opinion with reasons and evidence.

I can use discourse markers to structure my monolog.

::: notes
Read through. "By the end of today..." Time: 1 min.
:::
```

### Pattern H: Timer slide (countdown)

```markdown
# Your Turn: Rewrite

Read your feedback. Then rewrite your article.

You have **30 minutes**.

::: notes
Hand out printed feedback. Time: 30 min. Ss individual.
:::
```

For a visual countdown timer, add `data-timer` to the heading (estimated seconds):

```markdown
# Writing Task {data-timer="1260"}

PET prompt + requirements.

::: notes
21 minutes for writing. Time: 21 min. Ss individual.
:::
```

### Pattern I: Summary slide (matches objectives)

The summary mirrors the objectives slide with checkmarks:

```markdown
# I can...

I can state a clear opinion. ✓

I can support my opinion with reasons and evidence. ✓

I can use discourse markers to structure my monolog. ✓

::: notes
Self-assessment. Which was easiest? Hardest? Time: 1 min. T-Ss.
:::
```

### Pattern J: End slide (solid color background)

```markdown
#  {data-background-color="#2c3e50"}

**Topic Name** **B2**

::: notes
Thank students. Preview next lesson. Time: 0.5 min.
:::
```

---

## Phase 4: Validate Before Building

Run the validation script BEFORE pandoc:

```powershell
python scripts/validate_slides.py output/{subfolder}/slides/slides.md
```

The script checks:
- **Speaker notes** — every content slide has `::: notes`
- **Fenced div balance** — all opened `:::` blocks have matching closing `:::`
- **Raw HTML** — no forbidden `<div>`, `<span>`, etc. (must use Pandoc Markdown)
- **Missing files** — audio/image files referenced in attributes actually exist
- **YouTube IDs** — video IDs in `::: {.youtube}` look valid (8-15 alphanumeric chars)
- **Horizontal rules** — warns about `---` separators that may cause unintended slide breaks

**Exit codes:**
- `0` — all checks pass, ready to build
- `1` — warnings only (non-blocking, but review suggestions)
- `2` — errors found (fix before building)

---

## Phase 5: Build

```powershell
# From the slides/ directory:
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
  -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
  -V theme=black \
  -V width=1280 -V height=720 -V margin=0.04 \
  --css="slides-pandoc.css" \
  --include-in-header="slides-header.html" \
  --lua-filter="youtube-embed.lua" \
  --lua-filter="audio-autoplay.lua"
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

- **Do not write raw HTML** — use Pandoc Markdown only (this includes HTML files like `slides-header.html` — always copy, never write)
- **Do not use `--slide-level=2`** — creates vertical slides
- **Do not use `data-background-iframe` for YouTube** — fullscreen, Error 153
- **Do not use `##` headings for slide breaks** — only `#`
- **Do not invent statistics** — source from lesson plan or transcript
- **Do not use `<!-- .element: class="fragment" -->`** — inert HTML comments
- **Do not set `opacity: 1` on fragment base classes** — breaks hidden→visible
- **Do not place multiple logo files in assets/** — one `assets/logo.png`
- **Do not use `---` to separate slides** — use `# ` headings only
- **Do not skip the blueprint phase** — always create stage-to-slide mapping first

---

## Workflow Summary

```
1. Run existing tests (green baseline)
2. Create stage-to-slide mapping blueprint
3. Set up slides/ directory (assets, CSS, Lua, header)
4. Write slides.md (pure Pandoc Markdown)
5. Validate: python scripts/validate_slides.py output/{subfolder}/slides/slides.md
6. Build: pandoc slides.md ... (from slides/ directory)
7. Re-test: python -m pytest tests/ -v --tb=short
8. Serve: background_process start --command "python -m http.server 8000" --workdir "output/{subfolder}/slides/"
9. Open browser at http://localhost:8000/ and review (see Phase 7 checklist)
10. Stop the background server when done
11. Deploy: /git-pages {subfolder}
12. Update slideshow_url in lesson plan .md
```
