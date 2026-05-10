---
name: lesson-plan-to-reveal
description: Converts a lesson plan JSON file into a reveal.js presentation using direct inline markdown. Generates pedagogical ESL slides following the design rules in docs/slide-design-reference.md. Builds to static HTML via template injection.
---
# Skill: Lesson Plan to reveal.js Presentation

## Purpose
Convert a lesson plan JSON into a reveal.js slideshow for ESL classroom delivery. The teacher controls all slides — students never interact directly. **Slides support the teacher's narration, not replace it.** Student-facing content appears on screen; teacher procedure text goes in speaker notes only.

**Pipeline**: JSON → markdown + index.html (`json_to_markdown.py`) → open `slides/index.html` directly

**Slide design authority**: `docs/slide-design-reference.md` — this file defines all slide types, fragment policies, text limits, and vocabulary rules. The Python script reads this reference at generation time.

## When to Use This Skill

Use `lesson-plan-to-reveal` when converting a lesson plan JSON to slides. The skill:
1. Downloads a Pixabay title image and copies the institution logo into `output/{subfolder}/slides/assets/`
2. Runs `scripts/json_to_markdown.py` with `--title-image`, `--title-attribution`, and `--logo-image` — generates both `slides.md` and `index.html`
3. Reports the output path

## Workflow

### Step 1: Validate input
- Verify lesson plan JSON exists and parses
- Validate required fields: `teacher`, `duration`, `date`, `topic`, `materials`, `lesson_plan.stages`
- Read answer key from `answer_key` field (`.md` file or "none")

### Step 2: Download title image via Pixabay & copy logo into slides directory

Extract the subfolder and topic from the JSON path, then download 1 matching image
and copy the institution logo into `slides/assets/` so mkslides auto-copies them to the site:

```powershell
$jsonFile = "output/{subfolder}/{file}.json"
$jsonData = Get-Content $jsonFile | ConvertFrom-Json
$topic = $jsonData.topic

$subfolder = ($jsonFile -split '\\|/')[1]
$slidesDir = "output/$subfolder/slides"
$slidesAssetsDir = "$slidesDir/assets"
New-Item -ItemType Directory -Force -Path $slidesAssetsDir | Out-Null

$pixabayOutput = python scripts/pixabay_download.py --query "$topic" --type image --count 1 --output-dir "$slidesAssetsDir"
$pixabayResult = $pixabayOutput | ConvertFrom-Json

if ($pixabayResult.files.Count -gt 0) {
    $titleImage = $pixabayResult.files[0].path
    $titleAttribution = $pixabayResult.files[0].attribution
} else {
    Write-Warning "Pixabay search returned no results for '$topic' — falling back to gradient"
    $titleImage = ""
    $titleAttribution = ""
}

# Copy institution logo into slides/assets/
Copy-Item -Path "templates/Image_20260324_141022.png" -Destination "$slidesAssetsDir/logo.png" -Force
$logoImage = "$slidesAssetsDir/logo.png"
```

Output: `output/{subfolder}/slides/assets/pixabay_{id}_1.jpg` and `output/{subfolder}/slides/assets/logo.png`

### Step 3: Generate markdown and HTML

```bash
python scripts/json_to_markdown.py output/{subfolder}/{file}.json --title-image "$titleImage" --title-attribution "$titleAttribution" --logo-image "$logoImage"
```
Output: `output/{subfolder}/slides/{mmddyy}-{topic}-slides.md` and `output/{subfolder}/slides/index.html`

The script generates slides following `docs/slide-design-reference.md`:
- **Title** — topic + CEFR badge + strap subheader (derived from objective) + logo + Pixabay background at 80% opacity
- **Objective** — 3 simple outcomes in accessible language, tied to PET reading test
- **Vocabulary** — 3-5 words extracted from actual lesson text with phonemic script + clean definitions
- **Lead-in** — Pixabay background image + topic-specific open question
- **Pre-reading** — Pixabay background + 2 prediction prompts
- **Task slides** — brief student-facing task instructions (max 3 lines), full procedure in speaker notes
- **Answer slides** — properly parsed with ✓/✗ fragment reveals
- **Section transitions** — red backgrounds, natural language
- **Post-reading discussion** — all questions visible
- **Summary** — "What you can do now"
- **End slide**

