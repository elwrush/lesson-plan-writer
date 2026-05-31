# AGENTS.md — Lesson Plan Writer 3

## Environment

- **OS:** Windows AMD64 (win32 sys.platform)
- **Shell:** PowerShell
- **Python:** 3.x
- **PowerShell quoting trap:** Inline `python -c "..."` with complex quoting (regex, nested quotes, f-strings with backslashes) ALWAYS hits PowerShell escaping issues. **Never use inline `python -c` for complex code.** Instead: write the Python script to `C:\Users\elwru\AppData\Local\Temp\kilo\*.py` via the Write tool, then execute via `python "C:\Users\elwru\AppData\Local\Temp\kilo\*.py"`. This avoids all quoting problems.

## Golden Rule: Pattern-first, not guess-first

Before writing any HTML, CSS, Typst, slide markup, or configuration, **read the template or an existing file that already does what you need**. The correct pattern is always in the codebase already — guessing or generating from training data wastes time and causes errors. Specifically:
- Slide attributes: check `templates/base-slides-template.html` for the exact attribute pattern
- Typst syntax: check `.kilo/skills/create-pdf-lesson-file/SKILL.md` (Typst Pitfalls section)
- Slide structure: check the most recently built `output/*/slides/index.html`

## Two pipelines

### PDF (2-stage)
1. **`write-lesson-plan` skill** → `output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json`
2. **`create-pdf-lesson-file` skill** → converts JSON → `PDF/{subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`

### Slides (template-based)
1. **`write-lesson-plan` skill** → JSON (same as above)
2. **`lesson-plan-to-reveal` skill** → copies `templates/base-slides-template.html` → hand-builds `index.html` with raw HTML `<section>` elements in `output/{subfolder}/slides/`
3. **`/git-pages` command** (or `publish-to-github-pages` skill in `.kilo/skills/`) → deploys all slideshows in `output/` to gh-pages

**Markdown pipeline is permanently abandoned.** All slides are raw HTML `<section>` elements. `scripts/json_to_markdown.py` is deprecated — do not use for new presentations. Auto-animate requires sibling `<section data-auto-animate>` elements, which cannot be produced from the markdown plugin.

## Key commands

```bash
# Kilo CLI commands
# /git-backup — Stage all, auto-generate commit message, commit+push to main
# /git-pages — Deploy slides subfolder to gh-pages with landing page
# /lint — Run ruff check --fix and ruff format

# PDF (from project root)
python scripts/json_to_pdf.py output/<subfolder>/<file>.json

# Slides — copy base template + hand-build sections
cp "templates/base-slides-template.html" "output/<subfolder>/slides/index.html"

# Slide validation (runs 66 reveal.js rule checks)
npx revealjs-validator --project "output/<subfolder>/slides/"
# Then open index.html in browser + check console (F12) for errors

# Pixabay image download (for slide backgrounds)
python scripts/pixabay_download.py --query "topic" --type image --count 3

# Tests (56 total, all pass)
python -m pytest tests/ -v
python -m pytest tests/test_json_to_pdf.py -v          # 18 tests
python -m pytest tests/test_json_to_markdown.py -v      # 26 tests
python -m pytest tests/test_git_pages_safety.py -v      # 12 tests — red-green safety guard for /git-pages

# Locate slide by reveal.js index (deterministic editing)
python scripts/locate_slide.py "file:///path/to/index.html#/7"
python scripts/locate_slide.py 7 --slides-dir path/to/slides/
```

## Linting & Quality

ruff is installed globally via pip. **Pre-commit hook is permanently uninstalled** (caused git lock contention). Use the `/lint` command instead — it runs encoding checks, then ruff on demand with no background processes.

**Windows UTF-8 trap:** Python on Windows defaults to cp1252 for file I/O and console output. Always use `encoding="utf-8"` when opening project files (`open(path, "r", encoding="utf-8")`). For scripts that print Unicode to the console, add:
```python
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```
The `check_encoding.py` script (run as part of `/lint`) scans all text files for encoding issues and fixes cp1252→UTF-8.

