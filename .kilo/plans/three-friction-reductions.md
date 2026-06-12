# Plan: Three Friction Reductions

**Date:** 12 June 2026  
**Status:** Plan — awaiting approval before execution

---

## Step 1: Integrate `typst_check.py` into skill workflows

### What
Add a mandatory compile-check step to both Typst-producing skills, so the agent validates Typst code against the actual compiler before writing final output.

### Changes

**File A: `.kilo/skills/create-pdf-lesson-file/SKILL.md`**

Insert into the "Typst Syntax — Avoid Hallucination" section (after line 96, the "follow read-edit-compile-check" rule):

```markdown
### Mandatory Pre-Output Validation

**Before writing ANY `.typ` file to disk, validate it through `typst_check.py`:**

```powershell
python scripts/typst_check.py path/to/file.typ
```

**For snippets generated inline (not yet written to disk), pipe via stdin:**

```powershell
echo "$typstContent" | python scripts/typst_check.py -
```

**If validation fails:** Read the error output, fix the Typst code, and re-validate. Do NOT write the file until validation passes (exit code 0).

**If validation passes:** Proceed to write the `.typ` file, then continue to `typst compile`.

This replaces the old "follow read-edit-compile-check" rule — the agent now checks BEFORE writing, not after.
```

**File B: `.kilo/skills/create-bespoke-materials/SKILL.md`**

Insert a new section after the "Hard-Won Lessons" block (after line 40):

```markdown
### Pre-Output Typst Validation (MANDATORY)

Before writing any `.typ` file for bespoke materials, validate it:

```powershell
python scripts/typst_check.py path/to/file.typ
# or for inline content:
echo "$typstContent" | python scripts/typst_check.py -
```

Do NOT write the file until validation passes. The tool catches: mid-word bold, hash-in-content, hash-in-code-mode, unclosed blocks, and all other compile errors catalogued in the Typst Pitfalls section.
```

### Rationale
The current workflow is "write → compile → read errors → fix → recompile." This takes 2+ human-in-the-loop cycles. The new workflow is "write → validate → fix (if needed) → write file → compile" — the agent fixes errors before the human ever sees them.

---

## Step 2: Build pedagogical scaffold script (`scripts/scaffold_slides.py`)

### What
A Python script that generates the HTML skeleton for a reveal.js slideshow. Takes the base template, inserts N empty `<section>` elements with guaranteed valid structure, stable IDs, and placeholder comments. The agent then fills content via targeted Edit tool calls — one slide at a time — instead of generating all 37+ sections in a single Write.

### Design

```bash
python scripts/scaffold_slides.py \
  --count 37 \
  --output output/051226-topic/slides/index.html
```

**What it produces** (inserted between `<div class="slides">` and `</div>`):

```html
<!-- Slide 0 -->
<section id="slide-0">
  <!-- TODO: Fill slide 0 content here -->
</section>

<!-- Slide 1 -->
<section id="slide-1">
  <!-- TODO: Fill slide 1 content here -->
</section>
...
```

**What it does NOT do:**
- Does NOT set background colors (agent sets these during content fill based on slide type)
- Does NOT set fragment classes (agent adds these during content fill)
- Does NOT add auto-animate attributes (agent adds these during content fill)
- Does NOT add any content — purely structural scaffolding

**What it DOES do:**
- Copies `templates/base-slides-template.html` to the output path
- Copies SFX files (`blip.mp3`, `BELL.mp3`) from `C:\PROJECTS\SFX\` to `output/.../slides/assets/`
- Copies institution logo to `output/.../slides/assets/`
- Creates `assets/` directory if missing
- Inserts N empty `<section>` elements with stable, sequential IDs
- Prints slide count to stdout for verification
- Exits 0 on success, non-zero on failure

**Edge cases:**
- Output directory doesn't exist → create it (mkdir -p)
- Base template not found → error, exit 2
- SFX files not found → warn but continue (not all presentations need timers)
- `assets/` already exists → skip creation, don't overwrite existing files

### Skill integration

Update `.kilo/skills/lesson-plan-to-reveal/SKILL.md` Step 1 (currently "Copy the base template"):

**Old (line 144-150):**
```markdown
### Step 1: Copy the base template
```powershell
cp "templates/base-slides-template.html" "output/{subfolder}/slides/index.html"
```
```

**New:**
```markdown
### Step 1: Generate the slide scaffold

After Phase 0 (Design Blueprint) is complete and you know the exact slide count:

```powershell
python scripts/scaffold_slides.py \
  --count <N> \
  --output "output/{subfolder}/slides/index.html"
```