### Step 4: Verify output
- Check `index.html` exists in the slides directory
- Verify title slide contains logo `<img>` tag with class `title-logo`
- Verify fragment usage: only on answer reveal slides, not on expository content
- Verify procedure text is in speaker notes (not on screen)
- Verify vocabulary words have phonemic script
- Verify title slide has strap subheader (not date/teacher/materials)

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

| Slide | Generated when | On-screen content | Speaker notes |
|---|---|---|---|
| Title + logo | Always | Topic, CEFR badge, strap subheader, logo | — |
| Objective | Always | 3 accessible outcomes tied to PET | — |
| Vocabulary | Always | 3-5 words from actual lesson text, one word per slide with Pixabay background | Drilling instructions |
| Lead-in image | "lead-in" stage | Topic-specific question | Photo display script, procedure |
| Pre-reading | "gist" stage (first) | 2 prediction prompts | Prediction activity script |
| Task instruction | "detail"/"inference"/"exercise" | Student-facing task steps (max 3) | Full procedure, timing, goal |
| Answer slides | Answer key present | Questions + fragment-reveal answers | — |
| Section transition | Between stages | Next stage name + warm-up question | Brief transition reminder |
| Post-reading discussion | "post-reading"/"speaking" | Discussion questions (all visible) | Timing, feedback notes |
| Wrap-up | "wrap-up"/"reflection" | Reflection questions | Error correction notes |
| Summary | Always | 3 "can do now" outcomes | Elicitation script |
| End | Always | "Thank you" + topic + CEFR | — |

## Key Design Rules

1. **Student-facing content on screen only** — task instructions, questions, vocabulary, answers. Teacher procedure text ("Students read...", "Pair check", "Feedback") goes in speaker notes. "Ss" is never used on screen.
2. **Objective slide uses accessible language** — avoid complex words like "identify", "distinguish", "inference". Use simple phrases like "Understand what the article is mainly about", "Find the most important facts and mistakes". Tie outcomes to PET reading test ("These are the same skills you need for the PET reading test!").
3. **Title slide: topic + CEFR badge + strap subheader** — NO date, teacher name, duration, or materials. Strap is derived from the lesson objective using natural teacher voice (e.g., "Reading for the main idea — bridging the generation gap"). Avoid stilted phrases like "An article about...".
4. **Task slides: brief student instructions** — extract task description from procedure, skip teacher-only instructions. Max 3 task lines on screen. Material references go in speaker notes, not on screen.
5. **Lead-in and pre-reading: Pixabay background images** — topic-relevant photos at 70% opacity. Fallback to gradient.
6. **Vocabulary slides: one word each, with Pixabay background** — "Important Words you need to know" title (NOT "Key Vocabulary"). Each slide: word + phonemic in IPA + bolded target word in context sentence that implies meaning (NOT dictionary definition). Max 5 words total. Pixabay background at 70% opacity that precisely conveys word meaning. All visible at once — NO fragments.
7. **Answer slides: properly parsed** — True/False with ✓/✗ fragments, letter answers, "Students' own answers" handled correctly. Article text sections are skipped.
8. **Transitions: natural language** — "Moving from X." not "Transition from X to Y."
9. **Stage aims humanized** — "To activate interest in..." not "To lead-in to..."
10. **Backgrounds**: Pixabay image at 80% opacity (title), 70% (lead-in/pre-reading/vocabulary), gradient fallback, red (transitions), dark (end)
11. **Logo: transparent RGBA PNG** — white backgrounds converted to transparency. Max height 100px, centered with 1em margin below.

## Files

| File | Purpose |
|---|---|
| `docs/slide-design-reference.md` | Slide design rules (authoritative) |
| `scripts/json_to_markdown.py` | JSON → markdown converter |
| `scripts/pixabay_download.py` | Pixabay image downloader |
| `templates/slides-template.html` | Static reveal.js HTML template (CDN, inline markdown) |
| `templates/Image_20260324_141022.png` | Institution logo (ACT) for title slide |

## Dependencies
- Python 3.x + Pillow, requests
- Pixabay API key (`PIXABAY_API_KEY` env var — loaded by `pixabay_download.py`)
- reveal.js 5.x via CDN (no npm needed)