To avoid cp1252 issues in interactive Python sessions, set `$env:PYTHONUTF8=1` in PowerShell before running Python commands that handle project files. This makes Python default to UTF-8 for all file I/O on Windows.

```bash
# Lint + fix (all files) — replaces pre-commit hook
python -m ruff check --fix .

# Format all Python files
python -m ruff format .

# Both in sequence
python -m ruff check --fix . ; python -m ruff format .

# Run pre-commit checks on all files (without hook, without committing)
python -m pre_commit run --all-files
```

A lint command is defined at `.kilo/command/lint.md` — invoke via Kilo CLI.

## JSON schema

- Top-level: `teacher`, `duration`, `date` (DDMMYY), `topic`, `materials`, `lesson_plan`
- `lesson_plan` keys: `shape`, `shape_name`, `cefr_level`, `class`, `stages[]`
- Each stage: `stage_number`, `stage`, `stage_aim`, `procedure`, `time`, `interaction`
- Optional top-level: `transcript`, `answer_key`, `cefr_level`, `class`, `objective`
- `answer_key` value: `"none"`, or a file path to `.typ` markup (`.md` files are NOT accepted — the markdown intermediary was removed)
- **`lesson_plan` and `answer_key` use underscore** (not hyphen). The test fixture has a bug — uses `answer-key` — ignore it; production JSON always uses `answer_key`.
- Shape templates (A–G) at `knowledge-base/lesson plan shapes/json/shape-{letter}.json`

## PDF rendering (Typst)

- Renderer: `typst compile` (NOT Quarto — abandoned, it ignored `format: typst`)
- Template: `.typ` content generated by `build_typ_content()` in `scripts/json_to_pdf.py` (Python f-strings, compiled with `typst compile`)
- Font: Roboto OTF from `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\` via `--font-path`
- Logos: `templates/Image_20260324_141022.png` (ACT), `templates/cambridge.png` (Cambridge) — page-1 content only, not a page header
- Logo band is rendered as page-1 content (a `#block` + `#grid`), not as a page header. Margins are uniform at 0.75in.
- Line spacing: `#set par(leading: 0.55em)` — leading is **additional** space, not a multiplier

## Typst Error Reference

When Typst compilation fails, the most common causes are documented in the `create-pdf-lesson-file` skill at: `.kilo/skills/create-pdf-lesson-file/SKILL.md` (section: **Typst Pitfalls — Compile Errors and Fixes**).

Five known error patterns covered:
1. **Bold only at word boundaries** — `*M*y` fails; use `#strong[M]y`
2. **`#` inside content blocks** — `[*#*]` fails; use `[*\#*]`
3. **Raw blocks are markup, not function arguments** — `#raw(```)``` invalid; use `` ``` `` directly
4. **`#raw()` takes a string** — no backtick syntax inside function calls
5. **No markdown pipe tables** — use `#table(columns: N, ...)` instead

**Before modifying any `.typ` file or `json_to_pdf.py`, read the Categorised Typst Pitfalls section in that skill first.** Do not guess Typst syntax from training data.

## Content transforms (in json_to_pdf.py build_typ_content)

