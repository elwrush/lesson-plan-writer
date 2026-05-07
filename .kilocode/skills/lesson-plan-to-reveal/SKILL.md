---
name: lesson-plan-to-reveal
description: Converts a lesson plan JSON file into a reveal.js presentation using mkslides. Generates pedagogical ESL slides following the design rules in docs/slide-design-reference.md. Builds to static HTML via mkslides.
---
# Skill: Lesson Plan to reveal.js Presentation

## Purpose
Convert a lesson plan JSON into a reveal.js slideshow for ESL classroom delivery. The teacher controls all slides — students never interact directly. Slides support the teacher's narration, not replace it.

**Pipeline**: JSON → markdown (`json_to_markdown.py`) → mkslides build → `site/index.html`

**Slide design authority**: `docs/slide-design-reference.md` — this file defines all slide types, fragment policies, text limits, and vocabulary rules. The Python script reads this reference at generation time.

## When to Use This Skill

Use `lesson-plan-to-reveal` when converting a lesson plan JSON to slides. The skill:
1. Runs `scripts/json_to_markdown.py` to generate markdown
2. Runs `python -m mkslides build` to generate HTML
3. Reports the output path

## Workflow

### Step 1: Validate input
- Verify lesson plan JSON exists and parses
- Validate required fields: `teacher`, `duration`, `date`, `topic`, `materials`, `lesson_plan.stages`
- Read answer key from `answer_key` field (`.md` file or "none")

### Step 2: Generate markdown
```bash
python scripts/json_to_markdown.py output/{subfolder}/{file}.json
```
Output: `output/{subfolder}/slides/{mmddyy}-{topic}-slides.md`

The script generates slides following `docs/slide-design-reference.md`:
- Title + CEFR badge + gradient background
- Objective slide — 3 outcomes, all visible at once
- Vocabulary slide — 3-5 CEFR-appropriate words with phonemic script + example sentences
- Lead-in — Pixabay background image + open question
- Pre-reading prediction — article title + 2 prompts
- Task instruction — brief numbered steps, full procedure in speaker notes
- Answer explanation — answers with fragment reveal + explanation + source citation
- Section transitions — red backgrounds between stages
- Post-reading discussion — all questions visible
- Summary — "What you can do now"
- End slide

### Step 3: Build with mkslides
```bash
python -m mkslides build "output/{subfolder}/slides" -d "output/{subfolder}/site"
```

### Step 4: Verify output
- Check `site/index.html` exists
- Verify fragment usage: only on answer reveal slides, not on expository content
- Verify procedure text is in speaker notes (not on screen)
- Verify vocabulary words have phonemic script

## Fragment Policy

| Use fragments for | DO NOT use fragments for |
|---|---|
| Revealing answers (highlight-green) | Task instructions |
| Highlighting wrong answers (highlight-red) | Vocabulary lists |
| Key vocabulary emphasis (grow, single word) | Objectives/outcomes |
| | Discussion questions |
| | Lead-in images and prompts |
| | Material references |
| | Any expository content |

## Slide Types Generated

Based on `docs/slide-design-reference.md`:

| Slide | Generated when | Fragment use |
|---|---|---|
| Title | Always | None |
| Objective | Always | None |
| Vocabulary | Always (keyword extraction) | None |
| Lead-in image | Stage name contains "lead-in" | None |
| Pre-reading | Stage name contains "gist" | None |
| Task instruction | "detail"/"inference"/"exercise" stages | None |
| Answer explanation | Answer key present | YES — highlight-green per answer |
| Section transition | Between stages | None |
| Post-reading discussion | "post-reading"/"speaking"/"discussion" stages | None |
| Summary | Always | None |
| End | Always | None |

## Key Design Rules

1. **Procedure text in speaker notes** — never on visible slides
2. **Task instruction: 3 steps max, numbered** — full procedure in Notes
3. **Vocabulary: max 5 words per slide** — phonemic script + example sentence (NOT dictionary definition)
4. **Stage aims humanized** — "To activate interest in..." not "To lead-in to..."
5. **Answer slides: answer + why + source** (all 3 parts, fragment reveal)
6. **Backgrounds: gradient (title), warm (lead-in), red (transitions), dark (end)**

## Files

| File | Purpose |
|---|---|
| `docs/slide-design-reference.md` | Slide design rules (authoritative) |
| `scripts/json_to_markdown.py` | JSON → markdown converter |
| `mkslides.yml` | mkslides config (theme, transitions) |
| `templates/reveal-custom.html.jinja` | Custom template with ESL CSS |

## Dependencies
- Python 3.x + Jinja2
- mkslides v2.0.17 (`pip install mkslides`)
- Pixabay API key (for image slides — loaded by `pixabay-image-search` skill)