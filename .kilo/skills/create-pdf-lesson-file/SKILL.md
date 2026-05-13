---
name: create-pdf-lesson-file
description: Converts a lesson plan JSON file to a formatted PDF using Typst CLI and Jinja2 templating.
---

# Skill: Create PDF Lesson File

## Purpose
Convert lesson plan JSON files to professionally formatted PDFs using Typst CLI with Roboto font, logo header, and structured lesson information.

## Workflow

### Step 1: Validate Input
- Check that the JSON file exists
- Parse and validate against required schema:
  - `teacher`, `duration`, `date`, `topic`, `materials`
  - `lesson_plan.shape`, `lesson_plan.shape_name`, `lesson_plan.cefr_level`, `lesson_plan.class`, `lesson_plan.stages`
  - Each stage must have: `stage_number`, `stage`, `stage_aim`, `procedure`, `time`, `interaction`
- Halt on first validation error with descriptive message

### Step 2: Process Content
- If `answer_key` is a file path to a `.md` file, read its contents
- If `transcript` is a file path to a `.md` or `.txt` file, read its contents
- Convert markdown content to Typst markup (headings, bold, italic, bullet lists)
- Format date from `DDMMYY` or `YYMMDD` to `D Month, YYYY`
- Humanize robotic stage aims (e.g., "To reading for gist" → "To get the general idea of the text")
- Strip minute indicators from procedure text (e.g., "3 min.", "2 min.")

### Step 3: Render Template
- Use Jinja2 to fill `templates/lesson-plan-template.typ` with processed data
- Template produces:
  - Page 1 header with Cambridge and ACT logos, title "Lesson Plan"
  - Lesson Information: Topic line, then table (Teacher, Date, Class, Duration, CEFR, Shape, Materials, Slideshow URL)
  - Lesson Aim box with left border
  - Lesson Stages table (Time, Goal, Procedure, Interaction)
  - Answer Key and Transcript sections on page breaks

### Step 4: Render PDF with Typst
- Copy logo images to temp directory alongside the `.typ` file
- Run: `typst compile <temp.typ> <output.pdf> --font-path <roboto_dir>`
- Output path: `PDF/{input_subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`
- Clean up temporary `.typ` file and copied images after rendering

### Step 5: Confirm Output
- Report success with output file path
- Report any errors with details

## File Locations
- **Template:** `C:\PROJECTS\LESSON PLAN WRITER 3\templates\lesson-plan-template.typ`
- **Script:** `C:\PROJECTS\LESSON PLAN WRITER 3\scripts\json_to_pdf.py`
- **Logos:** `C:\PROJECTS\LESSON PLAN WRITER 3\templates\Image_20260324_141022.png` (ACT), `1135082720.png` (Cambridge)
- **Roboto fonts:** `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\`
- **Output:** `C:\PROJECTS\LESSON PLAN WRITER 3\PDF\{subfolder}\{mmddyy}-{topic}-lesson-plan.pdf`

## Usage
```bash
python scripts/json_to_pdf.py <json_file_path> [--output-dir <dir>]
```

## Dependencies
- Python 3.x
- Jinja2 (`pip install jinja2`)
- Typst CLI (v0.13+)
- Roboto OTF fonts (in TinyTeX or system)
- pytest (`pip install pytest`) for running tests

## Testing
Run tests with:
```bash
cd C:\PROJECTS\LESSON PLAN WRITER 3
python -m pytest tests/test_json_to_pdf.py -v
```

## Notes
- Black and white formatting only
- Logos appear only on page 1 header
- Roboto font used throughout
- Topic names normalized for filenames: lowercase, spaces to hyphens
- Date format in filename: mmddyy (no hyphens)
- Filename suffix: `-lesson-plan` (e.g. `051226-what-connects-us-lesson-plan.pdf`)
- Fails fast on any error - does not continue on validation failure

## Typst Syntax — Avoid Hallucination

When modifying the template or debugging Typst compile errors:

1. **Load the `typst-author` skill** for accurate syntax references and examples
2. **Search local docs** (`.kilocode/skills/typst-author/docs/`) before writing any Typst code
3. **Follow read-edit-compile-check**: make a change, run `python scripts/json_to_pdf.py ...`, read errors, fix
4. **Never guess Typst syntax** — models hallucinate heavily on Typst

Key pitfalls:
- `#set par(leading: Xem)` is **additional** spacing, not a line-height multiplier
- `#set text(font: "Roboto")` requires `--font-path` pointing to actual OTF files
- `context { if counter(page).get().first() == 1 { ... } }` for conditional page-1 headers
- `table.cell(colspan: N)` merges N columns, consuming only one cell position in the row