- Date: `050726` → `7 May, 2026`
- Stage aims: robotic templates humanized (e.g. "To reading for gist" → "To understand the general idea of the text")
- Procedure: minute indicators stripped (`3 min.` → ``)
- Windows paths: `\` → `/` for Typst

## Language quality

Stage aims must read as natural English, not template fills. Unacceptable:
- "To lead-in to the topic of..."
- "To reading for gist"
- "To post-reading speaking task"

Acceptable: "To activate interest in...", "To get the general idea of the text", "To discuss ideas from the reading"

## Slide design reference

`docs/slide-design-reference.md` defines slide types (vocabulary, task, answer, transition), fragment policy, auto-animate rules, and Pixabay image strategy. The `json_to_markdown.py` script reads this doc at generation time.

### V1 Slide Flow (Actual)

```
SLIDESHOW FLOW — index2.html
────────────────────────────────────────────
 0  Title (Pixabay background, CEFR badge)
 1  Objective (4 bullets)
 2  Lead-in (Pixabay bg, discussion Q)
 3  Vocab 1 (generation gap) — h2 on first only
 4  Vocab 2 (frustration)
 5  Vocab 3 (redefine)
 6  Vocab 4 (workplace)
  7  Transition → What's the main idea? (red bg)
  8  Transition → Finding details (red bg)
  ─────── T/F Strategy Block (4 steps) ───────
  9  T/F Header + Step 1 + tip text
 10  T/F Step 2 (sub-questions + rule)
 11  T/F Step 3 (evidence + keywords)
 12  T/F Step 4 (answer with paragraph quotes)
 13  Exercise 2 Timer (60s)
 14  Exercise 2 Answers (answer-table, tick/cross, Why column)
  ─────── Paragraph Matching Block (4 steps) ───────
 15  Transition → Matching ideas (red bg)
 16  Para Matching Header + Step 1
 17  Para Matching Step 2 (keywords list)
 18  Para Matching Step 3 (scan paragraphs)
 19  Para Matching Step 4 (confirm match + answer)
 20  Exercise 3 Timer (180s)
 21  Exercise 3 Answers (1–2) (answer-table, Why column)
 22  Exercise 3 Answers (3–4)
 23  Exercise 3 Answers (5–6)
  ─────── Multiple Choice Strategy Block (5 steps) ───────
 24  Transition → Making conclusions (red bg)
 25  MC Header + Step 1 (demo Q + options)
 26  MC Step 2a (auto-animate entry, transparent borders)
 27  MC Step 2b (auto-animate reveal, white borders)
 28  MC Step 3 (scan + photo/headline tip)
 29  MC Step 4 (fragment strike table, a/b eliminated)
 30  MC Step 5 (answer-table wrap, answer + citations)
 31  Exercise 4 Timer (240s)
 32  Exercise 4 Answer (answer-table wrap, tick/cross, Why)
  ─────── Discussion — Review — Summary ───────
 33  Transition → Let's Discuss (red bg)
 34  Task → Let's Discuss (420s, 3 Qs)
 35  Transition → Let's Review (red bg)
 36  Summary (✓ bullets)
────────────────────────────────────────────
```

### Mandatory Pre-Write Checklist (for agent)

Before writing ANY slide HTML for a new or updated presentation, this agent MUST:
1. **Read `templates/base-slides-template.html`** — open the file and scroll through the reference slides section. Find the EXACT pattern for each slide type you need.
2. **Copy, don't invent** — use the working example as a template. Change content only, not structure. Any pattern not in the template must be explicitly approved.
3. **Check font sizes** — every text element must be ≥0.9em (labels) or ≥1em (body). Title slide h2=2.2em, logo 120px. No 0.7em text.
4. **Check green background** — answer slides use `#0d5e1a`, NOT `#0d5e1a`. The old green is too light for projection contrast.
5. **Check vertical centering** — title slides need `style="justify-content: center;"`. reveal.js defaults to flex-start.
6. **One concept per slide** — if a slide feels busy, split it. Max 3 items per answer slide.
7. **Auto-animate for transformations** — structural changes (simple→compound, error→correction) use 2-slide auto-animate pairs. Entry = transparent borders, Reveal = `#4fc3f7` blue borders.
8. **Why column on every answer** — every answer slide has an `a-why` span with explanation.
9. **Fragments on answers only** — task instructions, objectives, and summaries stay static. No fragments on non-answer content.
10. **Validate** — run `npx revealjs-validator --project "output/{subfolder}/slides/"` and fix all errors.

If any rule is unclear, ask. Do not guess.

### Key Design Rules

