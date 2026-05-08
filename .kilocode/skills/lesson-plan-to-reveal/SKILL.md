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
1. Downloads a Pixabay title image to `output/{subfolder}/assets/` via `pixabay_download.py`
2. Copies the institution logo (`templates/Image_20260324_141022.png`) to `output/{subfolder}/assets/`
3. Runs `scripts/json_to_markdown.py` with `--title-image`, `--title-attribution`, and `--logo-image`
4. Runs `python -m mkslides build` to generate HTML
5. Reports the output path

## Workflow

### Step 1: Validate input
- Verify lesson plan JSON exists and parses
- Validate required fields: `teacher`, `duration`, `date`, `topic`, `materials`, `lesson_plan.stages`
- Read answer key from `answer_key` field (`.md` file or "none")

### Step 2: Download title image via Pixabay & copy logo

Extract the subfolder and topic from the JSON path, then download 1 matching image
and copy the institution logo into assets:

```powershell
$jsonFile = "output/{subfolder}/{file}.json"
$jsonData = Get-Content $jsonFile | ConvertFrom-Json
$topic = $jsonData.topic

$subfolder = ($jsonFile -split '\\|/')[1]
$assetsDir = "output/$subfolder/assets"
New-Item -ItemType Directory -Force -Path $assetsDir | Out-Null

$pixabayOutput = python scripts/pixabay_download.py --query "$topic" --type image --count 1 --output-dir "$assetsDir"
$pixabayResult = $pixabayOutput | ConvertFrom-Json

if ($pixabayResult.files.Count -gt 0) {
    $titleImage = $pixabayResult.files[0].path
    $titleAttribution = $pixabayResult.files[0].attribution
} else {
    Write-Warning "Pixabay search returned no results for '$topic' — falling back to gradient"
    $titleImage = ""
    $titleAttribution = ""
}

# Copy institution logo into assets
Copy-Item -Path "templates/Image_20260324_141022.png" -Destination "$assetsDir/logo.png" -Force
$logoImage = "$assetsDir/logo.png"
```

Output: `output/{subfolder}/assets/pixabay_{id}_1.jpg` and `output/{subfolder}/assets/logo.png`

### Step 3: Generate markdown

```bash
python scripts/json_to_markdown.py output/{subfolder}/{file}.json --title-image "$titleImage" --title-attribution "$titleAttribution" --logo-image "$logoImage"
```
Output: `output/{subfolder}/slides/{mmddyy}-{topic}-slides.md`

The script generates slides following `docs/slide-design-reference.md`:
- Title + institution logo + CEFR badge + **Pixabay background image at 80% opacity** + title text on solid maroon (`#800020`) background (CSS in `reveal-custom.html.jinja`)
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

### Step 4: Build with mkslides
```bash
python -m mkslides build "output/{subfolder}/slides" -d "output/{subfolder}/site"
```

### Step 5: Copy assets to site directory

```powershell
if ($titleImage) {
    Copy-Item -Path "output/$subfolder/assets" -Destination "output/$subfolder/site/" -Recurse -Force
}
```

This ensures the title slide image is served alongside the built HTML.

### Step 6: Verify output
- Check `site/index.html` exists
- Verify title slide contains logo `<img>` tag with class `title-logo`
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
| Title + logo | Always | None |
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
5.  **Answer slides: answer + why + source** (all 3 parts, fragment reveal)
6.  **Backgrounds: Pixabay image at 80% opacity (title) with solid maroon `#800020` text background, gradient (fallback), warm (lead-in), red (transitions), dark (end)**

## Files

| File | Purpose |
|---|---|---|
| `docs/slide-design-reference.md` | Slide design rules (authoritative) |
| `scripts/json_to_markdown.py` | JSON → markdown converter |
| `scripts/pixabay_download.py` | Pixabay image downloader |
| `mkslides.yml` | mkslides config (theme, transitions) |
| `templates/reveal-custom.html.jinja` | Custom template with ESL CSS |
| `templates/Image_20260324_141022.png` | Institution logo (ACT) for title slide |

## Dependencies
- Python 3.x + Jinja2
- mkslides v2.0.17 (`pip install mkslides`)
- Pixabay API key (`PIXABAY_API_KEY` env var — loaded by `pixabay_download.py`)
- Pillow, requests (Python packages)