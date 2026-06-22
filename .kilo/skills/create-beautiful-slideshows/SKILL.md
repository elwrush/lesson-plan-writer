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

---

## ⚠️ CORE DESIGN PRINCIPLE: SHOW, DON'T TELL

**Every slide must answer:** *"What does this slide let the student SEE that they wouldn't get from just reading the textbook or hearing the teacher say it?"*

If a slide only restates something the teacher could say or the book already shows, **delete it or redesign it**. The slide must earn its place by creating a visual or interactive experience that supports learning.

**Before writing every slide, ask:**
- What does the student SEE change/animate/appear? (Show, don't tell)
- Does this reduce cognitive load or add to it? (Strip anything non-essential)
- Could the teacher achieve the same effect by just speaking? (If yes, kill the slide)
- Is this slide for the teacher or for the student? (It should be for the student)

**Examples of showing vs telling:**

| ❌ Telling (plumber) | ✅ Showing (teacher) |
|---------------------|---------------------|
| "Exercise 3, p. 39 — Answer the 6 questions" (just an instruction) | Transition → Skill (scanning strategy with boxed example) → Task with timer → Answers fragment-revealed one by one |
| List of 5 vocab words with definitions | One word per slide. Phonemic script visible first. Word + audio appears on click. Context sentence appears on next click. Student hears and sees the word in its natural context. |
| "Here are compound adjectives" (static list) | Auto-animate pair: word parts slide together and merge into the compound adjective. The student *watches* the transformation happen. |
| A bullet list of opinions | Opinion pairs as a/b choices with live class polling — students see their peers' hands go up |
| Summary bullet points at the end | A closing image or question that sends students out thinking |

**When a slide doesn't show, it either needs to be:** (a) redesigned to have a visual/interactive element, or (b) removed and its content moved to speaker notes.

This principle overrides all technical convenience. A technically perfect slide that only tells is worse than no slide at all.

### Grammar & pronunciation: showing is non-negotiable

Grammar and pronunciation are the domains where "show, don't tell" is most critical. Students cannot *hear* clause boundaries, sentence order, word stress, or morphological transformations — they need to *see* them.

**Auto-animate is the primary tool for grammar showing.** Use it for:
- **Word transformations:** two separate words sliding together to form a compound adjective (`heart` + `breaking` → `heartbreaking`)
- **Sentence restructuring:** jumbled word order rearranging into a correct sentence
- **Clause visualization:** a fragment expanding into a full clause with subject/verb appearing
- **Word stress:** syllables separating and the stressed syllable highlighting
- **Error → correction pairs:** an incorrect form morphing into the correct form in place

**Pattern for grammar auto-animate** (from M3-WRITING-CA-FEEDBACK, the gold standard):
```markdown
#  {data-auto-animate="true" data-auto-animate-id="punct-demo"}

[text before error]{data-id=t1} [error]{data-id=t2} [text after error]{data-id=t3}

[Rule text hidden.]{style="visibility: hidden;"}

#  {data-auto-animate="true" data-auto-animate-id="punct-demo"}

[text before correction]{data-id=t1} [correction]{data-id=t2 style="border: 2px solid #ffdd00; border-radius: 4px; padding: 2px 8px;"} [text after correction]{data-id=t3}

[Rule text visible.]{style="color: #ffdd00;"}
```

**Key rule:** ALL `data-id` elements must persist between entry and reveal. If an element with `data-id` vanishes on the reveal slide, it disappears abruptly — the student sees a blink, not a transformation. The only thing that should change is the *content or styling* of the persistent elements.

**If you cannot auto-animate it, fragment-reveal it.** One piece appearing at a time (word, syllable, clause) is still showing. A static block of text with no animation is telling — redesign it.

---

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

### Shield Usage Rule (ALL slides, not just differentiation)

**`.shield` divs are ONLY for image-background slides.** On plain dark background slides, use plain paragraphs or `.block` divs instead. The `.shield` class adds a dark semi-transparent backdrop that is necessary for readability over an image, but on a plain dark slide it creates an unnecessary nested dark box that looks like a design error.

- **Image background** → `::: {.shield} / content / :::` (dark backdrop ensures text is readable)
- **Plain dark background** → `content alone` (the slide background is already dark enough for readability)

This applies to ALL slide content: differentiation tiers, frameworks, definitions, steps — everything. If the slide has no `data-background-image`, do not use `.shield`.

### When differentiation is NOT needed:
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
   --lua-filter="$slidesDir\split-list.lua" \
   --lua-filter="$slidesDir\click-table.lua" \
   --lua-filter="$slidesDir\left-table.lua" \
   --lua-filter="$slidesDir\fa-yellow.lua" \
   --lua-filter="$slidesDir\vocab-audio-fragment.lua" \
   --lua-filter="$slidesDir\timer-inject.lua" \
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
- **Do not guess slide patterns from training data.** Before writing any slides.md, read the full [Proven Markdown Patterns](#proven-markdown-patterns-pandoc-310-revealjs-black-theme) section below. Every pattern you need is documented there. If you guess, you will get it wrong.
- **Do not use `vocab-animate.lua`** — this filter adds `data-auto-animate` to ALL slide headers, breaking navigation. Use `vocab-audio-fragment.lua` (standard build command) for vocabulary audio-on-fragment instead.
- **Do not add Lua filters to the build command that aren't in the standard list.** The standard filters are in the build command section above. Adding extra filters like `vocab-animate.lua`, `split-list.lua`, or `click-table.lua` without consulting the skill first will break the slideshow.
- **Do not use auto-animate (`data-auto-animate` or `data-id=`) for vocabulary word transformations.** The established pattern is one word per slide with fragment reveals + audio (see [Vocabulary slides](#vocabulary-slides-phonemic-script--wordaudio--context) below). Auto-animate is for table/diagram morphing only.
- **Do not reproduce textbook exercise content on slides.** Reference the page and exercise number (e.g. "Exercise 1, p. 38"). Students use their books. Only answer reveal slides should show content.
- **Before writing slides.md, read the Proven Markdown Patterns section in full.** Not skimming. Actually read every pattern. The pattern you need is almost certainly there.

---

## Workflow

### Step 1 — Run baseline tests

Run existing tests to establish green baseline.

### Step 2 — Read the lesson plan

Read the lesson plan and write a bespoke design prompt — reference `.kilo/prompts/slide-design-exemplar.md` as the model.

### Step 3 — Create stage-to-slide blueprint

Create a stage-to-slide design blueprint in `.kilo/plans/` — reference `.kilo/plans/M3-WRITING-CA-FEEDBACK-blueprint.md` as the format model.

### Step 4 — Plan differentiation tiers

For each main task slide, decide Standard / Advanced / Elite access levels.

### Step 5 — Read Markdown patterns

**MANDATORY:** Read the full Proven Markdown Patterns section. Every slide pattern (splash, title, objectives, vocab, exercise cycle, differentiation, answers, etc.) is documented there. Do not guess or invent patterns.

### Step 6 — Set up slides directory

Set up `slides/` directory with assets, CSS, Lua filters, and header file.

### Step 7 — Write slides.md

Write `slides.md` in pure Pandoc Markdown — **no `style=` attributes**, no raw HTML. Include three-tier differentiation with FA icons (shields only for image-background slides). Follow the patterns from Step 5 exactly.

### Step 8 — Validate

Run `python scripts/validate_slides.py output/{subfolder}/slides/slides.md`

### Step 9 — Build

Run pandoc build command from the `slides/` directory.

### Step 10 — Re-test

Run `python -m pytest tests/ -v --tb=short`

### Step 11 — Serve

Start background HTTP server from the `slides/` directory.

### Step 12 — Review

Open browser at `http://localhost:8000/` and verify against the review checklist.

### Step 13 — Stop server

Stop the background server when done.

### Step 14 — Deploy

Run `/git-pages {subfolder}` to deploy to GitHub Pages.

### Step 15 — Update lesson plan

Update `slideshow_url` in the lesson plan `.md` file.

### Before ANY .lua file edit

1. Search via Context7 for the relevant Pandoc Lua filter API function
2. If Context7 is down or doesn't have the answer, fall back to Tavily web search: `pandoc lua filter <topic>`
3. Cite the search result in the edit rationale

---

## Proven Markdown Patterns (Pandoc 3.10, reveal.js black theme)

Always fetch the MOST RECENTLY built slides.md for the current canonical pattern:
```powershell
Get-ChildItem output/*/slides/slides.md | Sort LastWriteTime -Descending | Select -First 1 | Get-Content -TotalCount 25
```

### Title slide (splash + title over same background)
```markdown
#  {#splash data-background-image="assets/splash.jpg" data-background-size="cover"}

#  {#title data-background-image="assets/splash.jpg" data-background-size="cover"}

![](assets/logo.png){.title-logo width=120}

::: {.title-row}
[**Title Text**]{.slide-title}
:::

::: {.shield}
[CTA text.]{.cta-text}
:::
```
- Logo: `{width=120}` (bare integer, no `px` unit)
- `.cta-text` uses plain text, NOT bold markers: `[text]{.cta-text}` not `[**text**]{.cta-text}`
- Exactly 2 content elements on title slide: `.title-row` + `.shield`

### Single-column grid table (objectives, numbered lists)
```markdown
+------------------------------------------------------------------+
| **1.** Item one that can span multiple lines of text here         |
+------------------------------------------------------------------+
| **2.** Item two                                                  |
+------------------------------------------------------------------+
| **3.** Item three                                                |
+------------------------------------------------------------------+
```
Grid tables have NO header row (no `<th>` yellow styling). All rows are body rows.

### Two-column pipe table with Answer column
Leverages `reading-feedback.lua` for white row lines and auto-animate data-ids:
```markdown
| Statement | Answer |
|-----------|--------|
| 1a. Columbus was an Italian explorer. | [**Fact**]{.fragment .answer-reveal} |
| 1b. Columbus was a brave explorer. | [**Opinion**]{.fragment .answer-reveal} |
```

### Three-column click-through table (definition + example pairs)
Wrap in `::: {.click-table}` div. Uses `click-table.lua` filter. Each row appears on click.
```markdown
::: {.click-table}
|  |  |  |
|---|---|---|
| **Fact** | can be proven | **FACT:** Columbus sailed from Spain in 1492. |
| **Opinion** | what someone thinks | **OPINION:** Columbus was a brave explorer. |
:::
```

### Shield usage rule
- **Image background** → `::: {.shield} / content / :::` (semi-transparent backdrop ensures readability)
- **Plain dark background** → plain paragraphs (the slide background is already dark enough)
- Never use `.shield` on a slide without `data-background-image`

### Three-tier differentiation (plain dark slide — NO shields)
```markdown
<i class="fa-solid fa-book-open"></i> **Standard** — Full scaffolding, questions visible.

<i class="fa-solid fa-pencil"></i> **Advanced** — Partial scaffolding, notes allowed.

<i class="fa-solid fa-star"></i> **Elite** — Minimal scaffolding, from memory.
```
If slide HAS a background image, wrap each tier in `::: {.shield}` instead.

### Exercise cycle (transition → skill → task+timer → answers)
Each exercise gets its own four-slide cycle:
```markdown
# Exercise N {#transition-exN data-background-color="#c0392b"}

# Skill for Exercise N {#skill-exN}
**Skill:** Skill name
Pedagogical advice here.

# Exercise N {#task-exN data-timer="300"}
Instructions here.

# Check Your Answers {#answer-exN}
[Answer 1.]{.fragment .answer-reveal}
[Answer 2.]{.fragment .answer-reveal}
```
Lower-order exercises: bare answers (short fragments).
Higher-order exercises: answer + explanation + evidence, one per slide.

### Answer slides with paragraph references (higher-order)
```markdown
::: {.split-list}
|  |  |
|---|---|
| **Question** | N — Paragraph X (Author) |
| **[Answer]{.highlight}** | Brief answer here. |
| **[Reason]{.highlight}** | Why this is the answer. |
| **[Evidence]{.highlight}** | *"Direct quote from source text."* |
:::
```

### Fragment rule
- Wrap ENTIRE cell content inside `[...]{.fragment .answer-reveal}` — hidden fragment text that takes up space causes unwanted indentation
- Lower order: bare answers (e.g. `[28 May 2000 · Sydney Harbour Bridge]{.fragment .answer-reveal}`)
- Higher order: full content inside the fragment (e.g. `[**Fact** — Historical records confirm...]{.fragment .answer-reveal}`)

### Timer on task slides
```markdown
# Task slide {#task-id data-timer="300"}
```
Read by `timer-inject.lua`. Value in seconds. Place after `vocab-audio-fragment.lua` in filter list.

### Font Awesome icons — yellow
All `<i class="fa-solid fa-...">` tags are colored yellow (`#ffd700`) by `fa-yellow.lua`. Add `[text]{.highlight}` for yellow text on any inline content.

### Vocabulary slides (phonemic script → word+audio → context)
```markdown
#  {#vocab-navigator}

/ˈnævɪɡeɪtə/

[**navigator**]{.fragment .answer-reveal data-audio-src="assets/vocab-navigator.mp3"}

[Context sentence here.]{.fragment .answer-reveal}
```
Audio plays on FRAGMENT reveal (not slide entry) via `vocab-audio-fragment.lua`.

---

## Error Handling

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Pandoc build fails with "Unknown writer" | Pandoc version too old | Update Pandoc to 3.9+ or check `-t revealjs` is available |
| YouTube embed shows Error 153 | Used `data-background-iframe` instead of `::: {.youtube}` div | Use the `.youtube` fenced div pattern from slides.md |
| Audio does not autoplay on slide entry | Audio path incorrect or missing `data-autoplay` attribute | Verify `audio-autoplay.lua` is in the filter list and audio file exists at the referenced path |
| Fragments visible on slide entry | Missing `.fragment` class or `opacity: 1` set on base class | Ensure fragment content uses `[text]{.fragment .answer-reveal}` syntax |
| Auto-animate elements disappear between slides | `data-id` on an element from the entry slide is missing on the reveal slide | Every element with `data-id` on slide N must also appear on slide N+1 (content/styling can change, but the element must exist) |
| CEFR badge not rendering | Badge text missing `.title-row` wrapper | Wrap the badge header row in `::: {.title-row}` |
| `.shield` boxes not visible over image background | `shield-block.lua` filter missing from build command | Add `--lua-filter="$slidesDir\shield-block.lua"` to the pandoc command |

---

## Scripts

The following scripts ship with this skill and are copied to each slideshow's `slides/` directory at build time:

- `scripts/youtube-embed.lua` — Converts `::: {.youtube}` fenced divs to responsive YouTube iframe embeds
- `scripts/audio-autoplay.lua` — Injects `<audio data-autoplay>` elements from heading attributes for autoplay on slide entry
- `scripts/autocue.lua` — Wraps `::: {.autocue}` divs in scrolling teleprompter container
- `scripts/shield-block.lua` — Forces `.shield` divs to display as blocks with dark backdrop (for image-background slides)
- `scripts/box-keywords.lua` — Wraps `[key]{.box}` spans in yellow-bordered boxes for visual reinforcement
- `scripts/reading-feedback.lua` — Adds white row lines and auto-animate `data-id` on table answer cells
- `scripts/slide-helper.lua` — Shared Lua library providing validated HTML generation functions used by all filters
- `scripts/validate_slides.py` — Pre-build validation: checks speaker notes, raw HTML, fenced div balance, YouTube IDs, inline CSS
- `scripts/lint_slides.py` — Post-build linting: checks banned colors, text shadow, answer slide structure
- `scripts/serve_slides.py` — Convenience server that opens the browser automatically