- **One step per slide** — enforced across all three pedagogy blocks
- **Step label format**: `<p><u><strong>Step N:</strong> description</u></p>`
- **Auto-animate**: only between adjacent slides with matching `data-id` on elements; previous slide must NOT have `data-auto-animate`
- **Fragment strike**: `class="fragment strike"` on td/p elements. Built-in CSS provides `opacity: 1` (always visible) and `text-decoration: line-through` only when `.visible` class is added on click
- **Answer tables**: `<table class="answer-table">` with 3 columns (Statement/Answer/Why?). Add `wrap` class for tables with long text. Right column uses `white-space: normal`
- **Table tick/cross**: middle column with `data-fragment-index` matching explanation cell for simultaneous reveal
- **Lightbulb removed** from all answer slides (saves screen real estate)
- **Green answer slide text contrast**: All text on `#0d5e1a` answer slides MUST use only white (`#fff`) or yellow (`#ffdd00`). No gray, blue, or muted colors — they are invisible at projection distance. The template's `.aim-label` uses gray `#888` by default and must be overridden with `color: rgba(255,255,255,0.7)` on green slides.
- **Pedagogical background**: `data-background-color="#1a6b5a"` + `class="pedagogical"` + `data-background-transition="none"`
- **Max 3 items per answer slide** — whether using answer-list flex layout or inline annotations. Split exercises with >3 items across multiple slides.
- **Inline S/V/O annotations** — for grammar identification exercises (subjects, verbs, objects), decorate words directly on the sentence rather than using a separate answer column. Use `class="fragment custom svo-s"`, `svo-v`, `svo-o` on `<span>` elements with CSS controlling border/color changes on `.visible`. Superscript labels (`<sup>S</sup>`, `<sup>V</sup>`, `<sup>O</sup>`) use `opacity: 0` → `opacity: 1` with CSS transitions. Use `data-fragment-index` to group each sentence's decorations and confirmation note for per-click reveal.
- **Custom fragments** — use `class="fragment custom"` when you need an element to stay fully visible but change specific CSS properties (border, color, opacity) on click. The `custom` keyword prevents reveal.js from applying default `opacity: 0; visibility: hidden`. All styling is controlled via CSS rules on `.fragment.custom.*` (default state) and `.fragment.custom.*.visible` (revealed state). Common use: annotations that animate in without hiding the underlying text.
- **Title slide layout** — Full-screen Pixabay background image using `data-background-image` with `data-background-color="#1a1a2e"` as fallback. Logo at `120px` (not 78px — too small on 1280x720). h2 at `2.2em` (not default ~1.6em). CEFR badge inline inside h2 with `vertical-align: middle`. Subheader at `1em` (not 0.7em). Opacity at `0.85` (not 0.7 — too dim). **CRITICAL:** Must add `style="justify-content: center;"` to the section — reveal.js defaults to `flex-start`, pushing content to the top of the slide. Both `data-background-color` AND `data-background-image` are required (background-color shows while image loads). Do NOT use `r-stack` for title slides — it creates a letterbox effect.
- **Font size minimums for readability** — On 1280x720 slides: main sentence text `1.2em`, labels/annotations `0.9em`, faded "before" comparison text `1em` at `rgba(...0.55)`. Never go below `0.85em` for any text. The default reveal.js base sizes assume desktop presentation — ESL students at projection distance need larger.
- **Why column on every answer row** — Every answer slide must include `class="a-why"` with a short explanation text (coordinator meaning, grammar rule, error type). The `a-why` class is defined in the base template CSS. Use `fragment fade-up` matching the answer cell's `data-fragment-index` so answer + explanation reveal simultaneously.
- **Demo slide before freer practice** — Before any freer practice task (e.g. Practice 2C, 10A), include a pedagogical demo slide. The teacher walks through ONE item step by step (Step 1: identify relationship, Step 2: choose coordinator, Step 3: combine) so students see the reasoning chain before attempting independently.
- **Lead-in error slides** — Each error gets a 2-slide auto-animate pair: Entry shows the error with transparent borders on problem words. Reveal dims the original (0.55 opacity) and shows the corrected version in `#4fc3f7` blue with white/blue underlines on fix words. Label line tells what type of error it is.
- **Diagnostic tests max 3 items per slide** — Split diagnostic tests across multiple slides (e.g. `slide-diagnostic-1-3`, `slide-diagnostic-4-6`). Add answer fragments below the questions with the correct coordinator and a Why explanation. Timer on each slide.
- **Formula reveals: 2-slide auto-animate pair** — When demonstrating a structural transformation (simple→compound, wrong→right): Entry shows both versions with transparent borders on CHANGED elements. Reveal changes borders to `#4fc3f7` blue + `box-shadow: 0 3px 0 0 #4fc3f7` for a visual double-underline effect. Both need `data-auto-animate` with matching `data-auto-animate-id`. Key elements need matching `data-id` on both slides.

