---
description: Converts a lesson plan JSON into a reveal.js presentation using raw HTML section elements. Copies the base template from templates/base-slides-template.html and hand-builds all slides as <section> elements. Markdown pipeline is permanently abandoned.
---

# Command: Lesson Plan to reveal.js

## Usage
`/lesson-plan-to-reveal <json_path>`

Accepts a lesson plan JSON path and generates an `index.html` slideshow in `output/{subfolder}/slides/`.

## What it does
1. Loads the `lesson-plan-to-reveal` skill for full slide design rules
2. Creates `output/{subfolder}/slides/` and `assets/` directories
3. Copies `templates/base-slides-template.html` → `index.html`
4. Copies institution logo to `assets/logo.png`
5. Builds all slides as raw HTML `<section>` elements between `<div class="slides">` and `</div>`
6. Reports the output path — open directly in browser (no server needed)

## Prerequisites
- Python 3.x with Pillow
- Institution logo at `templates/Image_20260324_141022.png`

## Workflow

### Step 1: Load the skill
`skill lesson-plan-to-reveal`

This loads all slide design rules: icon mapping, fragment policy, vocabulary layout, pedagogical slides, auto-animate patterns, answer tables, and B1 audience guidelines.

### Step 2: Parse the argument
Extract `<json_path>`. Resolve relative paths against project root. If no argument or file missing, abort.

```powershell
$jsonPath = Resolve-Path $args[0] -ErrorAction Stop
```

### Step 3: Extract subfolder from JSON path
The JSON path determines the output subfolder:
- E.g. `output/Term-1-Intro/051226-welcome-to-term-1-lesson-plan.json` → subfolder = `Term-1-Intro`
- Output dir: `output/{subfolder}/slides/`

### Step 4: Create output directories
```powershell
mkdir -p "output/{subfolder}/slides/assets"
```

### Step 5: Copy base template
```powershell
cp "templates/base-slides-template.html" "output/{subfolder}/slides/index.html"
```

### Step 6: Copy logo
```powershell
python -c "import shutil; shutil.copy('templates/Image_20260324_141022.png', 'output/{subfolder}/slides/assets/logo.png')"
```

### Step 7: Build slides
Read the lesson plan JSON. Build `<section>` elements following the skill's design rules:

| Slide | Content source |
|---|---|
| Title | Topic + CEFR + strap from objective |
| Objective | 3 outcomes from lesson objective |
| Lead-in | Open question from materials |
| Vocabulary | Key terms extracted from materials |
| Transitions | Stage transitions with directive + foreshadow |
| Pedagogy blocks | Strategy slides (T/F, Matching, MC) |
| Task instructions | Procedure text (student-facing only) |
| Answer slides | Answer key with fragment reveals |
| Post-reading | Discussion questions |
| Summary | "I can..." statements |
| End | Topic + CEFR |

Insert all `<section>` elements between `<div class="slides">` and `</div>` in `index.html`.

### Step 8: Verify output
- Check `output/{subfolder}/slides/index.html` exists
- Verify `<img src="assets/logo.png" class="title-logo">` in title slide
- Verify Font Awesome CDN link is present (from base template)
- Verify `autoAnimateUnmatched: true` in `Reveal.initialize()`
- Open in browser to verify visually

## Slide Design Rules Summary
See loaded skill for full details. Key constraints:
- **No markdown** — all slides are raw `<section>` elements
- **One step per slide** for pedagogical strategy blocks
- **Icons** only on first slide of each block (per icon mapping table in skill)
- **CEFR badge** on title slide with level-specific color
- **Vocabulary**: one word per slide, `#1a1a2e` background, yellow `<span class="vocab-word">`
- **Transitions**: red `#c0392b` background, directive + foreshadow
- **Answer tables**: 3 columns (Statement / Answer / Why?), fragment reveals
- **No automatic Pixabay downloads** — solid colors only
- **B1 audience**: direct "you" imperatives, ≤15 words per sentence, no passive voice

## Edge cases
- **No JSON path**: "Error: JSON file path required — usage: /lesson-plan-to-reveal <path>"
- **Missing base template**: "Error: templates/base-slides-template.html not found"
- **Output dir already exists**: Overwritten (backup not needed — git tracks source)
- **JSON with missing fields**: Abort with validation error listing missing fields
