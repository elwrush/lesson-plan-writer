# AGENTS.md — Lesson Plan Writer 3

## Environment

- **OS:** Windows AMD64 (win32 sys.platform)
- **Shell:** PowerShell
- **Python:** 3.x

## Two pipelines

### PDF (2-stage)
1. **`write-lesson-plan` skill** → `output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json`
2. **`create-pdf-lesson-file` skill** → converts JSON → `PDF/{subfolder}/{mm-dd-yy}-{topic}.pdf`

### Slides (template-based)
1. **`write-lesson-plan` skill** → JSON (same as above)
2. **`lesson-plan-to-reveal` skill** → copies `templates/base-slides-template.html` → hand-builds `index.html` with raw HTML `<section>` elements in `output/{subfolder}/slides/`
3. **`publish-to-github-pages` skill** → deploys `output/{subfolder}/slides/` to gh-pages

**Markdown pipeline is permanently abandoned.** All slides are raw HTML `<section>` elements. `scripts/json_to_markdown.py` is deprecated — do not use for new presentations. Auto-animate requires sibling `<section data-auto-animate>` elements, which cannot be produced from the markdown plugin.

## Key commands

```bash
# PDF (from project root)
python scripts/json_to_pdf.py output/<subfolder>/<file>.json

# Slides — copy base template + hand-build sections
cp "templates/base-slides-template.html" "output/<subfolder>/slides/index.html"
# Then add raw HTML <section> elements between <div class="slides"> and </div>
# Open output/<subfolder>/slides/index.html directly in browser (no server needed)

# Pixabay image download (for slide backgrounds)
python scripts/pixabay_download.py --query "topic" --type image --count 3

# Tests (41 total, all pass)
python -m pytest tests/ -v
python -m pytest tests/test_json_to_pdf.py -v       # 18 tests
python -m pytest tests/test_json_to_markdown.py -v  # 23 tests

# Locate slide by reveal.js index (deterministic editing)
python scripts/locate_slide.py "file:///path/to/index.html#/7"
python scripts/locate_slide.py 7 --slides-dir path/to/slides/
```

## JSON schema

- Top-level: `teacher`, `duration`, `date` (DDMMYY), `topic`, `materials`, `lesson_plan`
- `lesson_plan` keys: `shape`, `shape_name`, `cefr_level`, `class`, `stages[]`
- Each stage: `stage_number`, `stage`, `stage_aim`, `procedure`, `time`, `interaction`
- Optional top-level: `transcript`, `answer_key`, `cefr_level`, `class`, `objective`
- `answer_key` value: `"none"`, or a Windows absolute `.md` path (script reads file at render time)
- **`lesson_plan` and `answer_key` use underscore** (not hyphen). The test fixture has a bug — uses `answer-key` — ignore it; production JSON always uses `answer_key`.
- Shape templates (A–G) at `knowledge-base/lesson plan shapes/json/shape-{letter}.json`

## PDF rendering (Typst)

- Renderer: `typst compile` (NOT Quarto — abandoned, it ignored `format: typst`)
- Template: `templates/lesson-plan-template.typ` (Jinja2 + Typst)
- Font: Roboto OTF from `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\` via `--font-path`
- Logos: `templates/Image_20260324_141022.png` (ACT), `templates/1135082720.png` (Cambridge) — page 1 only via `context { if counter(page).get().first() == 1 { ... } }`
- Top margin: 1.25in (prevents logo clipping on print)
- Line spacing: `#set par(leading: 0.55em)` — leading is **additional** space, not a multiplier

## Content transforms (in json_to_pdf.py)

- Date: `050726` → `7 May, 2026`
- Stage aims: robotic templates humanized (e.g. "To reading for gist" → "To understand the general idea of the text")
- Procedure: minute indicators stripped (`3 min.` → ``)
- Answer key markdown → Typst markup (`#`→`=`, `**bold**`→`*bold*`, bullet lists, `---`→`#line`)
- Windows paths: `\` → `/` for Typst

## Language quality

Stage aims must read as natural English, not template fills. Unacceptable:
- "To lead-in to the topic of..."
- "To reading for gist"
- "To post-reading speaking task"

Acceptable: "To activate interest in...", "To get the general idea of the text", "To discuss ideas from the reading"

## Slide design reference

`docs/slide-design-reference.md` defines slide types (vocabulary, task, answer, transition), fragment policy, auto-animate rules, and Pixabay image strategy. The `json_to_markdown.py` script reads this doc at generation time.

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
- **Teal background** — `data-background="#1a6b5a"` + `class="pedagogical"` on all strategy slides.
- **Top alignment** — use `padding-top: 30px` on `.reveal .slides > section.pedagogical` in CSS. Do NOT use negative margins (they clip content off-screen). Inline `style="top: 0;"` on the section element if needed.

### Auto-Animate for Underline Reveal

When a pedagogical slide needs to show key words being underlined (e.g. Step 2 of a strategy: "Underline key words"), use TWO successive `<section>` elements with matching `data-auto-animate`. The first shows the text with transparent borders; the second shows white borders. The transition is triggered by advancing through slides (click/right arrow), NOT by fragments.

**DO NOT use `class="fragment"`** for this purpose. Fragments hide text (`opacity: 0`) which produces blank spaces. Auto-animate between two slides is the correct approach.

Pattern (both sections need `data-auto-animate`):

```html
<!-- Enter state: plain sentence, borders invisible -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" data-auto-animate>
    <div style="overflow: hidden;">
        <p><u><strong>Step 2:</strong> Underline key words</u></p>
        <p data-id="mcq" style="color:#ffdd00;">
            <em>"What is the <span data-id="w1" style="border-bottom: 2px solid transparent;">main message</span>
            of this <span data-id="w2" style="border-bottom: 2px solid transparent;">article</span>?"</em>
        </p>
    </div>
