---
name: create-beautiful-slideshows
description: Generate reveal.js slideshows from lesson plans using the Markdown → Pandoc → reveal.js pipeline.
license: MIT
compatibility:
  - python3
  - pandoc
  - reveal.js
metadata:
  author: Ed Rush (C·E·L Mathayom / ACT)
---

# Skill: Create Beautiful Slideshows

**Pipeline:** Markdown → Pandoc → reveal.js  
**Agent writes:** Pure Pandoc Markdown only — no HTML, no Typst, no raw CSS  
**Lua filters handle:** Audio autoplay, YouTube embeds  
**CSS handles:** Styling, shields, fragments, responsive sizing

## CSS / HTML Files Are Forbidden

- Do NOT read or edit any `.css`, `.html`, or `.htm` file
- `slides-pandoc.css` is hash-locked — modifying it breaks validation
- `slides-header.html` is copy-only — never write HTML by hand
- If a visual problem exists, fix in Pandoc Markdown or a Lua filter — NEVER in CSS
- The `style=` attribute is forbidden in `slides.md`

---

## Purpose

Generate interactive reveal.js slideshows from lesson plan content. The agent writes pure Pandoc Markdown (`slides.md`); Pandoc converts it to HTML using `--slide-level=1` (all horizontal slides). Lua filters inject native reveal.js features (audio autoplay, YouTube embeds). A shared CSS file handles styling.

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

## Core Design Principle: Show, Don't Tell

**Every slide must answer:** *"What does this slide let the student SEE that they wouldn't get from just reading the textbook or hearing the teacher say it?"*

If a slide only restates something the teacher could say or the book already shows, delete it or redesign it. The slide must earn its place.