This copies the base template, inserts <N> empty `<section>` elements with stable IDs (`slide-0`, `slide-1`, ...), copies SFX files and the logo to `assets/`, and guarantees valid HTML structure.

**Do NOT write `<section>` elements from scratch.** The scaffold guarantees every tag is balanced. Each slide is then filled one at a time using the Edit tool — targeting the `<!-- TODO: Fill slide N content here -->` comment and replacing it with the slide's HTML content.
```

### Rationale
The single most common structural bug is unbalanced `<section>` tags from bulk generation. The scaffold-first approach eliminates this entirely — the script guarantees `opens == closes` from the start. Each subsequent Edit tool call targets one section, so if an edit introduces a bug, it's isolated to that section.

---

## Step 3: Add overflow detection (`scripts/check_overflow.py`)

### What
A Python script using Playwright to render each slide in a headless browser and detect content extending beyond the slide viewport. Complements the existing `lint_slides.py` (design rules) and `revealjs-validator` (structural rules).

### Design

```bash
python scripts/check_overflow.py --project output/051226-topic/slides/
```

**How it works:**
1. Starts a local HTTP server on a random port serving the slides directory
2. Opens `index.html` in a headless Chromium browser (Playwright)
3. For each slide:
   - Navigates to the slide (via reveal.js hash: `#/N`)
   - Waits for reveal.js to initialize and render
   - Queries all child elements of the current slide section
   - Checks if any element's bounding rect exceeds the viewport bounds (1280×720)
   - Reports overflow: slide index, element tag, overflow direction (bottom/right), pixel amount
4. Shuts down the server and browser

**Output format:**
```
Slide 12: OVERFLOW — <div class="content"> extends 45px past bottom edge
Slide 12: OVERFLOW — <p class="a-why"> extends 12px past bottom edge  
Slide 27: OVERFLOW — <table class="answer-table"> extends 80px past bottom edge

3 slides with overflow detected (out of 37 total).
```

**Exit codes:**
- 0 — no overflow
- 1 — overflow detected (warnings only)
- 2 — tool error (browser not available, server failed, timeout)

**Dependencies:**
- `playwright` (Python package)
- `playwright install chromium` (one-time browser download)
- Already available: Python 3.x, local file serving

**Edge cases:**
- Slides with `data-auto-animate` — check both entry and reveal states
- Slides with fragments — check all fragment states (content may be hidden then revealed)
- Slides with timers/audio — skip these checks (timers are overlay elements)
- Very large presentations (50+ slides) — timeout per slide: 5s, total timeout: 5 minutes
- No internet (CDN links) — warn but continue; some layouts may render differently without reveal.js CSS

### Skill integration

Add as a new Phase 3 validation step in `.kilo/skills/lesson-plan-to-reveal/SKILL.md`:

```markdown
### Phase 3: Post-generation Validation (updated)

After filling all slides, run in order:

1. **Design rule check:**
   ```powershell
   python scripts/lint_slides.py --project "output/{subfolder}/slides/"
   ```

2. **Overflow check (NEW):**
   ```powershell
   python scripts/check_overflow.py --project "output/{subfolder}/slides/"
   ```
   Fix any slides with detected overflow before proceeding.

3. **Structural validation:**
   ```powershell
   npx revealjs-validator --project "output/{subfolder}/slides/"
   ```

4. **Section balance check** (unchanged) — count opens vs closes
```

### Rationale
`lint_slides.py` catches design rule violations (wrong colors, banned properties). `revealjs-validator` catches structural issues (missing attributes, invalid markup). But NEITHER catches visual overflow — text that extends past the slide boundary. This is a common failure mode when answer slides have dense content or pedagogical slides have long procedure text. The overflow check catches these at build time instead of at presentation time.

---

## Implementation order

1. **Step 1 first** (lowest risk, immediate value) — edit two SKILL.md files to add `typst_check.py` as mandatory step
2. **Step 2 second** (medium risk, new script) — build `scaffold_slides.py`, update skill workflow
3. **Step 3 third** (highest complexity, new dependency) — build `check_overflow.py` with Playwright, add to validation phase

## Files to create/modify

| File | Action |
|---|---|
| `.kilo/skills/create-pdf-lesson-file/SKILL.md` | Edit — add pre-output validation section |
| `.kilo/skills/create-bespoke-materials/SKILL.md` | Edit — add pre-output validation section |
| `scripts/scaffold_slides.py` | **Create** — new scaffold script |
| `.kilo/skills/lesson-plan-to-reveal/SKILL.md` | Edit — replace Step 1 with scaffold workflow, add Phase 3 overflow step |
| `scripts/check_overflow.py` | **Create** — new overflow detection script |