## Pedagogical Strategy Slides — Design Principles

Strategy slides teach a test-taking or reading skill explicitly. The design follows a **modelled whole-task approach** consistent with Strategy-Based Instruction (SBI) in EFL/ESL reading pedagogy.

### Core Pattern: One Consistent Worked Example

Pick one real exam question and carry it through every step of the strategy. Never mix examples mid-flow. The student sees the complete process on a single item before attempting it alone.

Example: A True/False statement about the "generation gap" article runs through Steps 1–4. A Multiple Choice question runs through its own 3 steps. Do not switch between different exam items within the same strategy block.

### Step Structure

| Step | Cognitive function | What goes on the slide |
|---|---|---|
| 1 | Decode | Read the statement carefully. Note each separate claim. |
| 2 | Analyse | Break into Yes/No sub-questions. State the decision rule (Yes→TRUE / No→FALSE). |
| 3 | Locate | Identify which paragraph(s) contain the evidence. Name them explicitly. |
| 4 | Confirm | Show the original question in yellow. Quote the text that confirms each sub-answer. Conclude. |

### Slide Layout Rules

- **One step per slide** — each `<section>` covers a single step. This lets the teacher pause and check understanding at each decision point.
- **Header on first slide only** — `True/False Strategy` heading on Slide 1 of the block. Remaining slides show only the step label.
- **Original question in yellow** on first and last slides — `<p style="color:#ffdd00;"><em>"Statement text"</em></p>`
- **Underline step labels** — `<u><strong>Step N:</strong> ...</u>`
- **Real quotes on Step 4** — actual text excerpts from the article, in italics with the relevant phrase highlighted
- **Rule embedded at Step 2** — not a separate slide. Include it: "If you answer Yes to all → TRUE. If you answer No to even one → FALSE."
- **Auto-animate for keyword underlines** — use `data-auto-animate` on a pair of adjacent slides to animate keyword underlines appearing. See pattern below.
- **Teal background** — `data-background-color="#1a6b5a"` + `class="pedagogical"` on all strategy slides.
- **Top alignment** — use `padding-top: 30px` on `.reveal .slides > section.pedagogical` in CSS. Do NOT use negative margins (they clip content off-screen). Inline `style="top: 0;"` on the section element if needed.

### Auto-Animate for Underline Reveal

When a pedagogical slide needs to show key words being underlined (e.g. Step 2 of a strategy: "Underline key words"), use TWO successive `<section>` elements with matching `data-auto-animate`. The first shows the text with transparent borders; the second shows white borders. The transition is triggered by advancing through slides (click/right arrow), NOT by fragments.

**DO NOT use `class="fragment"`** for this purpose. Fragments hide text (`opacity: 0`) which produces blank spaces. Auto-animate between two slides is the correct approach.

Pattern (both sections need `data-auto-animate`):

```html
<!-- Enter state: plain sentence, borders invisible -->
<section class="pedagogical" data-background-color="#1a6b5a" data-background-transition="none" data-auto-animate data-auto-animate-id="underline-demo">
        <div style="overflow: hidden;">
            <p><u><strong>Step 2:</strong> Underline key words</u></p>
            <p data-id="mcq" style="color:#ffdd00;">
                <em>"What is the <span data-id="w1" style="border-bottom: 2px solid transparent;">main message</span>
                of this <span data-id="w2" style="border-bottom: 2px solid transparent;">article</span>?"</em>
            </p>
        </div>
    </section>
    <!-- After click: borders become visible, animate via auto-animate -->
    <section class="pedagogical" data-background-color="#1a6b5a" data-background-transition="none" data-auto-animate data-auto-animate-id="underline-demo">
    <div style="overflow: hidden;">
        <p><u><strong>Step 2:</strong> Underline key words</u></p>
        <p data-id="mcq" style="color:#ffdd00;">
            <em>"What is the <span data-id="w1" style="border-bottom: 2px solid white;">main message</span>
            of this <span data-id="w2" style="border-bottom: 2px solid white;">article</span>?"</em>
        </p>
    </div>
</section>
```

