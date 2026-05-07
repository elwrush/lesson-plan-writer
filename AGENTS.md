# AGENTS.md — Lesson Plan Writer 3

## Two-stage pipeline

1. **`write-lesson-plan` skill** → creates `output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json`
2. **`create-pdf-lesson-file` skill** → converts JSON → `PDF/{subfolder}/{mm-dd-yy}-{topic}.pdf`

Skills are at `.kilocode/skills/<name>/SKILL.md`. New skills only appear after Kilo restart.

## Key commands

```bash
# Convert JSON to PDF
python scripts/json_to_pdf.py output/<subfolder>/<file>.json

# Run tests (18 tests)
python -m pytest tests/test_json_to_pdf.py -v
```

## JSON schema pitfalls

- `lesson_plan` uses **underscore**, not hyphen
- `answer_key` uses **underscore**, not `answer-key`
- Top-level fields: `teacher`, `duration`, `date`, `topic`, `materials`, `lesson_plan`
- Optional: `transcript`, `answer_key`, `cefr_level`, `class`
- `answer_key` can be a file path (`.md`) or `"none"` — script reads file contents at render time
- Date in JSON: `DDMMYY` string (e.g. `"050726"`)

## PDF rendering (Typst, not Quarto)

- Renderer: **`typst compile`**, not `quarto render`. Quarto was tried and abandoned — it ignored `format: typst` and fell back to LaTeX.
- Template: `templates/lesson-plan-template.typ` (Jinja2 with Typst markup)
- Font: Roboto OTF from `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\` via `--font-path`
- Logos: `templates/Image_20260324_141022.png` (ACT) and `templates/1135082720.png` (Cambridge) — both PNG
- Line spacing: `#set par(leading: 0.55em)` — Typst's `leading` is **additional** space, not a multiplier
- Logos only on page 1 via `context { if counter(page).get().first() == 1 { ... } }`
- Top margin: 1.25in to prevent logo clipping on print

## Content transforms in json_to_pdf.py

Script applies these transforms before rendering:
- **Date format**: `050726` → `7 May, 2026`
- **Stage aims**: humanized from robotic templates (e.g. "To reading for gist" → "To get the general idea of the text")
- **Procedure text**: minute indicators stripped (e.g. `3 min.`, `2 min.`)
- **Answer key markdown**: converted to Typst (`#`→`=`, `**bold**`→`*bold*`, bullet lists, horizontal rules)
- **Windows paths**: `\` → `/` for Typst compatibility

## Language quality

Stage aims must be natural English, not deterministic template fills. Examples of **unacceptable** output:
- "To lead-in to the topic of..."
- "To reading for gist"
- "To post-reading speaking task"

Acceptable: "To activate interest in...", "To get the general idea of the text", "To discuss ideas from the reading"

## Dependencies

- Python 3.x + Jinja2
- Typst CLI (installed separately, NOT the Quarto-embedded version)
- Roboto OTF fonts (via TinyTeX or system)
- No LaTeX, no Quarto needed
