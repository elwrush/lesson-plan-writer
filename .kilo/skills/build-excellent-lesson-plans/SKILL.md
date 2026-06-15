# Skill: build-excellent-lesson-plans

## Purpose
Generate professional lesson plan PDFs from Markdown using the three-layer Markdown → Pandoc → Typst → PDF pipeline.

## Pipeline
```
Agent writes lesson.md → build_lesson_pdf.py (validates + Pandoc + Lua filter + Typst + lint) → PDF
```

## Architecture

| Layer | What | Who writes |
|---|---|---|
| `templates/lesson-plan.typ` | Typst page setup, masthead, info table, aim block. `$body$` for content. | Developer, once, hash-locked |
| `scripts/lesson-tables.lua` | Pandoc Lua filter — reads `## Stage N:` headings from the body and generates a Typst `#table()` with colored headers. | Developer, once |
| `scripts/build_lesson_pdf.py` | Validates Markdown, runs Pandoc with template + Lua filter, compiles Typst, lints PDF, appends answer key/transcript if present. | Developer, once |
| `lesson.md` | YAML frontmatter (metadata) + Markdown body (stages, materials). **No Typst code, no HTML, no JSON.** | Agent, every lesson |

## Key conventions

- **Duration:** Standard lesson is 46 minutes. Total stage times must always match stated duration.
- **Stage numbering:** Sequential from 1. No gaps.
- **Output location:** Input `.md` in `output/{subfolder}/` → PDF in `PDF/{subfolder}/`.
- **Stages in Markdown body, not YAML.** YAML frontmatter is for simple metadata strings only. The Lua filter reads `## Stage N:` headings and builds the stage table.

## Workflow

### Step 1: Write a lesson plan in Markdown

Create a `.md` file in `output/{subfolder}/` with YAML frontmatter for metadata and Markdown body for stages.

**YAML frontmatter fields:**

```yaml
---
topic: "Gender Stereotypes and Gen Z"
teacher: "Ed Rush"
formatted_date: "15 June, 2026"
duration: "46 minutes"
cefr_level: "B2"
class: "M3"
shape: "G"
shape_name: "Task-Based Learning"
materials:
  - "BTN video (Episode 15)"
  - "YouTube clip: Andrew Tate (https://www.youtube.com/watch?v=...)"
  - "Slide deck"
slideshow_url: "https://example.com/slides"
main_aim: "By the end of the lesson, learners will have..."
subsidiary_aim: "Learners will also have practiced..."
transcript: "output/.../transcript_tate.typ"
---

= Lesson Stages

## Stage 1: Stage Name

**Time:** 5 min  |  **Interaction:** T-Ss

**Aim:** Natural English aim description

- Bullet point each step
- Keep procedures concise
- No blank lines between bullet items

## Stage 2: Next Stage
...
```

**Optional YAML fields:**
- `transcript` — path to a `.typ` transcript file. If present, appended to the PDF after the stages.
- `answer_key` — path to a `.typ` answer key file. Only include when the lesson actually has an answer key. If absent, no answer key header appears.
- `slideshow_url` — URL of the lesson slideshow. Renders as a gray-shaded row in the info table.

**Stage aim style:** Write aims in natural English. Vary sentence openers. Avoid robotic templates like "To lead-in" or "To reading for gist".

**Procedure style:** One dash per action step. No blank lines between bullets. Keep concise — the teacher has the lesson plan, they don't need full exercise instructions reproduced.

### Step 2: Generate the PDF

```powershell
python scripts/build_lesson_pdf.py output/{subfolder}/lesson.md
```

This validates the Markdown, runs Pandoc with `templates/lesson-plan.typ` and `scripts/lesson-tables.lua`, compiles via Typst, appends any answer key or transcript, and lints the PDF.

Output: `PDF/{subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`

### Step 3: Review

Open the PDF and check:
- Masthead (Cambridge logo · C·E·L Mathayom · ACT logo)
- Info table: teacher, date, class, duration, CEFR, shape, materials, slideshow URL (gray-shaded)
- Lesson aims with left accent bar (main aim bold, subsidiary aim bold)
- Stage table with colored headers (luma(230) fill) and four columns: Time, Goal, Procedure, Int
- Total timing matches duration
- Aims are natural English
- Bullet points render correctly throughout

## Key principles

- **Agent writes Markdown** — no Typst, no HTML, no JSON. Pandoc + Lua filter handle the conversion.
- **Lua filter builds the table** — `scripts/lesson-tables.lua` scans `## Stage N:` headings and generates the Typst `#table()`. No YAML `stages` arrays needed.
- **Template is locked** — `templates/lesson-plan.typ` is hash-verified. Changes require deleting `.template-lock.json`.
- **Optional appendices** — answer key and transcript are only appended when the corresponding YAML field is present. Headers appear inline, not on separate pages.
- **No inline `python -c`** — all operations use permanent `.py` files in `scripts/`.