Requirements:
- Both `<section>` elements MUST have `data-auto-animate`
- The `<p>` wrapping the question MUST have a `data-id` attribute (same value on both)
- Each `<span>` wrapping a keyword MUST have a `data-id` attribute (same on both)
- Slide 1 uses `transparent` border color so the text appears plain but the border space is reserved
- Slide 2 uses `white` border color - auto-animate animates the color transition during slide advance
- The previous slide (e.g. Step 1) should NOT have `data-auto-animate` — this prevents unwanted animation between unrelated slides
- Use `data-background-transition="none"` to keep background from animating (teacher controls pacing)

### Auto-Animate for S/V/O Annotation Demonstration

For grammar lead-in slides where you want to demonstrate subjects (S), verbs (V), and objects (O) on a single sentence, use the same two-slide auto-animate pattern but with THREE simultaneous annotations:

- **Subject**: `border-bottom: 2px solid #4fc3f7` (blue single underline) + `<sup style="opacity:0">S </sup>` → `opacity:1; color:#4fc3f7`
- **Verb**: `border-bottom: 2px solid #ff8a65` (orange) + `box-shadow: 0 5px 0 0 #ff8a65` (visual double underline) + `<sup>V </sup>`
- **Object**: `border: 2px solid #aed581` (green box) + `<sup>O </sup>`

Pattern:

```html
<!-- Slide 1 (entry): plain sentence, transparent annotations -->
<section data-auto-animate data-auto-animate-id="svo-demo" data-background-color="#1a1a2e">
    <h2 data-id="title">What's inside a sentence?</h2>
    <p>
        <span data-id="subject" style="border-bottom: 2px solid transparent;">
            <sup style="opacity:0;">S </sup>My roommate
        </span>
        <span data-id="verb" style="border-bottom: 2px solid transparent;">
            <sup style="opacity:0;">V </sup>lost
        </span>
        <span data-id="object" style="border: 2px solid transparent;">
            <sup style="opacity:0;">O </sup>his keys
        </span>
    </p>
</section>
<!-- Slide 2 (annotated): decorations appear via auto-animate CSS transition -->
<section data-auto-animate data-auto-animate-id="svo-demo" data-background-color="#1a1a2e">
    <h2 data-id="title">What's inside a sentence?</h2>
    <p>
        <span data-id="subject" style="border-bottom: 2px solid #4fc3f7;">
            <sup style="color:#4fc3f7;">S </sup>My roommate
        </span>
        <span data-id="verb" style="border-bottom: 2px solid #ff8a65; box-shadow: 0 5px 0 0 #ff8a65;">
            <sup style="color:#ff8a65;">V </sup>lost
        </span>
        <span data-id="object" style="border: 2px solid #aed581; padding: 0 4px; border-radius: 4px;">
            <sup style="color:#aed581;">O </sup>his keys
        </span>
    </p>
</section>
```

This is used for the **lead-in demonstration only** (one sentence). For multi-item practice exercises, use the inline S/V/O annotation with custom fragments (see Key Design Rules) instead — auto-animate would require 2 slides per item, which is impractical.

### Vertical Alignment Fix

Reveal.js `.slides` is a flex container that defaults to vertically centering its section children. To top-align pedagogical slides:

```css
.reveal .slides > section.pedagogical {
    align-self: flex-start;
    margin-top: 0;
    padding-top: 30px;
}
```

Do not use `margin-top: -X%` — it pushes content off-screen. A small positive `padding-top` on the section or its CSS parent is more reliable.

## Slide Icons