**Before writing every slide, ask:**
- What does the student SEE change/animate/appear? (Show, don't tell)
- Does this reduce cognitive load or add to it?
- Could the teacher achieve the same effect by just speaking? (If yes, kill the slide)
- Is this slide for the teacher or for the student?

| Telling (delete) | Showing (keep) |
|---|---|
| "Exercise 3, p. 39 — Answer the 6 questions" | Transition → Skill → Task with timer → Answers fragment-revealed one by one |
| List of 5 vocab words with definitions | One word per slide. Phonemic script first. Word + audio on click. Context sentence on next click. |
| "Here are compound adjectives" (static list) | Auto-animate pair: words slide together and merge |
| Summary bullet points at end | A closing image or question that sends students out thinking |

### Grammar: showing is non-negotiable

**Auto-animate is the primary tool for grammar showing.** Use it for word transformations, sentence restructuring, clause visualization, word stress highlighting, and error→correction pairs.

**Key rule:** ALL `data-id` elements must persist between entry and reveal. If an element with `data-id` vanishes on the reveal slide, it disappears abruptly — the student sees a blink, not a transformation.

**If you cannot auto-animate it, fragment-reveal it.** A static block of text with no animation is telling — redesign it.

See `references/PATTERNS.md` for exact grammar auto-animate syntax.

---

## Pedagogical Requirements

### Tiered Differentiation (Standard / Advanced / Elite)

**Every main task slide must offer tiered challenges.** Students self-select the level that matches their readiness.

| Tier | Scaffolding | Description |
|------|------------|-------------|
| **Standard** | Full support | Task scaffold visible (questions, prompts, word bank) |
| **Advanced** | Partial support | No scaffold during input; take notes, then answer from notes |
| **Elite** | Minimal support | Complete from memory and understanding alone |

**By skill:**
- **Reading:** Standard = questions visible. Advanced = read, notes, answer. Elite = read once, no notes.
- **Listening:** Standard = questions visible. Advanced = listen, notes, answer. Elite = listen once, answer from memory.
- **Speaking:** Standard = planned with bullet points. Advanced = planned from notes. Elite = spontaneous.
- **Writing:** Standard = model + word bank. Advanced = outline only. Elite = free writing.

**Display:**
- **Plain dark slide (no image):** Three paragraphs with bold tier labels + FA icons — no shields
- **Image-background slide:** Three `.shield` divs (dark backdrop for readability)

See `references/PATTERNS.md` for exact display syntax.

### Shield Usage Rule

`.shield` divs are ONLY for image-background slides. On plain dark slides, use plain paragraphs. Never use `.shield` on a slide without `data-background-image`.

### When differentiation is NOT needed:
Lead-in, transition, summary, stimulus-only slides, title and objectives slides.

---

## What NOT to Do

- **Do not read or edit .css, .html, or .htm files**
- **Do not edit .lua files** without Context7 search for the API function first
- **Do not write raw HTML** — use Pandoc Markdown only
- **Do not write inline CSS (`style=`) in slides.md** — validation will fail
- **Do not use `--slide-level=2`** — creates vertical slides
- **Do not use `data-background-iframe` for YouTube** — Error 153
- **Do not put `title:` in YAML frontmatter** — Pandoc generates an unstyled auto-title-slide before the splash. Use `pagetitle:` instead to set the HTML `<title>` tag without triggering the auto title slide:
  ```yaml
  ---
  pagetitle: "Lesson Name"
  ---
  ```
- **Do not embed pedagogical intent annotations inline in slides.md** — comments between YAML frontmatter and the first `#` heading create phantom `<section>` elements with no id. Comments that follow a heading (no blank line) are invisible to the test (which looks 2000 chars before the `<section>` tag). Use the `splash-annotations.html` companion file pattern instead (see `references/PATTERNS.md`).
- **Do not use `##` for slide breaks** — only `#`
- **Do not invent statistics** — source from lesson plan or transcript
- **Do not use `<!-- .element: class="fragment" -->`** — inert HTML comments
- **Do not use `---` to separate slides** — use `# ` headings
- **Do not skip the blueprint phase** — create `.kilo/plans/{lesson}-blueprint.md` first
- **Do not write teacher questions on slides** — the teacher elicits live
- **Do not reproduce full model texts or reading passages** — students use handouts
- **Do not exceed 25 body-text words per content slide** — split or fragment
- **Do not exceed 40 slides total for a 46-minute lesson**
- **Do not use more than 3 auto-animate pairs per presentation**
- **Do not present undifferentiated tasks** — see Pedagogical Requirements above
- **Do not guess slide patterns** — read `references/PATTERNS.md` before writing any slides
- **Do not use `vocab-animate.lua`** — use `vocab-audio-fragment.lua` instead
- **Do not use auto-animate for vocabulary** — use one-word-per-slide with fragment reveals

---

## Workflow

### Step 1 — Run baseline tests
```powershell
python -m pytest tests/ -v --tb=short
```

### Step 2 — Read the lesson plan
Read the lesson plan and write a bespoke design prompt. Reference `.kilo/prompts/slide-design-exemplar.md` as the model.

### Step 3 — Create stage-to-slide blueprint
Write to `.kilo/plans/{lesson}-blueprint.md`. Reference `.kilo/plans/M3-WRITING-CA-FEEDBACK-blueprint.md` as the format model. Present for user approval before proceeding.

### Step 4 — Plan differentiation tiers
For each main task slide, decide Standard / Advanced / Elite access levels.

### Step 5 — Read Markdown patterns
Read `references/PATTERNS.md` in full. Every slide pattern is documented there. Do not guess.

### Step 6 — Read architecture reference
Read `references/ARCHITECTURE.md` for build commands, infrastructure copy, test/serve/deploy procedures.

### Step 7 — Set up slides directory
Copy assets (logo, splash image) and infrastructure files. See `references/ARCHITECTURE.md` for the copy commands.

### Step 8 — Write slides.md
Pure Pandoc Markdown — no `style=`, no raw HTML. Follow patterns from `references/PATTERNS.md`.

### Step 9 — Validate
```powershell
python scripts/validate_slides.py output/{subfolder}/slides/slides.md
```

### Step 10 — Build
Run the pandoc build command from the `slides/` directory (see `references/ARCHITECTURE.md`).

### Step 11 — Re-test
```powershell
python -m pytest tests/ -v --tb=short
```

### Step 12 — Serve
```powershell
background_process start --command "python -m http.server 8000" --workdir "output/{subfolder}/slides/"
```

### Step 13 — Review
Open `http://localhost:8000/` and verify against the review checklist in `references/ARCHITECTURE.md`.

### Step 14 — Stop server and deploy
```powershell
/git-pages {subfolder}
```
Update `slideshow_url` in the lesson plan `.md` file.

---

## Examples

### Example 1: M3 Speaking — Gender Stereotypes and Gen Z
**Request:** Create slides for the M3 gender stereotypes speaking lesson
**Action:** Plan 23-slide mapping (title → objectives → lead-in → video → CCQs → model answer → opinion analysis → structure table → prepare → record → self-assessment → end). Write `slides.md` with audio autoplay for model answers, YouTube embed for video clip, fragment reveals for CCQs and answer analysis, pipe table for discourse markers, auto-animate for structure comparisons.
**Output:** `output/M3-SPEAKING-TBL-GENDER-ROLES/slides/index.html`

### Example 2: M3 Writing — CA Feedback
**Request:** Slides for writing CA feedback session
**Action:** Plan 12-slide mapping (title → lead-in → common errors with auto-animate pairs → your turn → end). Use `data-auto-animate` for punctuation correction pairs, `data-timer` for writing task countdown, CEFR badge in title row.
**Output:** `output/M3-WRITING-CA-FEEDBACK/slides/index.html`

### Example 3: M2 Business — B1
**Request:** Slides for business lesson, B1 level
**Action:** Title → objectives → vocabulary → listening → practice → production → summary → end. No audio or YouTube.
**Output:** `output/m2-5a-business/slides/index.html`

---

## Error Handling

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Pandoc fails "Unknown writer" | Pandoc too old | Update Pandoc to 3.9+ |
| YouTube embed Error 153 | Used `data-background-iframe` | Use `::: {.youtube}` div pattern |
| Audio does not autoplay | Wrong path or missing filter | Verify `audio-autoplay.lua` is in filter list |
| Fragments visible on entry | Missing `.fragment` class | Use `[text]{.fragment .answer-reveal}` |
| Auto-animate element vanishes | `data-id` missing on reveal slide | Every `data-id` from entry must exist on reveal |
| CEFR badge not rendering | Missing `.title-row` wrapper | Wrap badge row in `::: {.title-row}` |
| Shield not visible | `shield-block.lua` missing | Add to pandoc build command |

See also `references/TROUBLESHOOTING.md`.

---

## Reference Files

- `references/PATTERNS.md` — All slide Markdown patterns (read before writing slides)
- `references/ARCHITECTURE.md` — Build commands, infrastructure, test/serve/deploy (read during setup)
- `references/CSS.md` — CSS class table and design rules (read when styling questions arise)
- `references/TROUBLESHOOTING.md` — Extended symptom-to-fix table (read when errors occur)

---

## Scripts

All scripts ship from `scripts/` in the project root:

- `scripts/youtube-embed.lua` — Converts `::: {.youtube}` to responsive YouTube iframe
- `scripts/audio-autoplay.lua` — Injects `<audio data-autoplay>` for slide-entry audio
- `scripts/autocue.lua` — Scrolling teleprompter for `::: {.autocue}` divs
- `scripts/shield-block.lua` — Forces `.shield` divs to block display with dark backdrop
- `scripts/box-keywords.lua` — Yellow-bordered boxes around `[key]{.box}` spans
- `scripts/reading-feedback.lua` — White row lines + auto-animate `data-id` on tables
- `scripts/slide-helper.lua` — Shared Lua library required by all filters
- `scripts/white-reveal.lua` — Injects CSS for `.fragment.white-reveal.visible` (white text on reveal for non-answer content)
- `scripts/validate_slides.py` — Pre-build Markdown validation
- `scripts/lint_slides.py` — Post-build HTML linting
- `scripts/serve_slides.py` — Convenience HTTP server with auto-open
