---
description: Converts a lesson plan JSON file to a formatted PDF using Typst CLI. Loads the create-pdf-lesson-file skill and runs json_to_pdf.py.
---

# Command: Create PDF Lesson File

## Usage
`/create-pdf-lesson-file <json_path>`

Accepts a lesson plan JSON path (relative or absolute) and generates a PDF in `PDF/{subfolder}/`.

## What it does
1. Loads the `create-pdf-lesson-file` skill
2. Validates the JSON file exists and meets the required schema
3. Processes content: dates, stage aims, answer keys, transcripts
4. Generates .typ markup via Python `build_typ_content()`, then compiles with `typst compile` using logo header and Roboto font
5. Outputs PDF to `PDF/{input_subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`

## Prerequisites
- Typst CLI installed (`typst compile` — NOT Quarto-embedded version)
- Roboto OTF fonts in TinyTeX or system fonts
- Python 3.x (standard library — no extra packages required)
- Logos at `templates/Image_20260324_141022.png` and `templates/1135082720.png`

## Workflow

### Step 1: Load the skill
`skill create-pdf-lesson-file`

This loads the full skill instructions including validation rules, content transforms, and template rendering details.

### Step 2: Parse the argument
Extract the `<json_path>` argument. Resolve relative paths against the project root (`C:\PROJECTS\LESSON PLAN WRITER 3`).

```powershell
$jsonPath = Resolve-Path $args[0] -ErrorAction Stop
```

If no argument or the file doesn't exist, abort with error.

### Step 3: Validate JSON
Check the JSON file exists and has the required schema:
- `teacher`, `duration`, `date`, `topic`, `materials`
- `lesson_plan.shape`, `lesson_plan.shape_name`, `lesson_plan.cefr_level`, `lesson_plan.class`, `lesson_plan.stages[]`
- Each stage: `stage_number`, `stage`, `stage_aim`, `procedure`, `time`, `interaction`

Halt on first validation error.

### Step 4: Run the PDF script
```powershell
python scripts/json_to_pdf.py $jsonPath
```

### Step 5: Report output
On success, report the output path:
```
PDF/{subfolder}/{mmddyy}-{topic}-lesson-plan.pdf
```

On failure, show the error output from Typst or the script.

## Edge cases
- **JSON path not provided**: "Error: JSON file path required — usage: /create-pdf-lesson-file <path>"
- **JSON missing required fields**: Validation error with the specific missing field
- **Answer key path not found**: Warn and fallback to "none"
- **Typst compile fails**: Print stdout/stderr from the compiler
- **Output directory doesn't exist**: Created automatically by the script