Icons are no longer used on slides — they were removed to save screen real estate. All `<i class="fa-solid fa-... slide-icon ...">` elements and their associated CSS (`.slide-icon`, `.transition-icon`, `.pedagogical-icon`, `.objective-icon`) have been removed from all slide templates and the base template. The Font Awesome CDN link may remain in the base template for backwards compatibility but is not actively used. Do not add icons to any slide.

## Dependencies

- Python 3.x, Pillow, requests
- Typst CLI (NOT Quarto-embedded version)
- Roboto OTF fonts (TinyTeX or system)
- `@kilocode/plugin` in `.kilo/` and `.kilocode/` (tool internal, not for edits)
- reveal.js 5.x via CDN (loaded from `templates/base-slides-template.html`, no npm needed)

## Image replacement workflow (frequent task)

When asked to replace a slide background image with a Pixabay URL:

1. **Extract image ID** from the URL — e.g. `1407880` from `https://pixabay.com/photos/men-smoke-grill-picnic-forest-1407880/`
2. **Construct CDN URL** — `https://cdn.pixabay.com/photo/{year}/{month}/{day}/{id}_1280.jpg`  
   (Use the `_1280` variant for good resolution with reasonable size)
3. **Download + compress** using `compress_image()` from `scripts/pixabay_download.py`:
   ```python
   python -c "
   import sys; sys.path.insert(0, 'scripts')
   from pixabay_download import compress_image
   from pathlib import Path
   compress_image('CDN_URL', Path('output/SUBFOLDER/slides/assets/FILENAME.jpg'), ID, 1)
   "
   ```
4. **Place output** in `output/{subfolder}/slides/assets/` (the new pipeline output)
5. **Update HTML** — change the `data-background-image` attribute on the target slide to `assets/FILENAME.jpg`
6. **If no `assets/` dir exists**, create it first

The `compress_image` function applies: resize to 1920px max edge, JPEG quality=80, optimize=True (Pillow).

## Config dirs

- `.kilo/` — session plans, package.json (Kilo internal), and `.kilo/command/` for Kilo CLI commands (e.g., `lint.md`). Skills also live in `.kilo/skills/` (tracked by git).
- `.kilocode/` — legacy skills, node_modules (Kilo internal). **Now gitignored** — switching branches won't delete it anymore
- Skills at `.kilo/skills/<name>/SKILL.md` — new skills require Kilo restart
- Commands at `.kilo/command/<name>.md` — no restart needed

## Windows Path Handling

When processing `file://` URLs containing Windows paths with forward slashes (e.g., `file:///C:/PROJECTS/...`), the `/C:/` is misinterpreted. Use this pattern in Python:

```python
from pathlib import Path
url = url.strip()
if "#" in url:
    url = url.split("#")[0]
url = url.replace("file:///", "")
url = url.replace("file://", "")
path = Path(url)
if not path.exists():
    path = Path(url.replace("/", "\\"))  # Fix forward slashes for Windows
```

Alternatively, convert forward slashes to backslashes:
```python
windows_path = url.replace("/", "\\")
path = Path(windows_path)
```

## Slide Editing Workflow

When the user asks to edit a slide at a reveal.js URL (e.g., `index.html#/7`):

1. **Run `scripts/locate_slide.py`** to determine the slide section:
   ```bash
   python scripts/locate_slide.py "file:///path/to/index.html#/7"
   # OR
   python scripts/locate_slide.py 7 --slides-dir path/to/slides/
   ```
2. The script outputs JSON with slide index, section name, heading, and line numbers
3. Edit `index.html` directly using the line numbers from the output — the slide is a raw HTML `<section>` element
4. No regeneration needed — just reload the browser
5. **When adding a new slide**, insert a new `<section>` element at the correct position in `<div class="slides">`. All subsequent slide indices shift by +1.

### Stable slide IDs — preferred method

**To avoid index confusion**, every `<section>` should have a stable `id` attribute (e.g., `id="slide-title"`, `id="slide-lead-in"`). Unlike numerical indices, IDs don't shift when slides are added or removed.

To locate a slide by its stable ID:
```bash
python scripts/locate_slide.py --id slide-objective --html path/to/slides/index.html
```

