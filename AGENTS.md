# AGENTS.md — Lesson Plan Writer 3

## Two pipelines

### PDF (2-stage)
1. **`write-lesson-plan` skill** → `output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json`
2. **`create-pdf-lesson-file` skill** → converts JSON → `PDF/{subfolder}/{mm-dd-yy}-{topic}.pdf`

### Slides (2-stage)
1. **`write-lesson-plan` skill** → JSON (same as above)
2. **`lesson-plan-to-reveal` skill** → `scripts/json_to_markdown.py <json_path>` → generates `slides.md` + `index.html` in `output/{subfolder}/slides/`
3. **`publish-to-github-pages` skill** → deploys `output/{subfolder}/slides/` to gh-pages

## Key commands

```bash
# PDF (from project root)
python scripts/json_to_pdf.py output/<subfolder>/<file>.json

# Slides — convert JSON to markdown + self-contained HTML
python scripts/json_to_markdown.py output/<subfolder>/<file>.json
# Then open output/<subfolder>/slides/index.html directly in browser (no server needed)

# Partial update — regenerate specific sections only
python scripts/json_to_markdown.py output/<subfolder>/<file>.json --section title,vocab --merge

# Pixabay image download (for slide backgrounds)
python scripts/pixabay_download.py --query "topic" --type image --count 3

# Tests (41 total, all pass)
python -m pytest tests/ -v
python -m pytest tests/test_json_to_pdf.py -v       # 18 tests
python -m pytest tests/test_json_to_markdown.py -v  # 23 tests
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

- `templates/slides-template.html` — standalone reveal.js HTML template with CDN, inlines markdown
- `PIXABAY_API_KEY` env var required for background images (falls back to gradients if unset)

## Dependencies

- Python 3.x + Jinja2, Pillow, requests
- Typst CLI (NOT Quarto-embedded version)
- Roboto OTF fonts (TinyTeX or system)
- `@kilocode/plugin` in `.kilo/` and `.kilocode/` (tool internal, not for edits)
- reveal.js 5.x via CDN (loaded from `templates/slides-template.html`, no npm needed)

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
