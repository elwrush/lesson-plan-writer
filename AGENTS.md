# AGENTS.md — Lesson Plan Writer 3

## Two pipelines

### PDF (2-stage)
1. **`write-lesson-plan` skill** → `output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json`
2. **`create-pdf-lesson-file` skill** → converts JSON → `PDF/{subfolder}/{mm-dd-yy}-{topic}.pdf`

### Slides (3-stage)
1. **`write-lesson-plan` skill** → JSON (same as above)
2. **`lesson-plan-to-reveal` skill** → `scripts/json_to_markdown.py <json_path>` → markdown in `output/{subfolder}/slides/`
3. **`publish-to-github-pages` skill** → `python -m mkslides build "output/{subfolder}/slides" -d "output/{subfolder}/site"` then deploys to gh-pages

## Key commands

```bash
# PDF (from project root)
python scripts/json_to_pdf.py output/<subfolder>/<file>.json

# Slides — convert JSON to markdown, then build site
python scripts/json_to_markdown.py output/<subfolder>/<file>.json
python -m mkslides build "output/<subfolder>/slides" -d "output/<subfolder>/site"

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

- `mkslides.yml` at root configures reveal.js theme (white), 1280×720, slide numbers
- `templates/reveal-custom.html.jinja` customizes slide CSS
- `PIXABAY_API_KEY` env var required for background images (falls back to gradients if unset)

## Dependencies

- Python 3.x + Jinja2, Pillow, requests
- Typst CLI (NOT Quarto-embedded version)
- Roboto OTF fonts (TinyTeX or system)
- `@kilocode/plugin` in `.kilo/` and `.kilocode/` (tool internal, not for edits)

## Config dirs (do not edit manually)

- `.kilo/` — session plans, package.json (Kilo internal)
- `.kilocode/` — skills, node_modules (Kilo internal)
- Skills at `.kilocode/skills/<name>/SKILL.md` — new skills require Kilo restart