</section>
<!-- After click: borders become visible, animate via auto-animate -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" data-auto-animate>
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

## Slide Icons — Font Awesome 6

All slides use Font Awesome 6 icons via CDN to visually signal slide function. Icons are placed at the top of the slide, centered, before the heading.

**Add CDN once** in the `<head>` of the base template:
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
```

**CSS** (in `<style>` block):
```css
.slide-icon {
    font-size: 2.5em;
    margin-bottom: 0.3em;
    display: block;
    text-align: center;
}
.transition-icon  { color: rgba(255,255,255,0.85); }  /* red bg slides    */
.pedagogical-icon { color: rgba(255,255,255,0.9);  }  /* teal bg slides   */
.objective-icon   { color: rgba(255,221,0,0.85);    }  /* white bg slides */
```

**Icon mapping** — one icon on the first slide of each block, before the `<h2>`:

| Slide / Block | Icon | Class | Background |
|---|---|---|---|
| Objective: "Here's what you'll be able to do" | `fa-seedling` | `objective-icon` | white |
| Lead-in: "Let's get Started" | `fa-eye` | inherit | Pixabay image |
| Vocabulary: "Important Words" | `fa-spell-check` | inherit | Pixabay image |
| Transition (forward to next stage) | `fa-forward` | `transition-icon` | `#c0392b` |
| True/False Strategy block header | `fa-list-check` | `pedagogical-icon` | `#1a6b5a` |
| Strategy step slides (Steps 1–4) | `fa-chess` | `pedagogical-icon` | `#1a6b5a` |
| Multiple Choice Strategy block | `fa-list-check` | `pedagogical-icon` | `#1a6b5a` |
| Task instruction | `fa-pencil` | inherit | white |
| Discussion ("Let's Discuss") | `fa-comments` | `transition-icon` | `#c0392b` |
| Summary ("What you can do now") | `fa-flag-checkered` | inherit | white |
| End ("Thank you") | `fa-star` | inherit | `#2c3e50` |

**Placement pattern:**
```html
<section data-background="#c0392b">
    <i class="fa-solid fa-forward slide-icon transition-icon"></i>
    <h2>Finding details</h2>
    ...
</section>
```

For strategy blocks, the icon appears on the **first slide only** (the block header). Subsequent step slides in the same block do not show an icon.

**Key rule**: The icon describes the *function* of the slide, not the topic. A transition moves forward; a discussion invites talking; a strategy teaches a step-by-step method.

## Dependencies

- Python 3.x + Jinja2, Pillow, requests
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

## Config dirs (do not edit manually)

- `.kilo/` — session plans, package.json (Kilo internal)
- `.kilocode/` — skills, node_modules (Kilo internal)
- Skills at `.kilocode/skills/<name>/SKILL.md` — new skills require Kilo restart

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

This prevents the agent from editing the wrong slide due to index confusion.

## reveal.js Codebase

When making changes to reveal.js code (e.g., custom themes, configuration, or plugin modifications), **always use the global repomix skill to query the stored reveal.js codebase first**.

### Query Stored reveal.js

The packed reveal.js codebase is stored at: `knowledge-base\revealjs-packed.json`

```bash
# Load and query the packed JSON
$json = Get-Content "knowledge-base\revealjs-packed.json" | ConvertFrom-Json

# List all files
$json.files.PSObject.Properties.Name | Sort-Object

# Get specific file content
$json.files.'js/reveal.js'
$json.files.'css/reveal.scss'
$json.files.'css/theme/white.scss'

# Search for specific code
$json.files.PSObject.Properties | Where-Object { $_.Value -match "transition" }
```

### Update reveal.js Pack

To update the stored codebase when reveal.js releases a new version:

```bash
repomix --remote https://github.com/hakimel/reveal.js --style json --output knowledge-base\revealjs-packed.json --top-files-len 15
```

### Global Repomix Skill

See: `C:\Users\elwru\.kilo\skills\repomix-codebase-search\SKILL.md`