The script returns the line numbers and content for that slide regardless of its position in the sequence.

**Naming convention:** Use kebab-case prefixes matching the lesson stage:
- `slide-title`, `slide-objective`
- `slide-lead-in`, `slide-diagnosis-reveal`
- `slide-pet-scale-1`, `slide-pet-scale-2`
- `slide-test1-{range}` (e.g., `slide-test1-1-3`)
- `slide-test2-entry`, `slide-test2-reveal`
- `slide-transition-{target}` (e.g., `slide-transition-learn`)
- `slide-teach-{topic}` (e.g., `slide-teach-sentence-def`, `slide-teach-commands`)
- `slide-quick-check`
- `slide-transition-{topic}` (e.g., `slide-transition-capitals`)
- `slide-cap-rules-1-3`, `slide-cap-rules-4-6`
- `slide-did-you-know`
- `slide-p2b-task`, `slide-p2b-answers-{range}`
- `slide-p7-task`, `slide-p7-corrected-{range}`
- `slide-summary`, `slide-end`

## reveal.js Codebase

When making changes to reveal.js code (e.g., custom themes, configuration, or plugin modifications), **always query the live GitHub repository first**. Do not rely on static snapshots — the live codebase is the source of truth.

### Query Live reveal.js via Git

Use `gh` (GitHub CLI) to fetch individual files from the live repository. This is faster than cloning and always returns the current version.

```bash
# Get a specific file from the latest version
gh api repos/hakimel/reveal.js/contents/css/reveal.scss --jq '.content' | base64 -d

# Get the compiled CSS
gh api repos/hakimel/reveal.js/contents/dist/reveal.css --jq '.content' | base64 -d

# Get the main JS source
gh api repos/hakimel/reveal.js/contents/js/reveal.js --jq '.content' | base64 -d | head -200

# List the top-level directory structure
gh api repos/hakimel/reveal.js/contents/ --jq '.[].name'

# Search the codebase for a specific pattern (uses GitHub code search)
gh search code "data-auto-animate" --repo hakimel/reveal.js --limit 10

# Get a file from a specific tag/version
gh api repos/hakimel/reveal.js/contents/css/reveal.scss?ref=5.1.0 --jq '.content' | base64 -d
```

To see how a specific feature works (e.g., `autoAnimateUnmatched`), search the JS source:
```bash
gh api repos/hakimel/reveal.js/contents/js/reveal.js --jq '.content' | base64 -d | Select-String -Pattern "autoAnimateUnmatched" -Context 0,5
```

## Known CSS Conflicts with reveal.js

### Fragment `highlight-*` classes set `opacity: 1`

**Problem:** reveal.js built-in CSS forces `opacity: 1; visibility: inherit` on `.highlight-green`, `.highlight-red`, and `.highlight-blue` at all times. These classes are designed for color-change-on-reveal, not hide-reveal. Using `class="fragment highlight-green"` will NOT hide the element — it stays visible, only changing color when `.visible` is added.

**Evidence from compiled `reveal.css`:**
```css
.reveal .fragment.highlight-green{opacity:1;visibility:inherit}
.reveal .fragment.highlight-red{opacity:1;visibility:inherit}
/* .visible only changes color, not opacity: */
.reveal .fragment.highlight-green.visible{color:#17ff2e}
```

**Solution:** Use custom CSS classes that only apply on `.visible`:
```css
.reveal .fragment.answer-correct.visible {
    background: rgba(0, 120, 0, 0.5);
    padding: 0.3em 0.5em;
    border-radius: 4px;
}
.reveal .fragment.answer-incorrect.visible {
    background: rgba(120, 0, 0, 0.5);
    padding: 0.3em 0.5em;
    border-radius: 4px;
}
```
Then use `class="fragment answer-correct"` — the element starts hidden (default fragment behavior) and only gains background on click.

**To verify:** Check the compiled `reveal.css` from CDN for fragment CSS rules:
```bash
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" -OutFile "$env:TEMP\reveal.css"
Select-String -Path "$env:TEMP\reveal.css" -Pattern "fragment" -SimpleMatch
```
