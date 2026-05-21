---
name: lesson-plan-to-reveal
description: Converts a lesson plan JSON into a reveal.js presentation using raw HTML sections. All slides are hand-crafted <section> elements inside the base template. Markdown pipeline is permanently abandoned — auto-animate and pedagogical slides require native HTML.
---
# Skill: Lesson Plan to reveal.js Presentation

## Purpose
Convert a lesson plan JSON into a reveal.js slideshow for ESL classroom delivery. The teacher controls all slides — students never interact directly. **Slides support the teacher's narration, not replace it.** Student-facing content appears on screen; teacher procedure text goes in speaker notes only.

**Pipeline**: JSON → hand-built `index.html` with raw HTML `<section>` elements → open directly in browser (no server needed).

**Markdown is permanently abandoned** for slide generation. The reveal.js auto-animate feature requires sibling `<section data-auto-animate>` elements, which cannot be produced from a single `<section data-markdown>` container. All new presentations start from `templates/base-slides-template.html`.

**Slide design authority**: `docs/slide-design-reference.md` defines all slide types, fragment policies, text limits, vocabulary rules, and auto-animate patterns.

## When to Use This Skill

Use `lesson-plan-to-reveal` when converting a lesson plan JSON to slides. The skill:
1. **Parses the lesson plan JSON** — reads `lesson_plan.stages[]` to enumerate every stage and map each to slide types
2. **Reads source materials** — extracts exercise content from the source PDF and answer content from the answer key `.typ` file
3. Copies the institution logo into `output/{subfolder}/slides/assets/`
4. Copies `templates/base-slides-template.html` to `output/{subfolder}/slides/index.html`
5. Builds slides one by one as raw HTML `<section>` elements, inserting them between `<div class="slides">` and `</div>`
6. **Verifies every stage has at least one corresponding slide** — flags any stage that would be skipped
7. Reports the output path

## Workflow

### Step 0: Create the slides directory

```powershell
mkdir "output/{subfolder}/slides/assets"
```

### Step 1: Copy the base template

```powershell
cp "templates/base-slides-template.html" "output/{subfolder}/slides/index.html"
```

All slide `<section>` elements go between `<div class="slides">` and `</div>` in `index.html`. The `<head>`, `<style>`, `<body>`, `<script>` boilerplate is already complete — never edit it unless adding a new reveal.js plugin.

**Note:** The base template already includes the [audio-slideshow](https://github.com/rajgoel/reveal.js-plugins/tree/master/audio-slideshow) plugin (CDN-loaded) and the `TimerPlugin` in `Reveal.initialize()`. To add audio to a slide, use `data-audio-src="assets/file.mp3"` on the `<section>` element. Audio files go in `slides/assets/`. The plugin is configured with `advance: -1` (no auto-advance) — teacher controls playback via hover controls or `A` key. See the `audio:` config block in `Reveal.initialize()` for details.

**Known limitation — audio on multiple slides**: The audio-slideshow plugin does NOT reliably play the same audio file on more than one slide. If two or more slides need the same audio, copy the file to a distinct filename for each slide (e.g., `podcast_listen1.mp3` and `podcast_listen2.mp3`). Each `data-audio-src` value must be unique across the presentation.

### Step 2: Copy supporting files (timer plugin, logo)

```powershell
cp "templates/timer-plugin.js" "output/{subfolder}/slides/timer-plugin.js"
cp "templates/timer-plugin.css" "output/{subfolder}/slides/timer-plugin.css"
cp "templates/ACT.png" "output/{subfolder}/slides/assets/logo.png"
```

### Step 3: Backgrounds

**All background images must use `data-background-opacity="1.0"` (100% opacity). Never dim background images — the image should be fully vibrant.**

**Every element on a slide with a background image MUST use a text-shield class** (`text-shield` or `text-shield-light`) to ensure text remains legible against any image area. Text-shield classes add a semi-transparent background behind the text (see the Text Shield pattern section for details).

**Do NOT auto-download Pixabay or any other images.** If the teacher provides a background image URL or file path, you may use it. Never fetch images independently.

Default background color reference (solid colors — no shielding needed):
| Slide type | Default background |
|---|---|
| Title, lead-in, general content | `#1a1a2e` (dark navy/black) |
| Transition (forward to next stage) | `#c0392b` (red) |
| Pedagogical/strategy blocks, grammar rules | `#1a6b5a` (teal) |
| Answer tables | `#1e7e34` (green) |
| Summary | white (default) |
| End | `#2c3e50` (dark blue-gray) |

Background types available in reveal.js:
- **Solid color**: `data-background="#1a1a2e"` — default for most slides; no text-shield needed
- **Gradient**: `data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)"` — use for phase transitions or emphasis; no text-shield needed
- **Image**: `data-background-image="assets/filename.jpg" data-background-opacity="1.0"` — ONLY when teacher provides the file; ALL text on the slide MUST use `text-shield` or `text-shield-light`
- **Video**: `data-background-video="assets/clip.mp4" data-background-video-muted` — for lesson hooks, only with teacher-provided files; ALL text MUST use `text-shield`
- **Iframe**: `data-background-iframe="https://..." data-background-interactive` — for live web content as backdrop; text may need `text-shield` depending on the iframe content

**Rule summary:**
| Background type | `data-background-opacity` | Text-shield required? |
|---|---|---|
| Solid color | not applicable | No |
| Gradient | not applicable | No |
| **Image** | **`1.0`** | **Yes — ALL text on image slides must use `text-shield` or `text-shield-light`** |
| Video | `1.0` (implied) | Yes |
| Iframe | not applicable | Case-by-case |

See the [Reveal.js Backgrounds documentation](https://revealjs.com/backgrounds/) for full details on all available options and attributes.

### Step 4A: Parse the lesson plan — enumerate stages and map to slides

**CRITICAL: The lesson plan JSON is the primary authority for slide content.** Read `lesson_plan.stages[]` from the JSON. Every stage MUST produce at least one slide. Do NOT use the generic "Slide ordering convention" below — that was an old artifact and caused missing stages. Derive slide order from stage order.

For each stage in `lesson_plan.stages[]`:
1. Read the stage name, aim, procedure, time, and interaction from the JSON.
2. Determine which slide type(s) this stage maps to, using the Stage-to-Slide Mapping table below.
3. For any exercise referenced in the procedure (e.g., "Practice 2B"), **read the source PDF** to get the actual exercise content that students will see on screen.
4. For any answer key referenced in the JSON, **read the answer key file** (.typ) manually and re-express its content as HTML table rows. Do NOT attempt to parse Typst markup programmatically — `#table(...)` calls and `*bold*` syntax are not reliably machine-readable. Read the file, understand the answers, then hand-build the HTML.
5. For any bespoke (teacher-written) exercise that has no PDF source, **source content from the lesson plan JSON's procedure text** or from the user's specified item list. Do NOT assume all exercise content lives in a PDF.
6. Create the appropriate `<section>` elements.

**Stage-to-Slide Mapping** (use this to determine how many slides each stage needs):

| Stage type (from name/purpose) | Slide(s) to create | Content source |
|---|---|---|
| Lead-in — discussion / prediction | 1 slide with open question, dark `#1a1a2e` background | Stage procedure + user's context |
| Lead-in — error analysis with auto-animate | 2-3 auto-animate slides: error sentences (transparent borders) → corrected sentences (visible borders) | Bespoke error sentences from lesson plan |
| Diagnostic test (Test 1 in TTT) | 1 slide with all test items on screen, dark `#1a1a2e` background | Lesson plan JSON procedure text (bespoke items) |
| Teach / Clarifying | 1-2 slides per concept taught (not per sub-rule); group related rules together | Source PDF definitions + examples + rule statements |
| Controlled Practice / Practice X | 1 task slide (student-facing instructions + timer) + 1+ answer slides (see answer table sizing rules below) | Source PDF exercise content + answer key file |
| Freer Practice / Practice X | 1 task slide + 1+ answer slides (see answer table sizing rules below) | Source PDF exercise content + answer key file |
| Wrap-up | 1 summary slide | Stage procedure + learning objectives from JSON |
| Vocabulary (if pre-teach stage exists) | 1 slide per word (max 5) | Stage 11 pre-teach vocabulary selection |

**Slide order**: Follow stage_number order from the JSON. Insert Title (slide 0) and Objective (slide 1) BEFORE stage 1. Insert End slide AFTER the last stage.

**Speaker notes**: All slides EXCEPT transition slides and end slides must include `<aside class="notes">` containing:
- Stage aim from the JSON (`stage_aim`)
- Timing (`time` field in minutes)
- Interaction pattern (`interaction` field)
- The full procedure text from the JSON
- Do NOT put procedure text on screen — only student-facing task instructions

| Slide type | Notes required? | Content |
|---|---|---|
| Title | Yes | Lesson overview, teacher cues |
| Objective | Yes | Elicitation script, connection to prior learning |
| Lead-in | Yes | Activation script, timing, expected responses |
| Diagnostic test | Yes | Stage aim, timing, monitoring instructions |
| Teach / Clarifying | Yes | Key points to elicit, board plan cues |
| Task instruction | Yes | Full procedure, timing, interaction pattern |
| Answer table | Yes | Discussion prompts, expected student reactions |
| Transition | No | (Teacher's spoken introduction bridges the gap) |
| Summary | Yes | Elicitation script, connection to objective |
| End | No | — |

**Materials**: For any exercise referenced in the procedure by name (e.g., "Practice 2B", "Practice 7"), read the source PDF file from the `inputs/` folder to get the exercise text. Build screen content from the PDF, not from your own paraphrasing. The exercise must look exactly as it does in the textbook (same items, same numbering).

**Answers**: For any exercise that has an answer in the answer key, read the answer key `.typ` file and build answer table slides. Use `class="fragment answer-correct"` for correct answers, `class="fragment answer-incorrect"` for incorrect answers.

### Step 4B: Build slides (new build)

Write slide sections to a temp file, then splice them into the template. **Do NOT attempt to write the entire `index.html` in a single Write tool call** — at 600+ lines with Unicode content, the Write tool may reject or mangle the file. Do NOT copy the template and then incrementally replace sections with Edit tool calls — this is slow, fragile, and causes timeouts.

Instead, use the **splice approach**:

1. **Compose all `<section>` elements** in a temp file at `C:\Users\elwru\AppData\Local\Temp\kilo\slides_sections.html` using the Write tool.
2. **Copy the template** to the output directory via PowerShell:
   ```powershell
   cp "templates/base-slides-template.html" "output/{subfolder}/slides/index.html"
   ```
3. **Run a Python splice script** that finds the `<div class="slides">` boundary in the template and inserts the sections, then updates the `<title>`:
   ```python
   import re
   template_path = r"output/{subfolder}/slides/index.html"
   sections_path = r"C:\Users\elwru\AppData\Local\Temp\kilo\slides_sections.html"
   
   with open(template_path, "r", encoding="utf-8") as f:
       template = f.read()
   with open(sections_path, "r", encoding="utf-8") as f:
       sections = f.read()
   
   # Find the slides div boundary
   start_marker = '<div class="slides">'
   start_idx = template.find(start_marker)
   
   # Find the closing </div> that ends the slides div
   # Template structure: <div class="slides"> ... (comments/patterns) ... </div> (closes slides) </div> (closes reveal) <script> tags
   # Search after the last HTML comment end
   search_from = start_idx + len(start_marker)
   last_comment = template.rfind("-->", search_from, start_idx + 2000)
   end_idx = template.find("</div>", max(search_from, last_comment + 3))
   
   result = template[:start_idx + len(start_marker)] + "\n\n" + sections + "\n" + template[end_idx:]
   result = result.replace("<!-- TOPIC -->", lesson_title)
   
   with open(template_path, "w", encoding="utf-8") as f:
       f.write(result)
   ```
4. **Update the `<title>`** by replacing `<!-- TOPIC -->` with the lesson topic.
5. Then verify the output (Step 5).

**Why this works:**
- The Write tool call writes to the allowed `C:\Users\elwru\AppData\Local\Temp\kilo\` directory (no permission issues)
- Python handles UTF-8 cleanly (no BOM, no PowerShell encoding corruption)
- The splice is deterministic — finds `<div class="slides">` and the first `</div>` after the last HTML comment
- No size limit concerns — sections and template are written separately

The boilerplate (everything before `<div class="slides">` and everything after the closing `</div>` of the slides div) is always the same. Only the `<section>` elements inside `<!-- SLIDE N -->` comments change per lesson.

#### C. Editing an existing slideshow

When the user asks to modify an already-built slideshow (e.g., "change slide 7" or "add a new slide after the vocabulary"):
1. Read the current `index.html`.
2. Use the `Edit` tool for targeted incremental changes.
3. Use `scripts/locate_slide.py` to find the exact line numbers.

**Rule**: Every slide is a raw `<section>` element inside `<div class="slides">`.

### Step 5: Verify output

**Prefer revealjs-validator over bespoke scripts.** The project includes `revealjs-validator` (npm dev dependency) which checks 66 rules derived from the official Reveal.js docs. Run it in project mode for cross-file validation:

```bash
npx revealjs-validator --project "output/{subfolder}/slides/"
```

This catches broken auto-animate pairs, invalid fragment classes, missing assets, CSS misuse, and more. **However, the validator only checks static HTML structure — it CANNOT detect runtime errors that cause a blank page.** A presentation can pass all 66 rules and still show a blank screen due to a JavaScript error during `Reveal.initialize()`.

**CRITICAL — Browser test every build:** After the validator passes, open the slides in a browser and check the JavaScript console (`F12` → Console tab):
- Verify the page shows content (not blank/white)
- Verify NO red errors appear in the console
- Common runtime errors: undefined plugin references, CDN failures, plugin `init()` crashes
- If the page is blank, remove recently added plugins from the `plugins` array first, then debug

For the specific checks the validator doesn't cover (e.g., lesson plan stage coverage, answer table sizing, speaking notes on every slide), write a focused Python verification script to `C:\Users\elwru\AppData\Local\Temp\kilo\` that uses `in` operator checks.

If a check fails, do NOT trust what the terminal displays (Unicode renders inconsistently). Instead:
```python
idx = content.find(check_words[0])  # search for first word
if idx >= 0:
    print(repr(content[idx:idx+80]))  # show exact bytes
    print(content[idx:idx+80].encode("utf-8").hex())  # show hex
```

**Checklist:**
- **CRITICAL — Stage coverage check**: Count the number of `<section>` slides created (excluding Title + End). Verify this matches the number of `lesson_plan.stages[]` items. Each stage must have ≥ 1 corresponding `<section>` slide. If a stage has no slides, flag it immediately.
- Check `index.html` exists in the slides directory
- Check `timer-plugin.js` and `timer-plugin.css` exist in the slides directory
- Verify title slide contains `<img src="assets/logo.png" class="title-logo" />`
- Verify `TimerPlugin` is in the `plugins` array of `Reveal.initialize()`
- Verify `answer-correct` / `answer-incorrect` are used for answer fragments (NOT `highlight-green`/`highlight-red`)
- **Answer table sizing**: For every `<table class="answer-table">`, count the `<tr>` elements in `<tbody>`. Max 3 items per slide when a Why column is present (4-column tables). Max 5 for simple 3-column tables. Flag any table that exceeds the appropriate limit.
- Verify no instructional text like "Click to reveal" appears on slides — answer reveal behavior is self-evident.
- Verify fragment usage: only on answer reveal slides and strategy demonstrations, not on expository content
- Verify procedure text is in `<aside class="notes">`, not on screen
- Verify vocabulary words use `<span class="vocab-word">word</span>`
- Verify title slide has strap subheader (not date/teacher/materials)
- Verify `autoAnimateUnmatched: true` is in `Reveal.initialize()`
- Verify every slide with `data-auto-animate` also has `data-auto-animate-id` — without it, `null === null` causes all auto-animate slides to animate into each other.
- Verify transition slides use `data-background="#c0392b"`
- Verify pedagogical strategy slides use `data-background="#1a6b5a"` and `class="pedagogical"`
- Verify listening task slides that need audio have `data-audio-src="assets/filename.mp3"`
- **Verify no `<section>` has both `data-timer` AND `data-audio-src`** — never place a timer pill on a slide that plays audio or video

### Step 6: Publish and write URL to lesson plan JSON

After slides are verified, publish to GitHub Pages and write the deployment URL into the lesson plan JSON as `slideshow_url`. This feeds into the PDF template's gray-shaded Slideshow URL cell.

**Prerequisites:** `gh` CLI installed and authenticated. See `publish-to-github-pages` skill for details.

```powershell
# Extract owner and repo from git remote
$remoteUrl = git remote get-url origin
$owner, $repo = if ($remoteUrl -match 'github\.com[:\/](.+?)\/(.+?)\.git') { $matches[1], $matches[2] }
$url = "https://${owner}.github.io/${repo}/"

# Write URL to the lesson plan JSON
$jsonPath = "output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json"
$json = Get-Content $jsonPath -Raw | ConvertFrom-Json
$json | Add-Member -MemberType NoteProperty -Name "slideshow_url" -Value $url -Force
$json | ConvertTo-Json -Depth 10 | Set-Content $jsonPath

Write-Host "Slideshow URL written to $jsonPath : $url"
```

## Fragment Policy

| Use fragments for | DO NOT use fragments for |
|---|---|
| Revealing answers (`answer-correct`) | Task instructions |
| Highlighting wrong answers (`answer-incorrect`) | Vocabulary lists |
| Strategy step reveals (on pedagogical slides) | Objectives/outcomes |
| Eliminating wrong MC options (`strike`) | Discussion questions |
| Key vocabulary emphasis (`grow`, single word) | Lead-in images and prompts |
| | Material references |
| | Any expository content |

Fragment classes:
- `fragment answer-correct` — correct answer revealed (hidden until click, green background on reveal)
- `fragment answer-incorrect` — incorrect answer revealed (hidden until click, red background on reveal)
- `fragment highlight-green` — **DO NOT USE** (reveal.js built-in forces `opacity: 1`, prevents hiding)
- `fragment highlight-red` — **DO NOT USE** (same reason as above)
- `fragment strike` — eliminated wrong answer (always visible, strikethrough on click)
- `fragment grow` — emphasize single vocabulary word
- `fragment` (bare) — generic reveal


## Slide Type Templates (Raw HTML)

All patterns live in `templates/base-slides-template.html` as HTML comments. **Copy the pattern, paste it into `<div class="slides">`, and adapt the content.** Do not invent new patterns — only use variants of the ones documented here.

### 1. Title Slide
```html
<section data-background="#1a1a2e">
    <img src="assets/logo.png" class="title-logo" alt="Logo" />
    <h1>Topic Title <span class="cefr-badge B1">B1</span></h1>
    <p><em>Strap subheader — derived from lesson objective</em></p>
</section>
```
- CEFR badge colors: A1=green, A2=light green, B1=blue, B2=dark blue, C1=purple, C2=red
- Strap is derived from the lesson objective using natural teacher voice
- NO date, teacher name, duration, or materials on title slide
- Logo: `assets/logo.png`, max-height 100px (set in CSS)

### 2. Objective Slide
```html
<section>
    <h2>Here's what you'll be able to do</h2>
    <ul>
        <li>Understand what the article is mainly about</li>
        <li>Find the most important facts and mistakes</li>
        <li>Share your ideas with a partner</li>
    </ul>
    <p><em>These are the same skills you need for the PET reading test!</em></p>
</section>
```
- 3 outcomes max, each ≤10 words
- NO fragments — students see this as orientation
- Tie to PET reading test where applicable

### 3. Vocabulary Slides (one word per slide)
```html
<!-- First word (with header) -->
<section class="vocab-slide" data-background="#1a1a2e">
    <h2>Important Words</h2>
    <p><span class="vocab-word">generation gap</span></p>
    <p><em>/ˌdʒenəˈreɪʃn ɡæp/</em></p>
    <p><em>There is a big <span class="vocab-word">generation gap</span> between old people and young people.</em></p>
</section>

<!-- Subsequent words (no header) -->
<section class="vocab-slide" data-background="#1a1a2e">
    <p><span class="vocab-word">frustration</span></p>
    <p><em>/frʌˈstreɪʃn/</em></p>
    <p><em>I felt <span class="vocab-word">frustration</span> when my phone died.</em></p>
</section>
```
- **One word per slide** — max 5 words total
- `<span class="vocab-word">` renders yellow (#ffdd00) bold
- Word + phonemic script (IPA) + context sentence with word highlighted
- **Sentence must imply meaning, NOT define** — e.g., "There's such a **generation gap** between them" (GOOD) vs "generation gap — the difference between groups" (BAD)
- Background: `#1a1a2e`
- Class: `vocab-slide`

### 4. Lead-in Slide
```html
<section data-background="#1a1a2e">
    <h2>Let's get Started</h2>
    <h3>What do these two people have in common?</h3>
    <aside class="notes">
        Display the photo. Give students 20 seconds to look silently.
        Then ask the question. Elicit 3-4 responses.
        Connect responses to today's topic.
    </aside>
</section>
```
- One open question only
- Speaker notes in `<aside class="notes">`

### 5. Transition Slide (red background)
```html
<section data-background="#c0392b">
    <h2>Finding details</h2>
</section>
```
- Red background `#c0392b`
- **Heading only** — no subheader text or descriptive paragraphs. The teacher's spoken introduction bridges the gap. All `<p>` elements removed.

### 6. Auto-Animate Strategy Block
```html
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
    <h2>True/False Strategy</h2>
    <p><strong>Step 1:</strong> Read the statement carefully</p>
    <p><em>Statement text goes here.</em></p>
</section>
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
    <h2>True/False Strategy</h2>
    <p><strong>Step 1:</strong> Read the statement carefully</p>
    <p><em>Statement text goes here.</em></p>
    <p><strong>Step 2:</strong> Find the keywords</p>
    <p>"keyword1" · "keyword2" · "keyword3"</p>
</section>
<!-- ... up to 5 slides, each adding one more step ... -->
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
    <h2>True/False Strategy</h2>
    <!-- ... all previous steps ... -->
    <p class="fragment highlight-green">TRUE — Explanation of why it's true.</p>
</section>
```
**Critical rules for auto-animate:**
- All sections in one auto-animate block MUST be **consecutive siblings** in `<div class="slides">` — no other sections between them
- `data-auto-animate-id` MUST match across all sections in the block (e.g., `"tf-strategy"`)
- Each section builds on the previous one by adding new elements
- Use `data-auto-animate` (not `data-auto-animate-unmatched`) — `autoAnimateUnmatched: true` in Reveal.initialize handles unmatched elements
- All sections in the block share `class="pedagogical"` and `data-background="#1a6b5a"`
- The final section may include a `fragment highlight-green` for the answer reveal
- Auto-animate sections CANNOT be placed inside `<section data-markdown>` — this is the core reason markdown was abandoned

### 7. Task Instruction Slide
```html
<section data-timer="960">
    <h2>Finding details</h2>
    <ul>
        <li>Read the article again and complete the true/false task.</li>
        <li>Complete the paragraph matching task.</li>
    </ul>
    <aside class="notes">
        Stage 3 · 16 min · Ss-Ss
        Goal: To identify key facts and supporting details
        Materials: Student Book, pp 5-6
    </aside>
</section>
```
- `data-timer="seconds"` — time in seconds (minutes × 60)
- Brief student-facing instructions (max 3 bullet points)
- Full procedure, timing, and materials in `<aside class="notes">`
- **Listening task slides** that play an audio track should also add `data-audio-src="assets/filename.mp3"` on the `<section>` element
- **Never combine `data-timer` and `data-audio-src` on the same `<section>`** — timer pills conflict with audio playback. Use one or the other, not both.

### YouTube / Iframe Embedding

YouTube requires a valid `HTTP Referer` header for embedded players. Without it, YouTube returns Error 153. Use `referrerpolicy="strict-origin-when-cross-origin"` on the iframe to ensure the browser sends the referrer.

```html
<section data-background="#1a1a2e">
    <h2>Video Title</h2>
    <iframe
        width="760" height="430"
        src="https://www.youtube.com/embed/VIDEO_ID"
        frameborder="0"
        allowfullscreen
        referrerpolicy="strict-origin-when-cross-origin"
        style="border: none; display: block; margin: 0 auto;">
    </iframe>
    <p><em>Discussion prompt below the video.</em></p>
</section>
```

**Rules:**
- Use `src` directly (not `data-src`) — the iframe loads immediately. Reveal.js will auto-detect the YouTube URL and manage pause-on-navigate-away via postMessage.
- `referrerpolicy="strict-origin-when-cross-origin"` — REQUIRED. Without this, YouTube blocks the embed when the page is served from `file://` or any context without a default referrer.
- Also add `<meta name="referrer" content="strict-origin-when-cross-origin" />` inside `<head>` as a page-wide fallback for any other embedded resources that need a referrer.
- `allowfullscreen` enables the YouTube fullscreen button.
- Do NOT add `data-timer` to a slide that has a YouTube iframe.
- Background: `#1a1a2e` (dark navy).

### Diagnostic Talk Structure Slide

For teaching students how to structure a short talk (thesis → reasons → example):

```html
<section class="pedagogical structure-talk" data-background="#1a6b5a" data-background-transition="none">
    <h2>Structure Your Talk</h2>
    <p class="structure-step"><u><strong>Thesis:</strong> Say your main idea</u></p>
    <p class="structure-step"><u><strong>Reasons:</strong> Give 1-2 reasons</u></p>
    <p class="structure-step"><u><strong>Example:</strong> Share an example you know</u></p>
    <p class="transition-words">First... &nbsp; Also... &nbsp; For example...</p>
</section>
```

- Teal background `#1a6b5a`, `class="pedagogical structure-talk"`
- Three underlined steps teaching basic argument structure
- Yellow transition word box at bottom: First / Also / For example

### 8. Pedagogical Strategy Slide (non-auto-animate)
```html
<section class="pedagogical" data-background="#1a6b5a">
    <h2>Multiple Choice Strategy</h2>
    <p><strong>Step 1: Read all options first</strong> <span class="fragment"> — look at all three choices</span></p>
    <ul class="fragment">
        <li>a) Option A text</li>
        <li>b) Option B text</li>
        <li>c) Option C text</li>
    </ul>
    <p class="fragment"><strong>Step 2: Eliminate wrong answers</strong></p>
    <p class="fragment strike">a) Reason. <strong>Eliminate.</strong></p>
    <p class="fragment strike">b) Reason. <strong>Eliminate.</strong></p>
    <p class="fragment"><strong>Step 3: Confirm the answer</strong></p>
    <p class="fragment answer-correct">c) Explanation. ✓ <strong>c is correct!</strong></p>
</section>
```
- Teal background `#1a6b5a` via `data-background`
- `class="pedagogical"` for white text styling
- Fragments used for step-by-step reveal of strategy

### 9. Answer Slide (True/False)

Use the same `answer-table` pattern with green background and fragment reveals:

```html
<section data-background="#1e7e34">
    <h2>Exercise N — Answers</h2>
    <p class="aim-label">True/False</p>
    <table class="answer-table">
        <thead><tr><th>Statement</th><th>Answer</th></tr></thead>
        <tbody>
            <tr><td>Statement text here.</td><td class="fragment answer-correct">✓ <strong>True</strong></td></tr>
            <tr><td>Another statement.</td><td class="fragment answer-incorrect">✗ <strong>False</strong></td></tr>
            <tr><td>Corrected statement.</td><td class="fragment answer-correct">✓ <em>Explanation</em></td></tr>
        </tbody>
    </table>
</section>
```
- **Statements visible at slide entry** — teacher and students see all questions immediately
- **Answer column uses `class="fragment answer-correct"` or `class="fragment answer-incorrect"`** — revealed one row at a time
- `answer-correct` = green background on reveal, `answer-incorrect` = red background on reveal
- **Do NOT use `highlight-green`/`highlight-red`** — reveal.js built-in classes force `opacity: 1`, preventing fragment hiding
- **CRITICAL — Color contrast on green slides**: On `#1e7e34` answer slides, **only two colors are allowed** for text: **white `#fff`** or **yellow `#ffdd00`**. Any other color — blue (`#4fc3f7`), gray (`#999`, `#ccc`, `#888`), light gray, silver, muted tones — is **FORBIDDEN**. They are invisible against the green background at projection distance. If you see any text on a green answer slide that is not white or yellow, it is a bug that must be fixed. Use `<span style="color: #fff;">` explicitly for any element whose color is not obvious from context.
- **Answer table sizing**: Max **3 items per slide** when a Why column is present (4-column tables: # / Sentence / Answer / Why?). For simple 3-column tables without Why column, up to 5 items per slide. Examples: 11 grammar items → 4 slides of 3+3+3+2; 6 errors → 2 slides of 3+3.
  - Do NOT include instructional text like "Click to reveal" — the reveal behavior is self-evident.
  - Use `data-fragment-index` matching on Answer and Why cells for per-row reveal (both columns reveal on the same click).
  - Table font: `0.875em` for 4-column tables, with Why column at `0.9em`.

### 10. Answer Slide (Multiple Choice / Matching)

```html
<section data-background="#1e7e34">
    <h2>Exercise N — Answers</h2>
    <p class="aim-label">Multiple Choice</p>
    <table class="answer-table">
        <thead><tr><th>Question</th><th>Answer</th><th>Why?</th></tr></thead>
        <tbody>
            <tr><td>Question text</td><td class="fragment answer-correct">✓ <strong>c) Option C</strong></td><td class="fragment">citation from text</td></tr>
        </tbody>
    </table>
</section>
```
- **Questions/options visible at slide entry** — students see all choices
- **Answer and Why columns are fragments** — revealed one row at a time via clickthrough
- **Answers must be yellow, not white**: Answers should be highly contrastive to questions. Use class `answer-yellow` (yellow `#ffdd00`) on answer reveal text (e.g., `class="fragment answer-yellow"`). Questions/options stay white; revealed answers turn yellow to visually separate them.

### 11. Summary Slide
```html
<section>
    <h2>What you can do now</h2>
    <ul>
        <li>✓ I can find the main idea</li>
        <li>✓ I can find important facts</li>
        <li>✓ I can share my ideas</li>
    </ul>
    <aside class="notes">
        Elicit from students: What did you learn today?
        Connect back to their predictions from the beginning.
        Praise effort, mention one thing to improve.
    </aside>
</section>
```
- 3 "I can..." outcomes with checkmarks
- Speaker notes: elicitation script

### 12. End Slide
```html
<section data-background="#2c3e50">
    <h2>Thank you</h2>
    <p><em>Topic Name</em> | B2</p>
</section>
```
- Dark background `#2c3e50`

## Slide Indexing System

When the user provides a reveal.js URL like `file:///.../index.html#/N`, use `scripts/locate_slide.py` to map the slide index to its HTML section.

```bash
python scripts/locate_slide.py "file:///path/to/index.html#/7"
python scripts/locate_slide.py 7 --slides-dir path/to/slides/
```

The script reads `index.html` directly (not a markdown file). The slide index equals the 0-based position of the `<section>` element within `<div class="slides">`.

Mapping:
- URL `index.html#/` or `index.html#/0` → first `<section>` (title)
- URL `index.html#/1` → second `<section>` (objective)
- URL `index.html#/7` → eighth `<section>`
- And so on...

### Slide Editing Workflow (HTML)

When asked to edit a slide at a reveal.js URL:

1. **Run `scripts/locate_slide.py`** to determine the section index and line numbers:
   ```bash
   python scripts/locate_slide.py "file:///path/to/index.html#/7"
   ```
2. The script outputs JSON with slide index, heading text, and line numbers
3. **Edit `index.html` directly** using the line numbers from the output — no intermediate markdown file
4. **No regeneration needed** — the HTML is already complete. Just reload the browser.
5. **When adding a new slide**, insert a new `<section>` element at the correct position in `<div class="slides">`.

**Stable slide IDs (preferred):** Every `<section>` should have a stable `id` attribute to prevent index confusion when slides are added or removed:
```html
<section id="slide-lead-in" data-background="#1a1a2e">
```
To locate a slide by its stable ID:
```bash
python scripts/locate_slide.py --id slide-objective --html path/to/slides/index.html
```
Use kebab-case names matching the slide function (e.g., `slide-title`, `slide-objective`, `slide-lead-in`, `slide-test1-1-3`, `slide-p7-corrected-1-3`, `slide-summary`).

## Key Design Rules

1. **Student-facing content on screen only** — task instructions, questions, vocabulary, answers. Teacher procedure text goes in `<aside class="notes">`. "Ss" is never used on screen.
2. **Objective slide uses accessible language** — avoid complex words like "identify", "distinguish", "inference". Use simple phrases. Tie outcomes to PET reading test.
3. **Title slide: topic + CEFR badge + strap subheader** — NO date, teacher name, duration, or materials.
4. **Task slides: brief student instructions** — extract task description from procedure, skip teacher-only instructions. Max 3 task lines on screen.
5. **Stage names: student-friendly language** — "Lead-in" → "Let's get Started", "Reading for gist" → "What's the main idea?", "Reading for detail" → "Finding details", "Reading for inference" → "Making conclusions", "Post-reading" → "Let's Discuss", "Wrap-up" → "Let's Review"
6. **Vocabulary slides** — generated AFTER lead-in stage. One word per slide with dark navy background. "Important Words" title on first slide only. Yellow bold (#ffdd00) via `<span class="vocab-word">`.
7. **Answer slides** — use `<table class="answer-table">` with green background `#1e7e34`. Statements visible on entry; answers use `class="fragment answer-correct"` or `class="fragment answer-incorrect"` for clickthrough reveal. **Do NOT use `highlight-green`/`highlight-red`** (reveal.js keeps them at `opacity: 1`; they never hide). **CRITICAL — Green slide text: only white `#fff` or yellow `#ffdd00` allowed.** Gray, blue, or any muted color is invisible at projection distance. Never use any other color on `#1e7e34` slides.
8. **Transition slides: heading only (no subheader text).** The red background + icon + heading is sufficient — the teacher's spoken introduction bridges the gap. Remove all `<p>` elements from transition slides.
9. **Backgrounds**: dark navy `#1a1a2e` (title, lead-in, vocabulary), red `#c0392b` (transitions), teal `#1a6b5a` (pedagogical/strategy), green `#1e7e34` (answer tables), dark `#2c3e50` (end)
10. **Logo**: `assets/logo.png`, transparent RGBA PNG, max-height 100px, centered
11. **Text highlighting**: white text, dark text-shadow, pedagogical sections use white-on-teal
12. **Vocabulary words**: yellow boldface (`#ffdd00`) via `<span class="vocab-word">` — in both the word heading AND context sentence
13. **Timer pill vs audio**: Never add `data-timer` to a slide that also has `data-audio-src`. Slides with audio playback should not have a timer pill — the two controls conflict visually and functionally.
14. **Proper HTML lists for letters/numbers**: Never use manual lettering or numbering in `<p>` tags (e.g., `<p><strong>A</strong> Option text</p>`). Use semantically correct HTML lists instead: `<ol type="A">` for lettered options, `<ol>` for numbered items, `<ul>` for bullet points. Each item gets its own `<li>` element. This ensures proper alignment and accessibility.
## Authorial Voice & Audience

This skill generates slides for **Thai secondary students (CEFR A2–B2)**. The default voice targets **B1** (Mathayom 2-3). All student-facing text on screen MUST follow these rules, with level-appropriate relaxations noted.

### Baseline (Applies to all CEFR levels)

#### 1. Person Rule
All on-screen student-facing text MUST use **direct "you" imperatives**, never third person:

| Wrong | Correct |
|-------|---------|
| "Students read the article again..." | "Read the article again." |
| "They must correct the false statements." | "Correct the false statements." |
| "Ss complete the task individually." | "Complete the task on your own." |

**`<aside class="notes">` remains unrestricted** — teacher procedure can use full professional vocabulary.

#### 2. Person Rule
- Collective framing: "We can see...", "Our class can think about..."
- Positive, concrete questions — avoid abstract philosophical prompts
- Group participation questions, not individual introspection

#### 3. No Automatic Image Downloads
When regenerating slides, **do not auto-download images**. Start with solid theme colors. Use gradients, images, or videos only when the teacher provides assets or when they serve a clear pedagogical purpose. Never fetch images independently.

### B1 Default (Mathayom 2-3)

#### Vocabulary Ceiling
No words above CEFR B1 on screen without inline definition:
- "identify" → use "find"
- "predict" → use "guess"
- "convincing" → use "makes sense"
- "distinguish" → use "tell the difference"
- "evaluate" → use "decide"
- "analyze" → use "look at carefully"
- "infer" → use "understand what the writer means"

#### Sentence Complexity
- Max 15 words per sentence on screen
- No semicolons — break into two sentences
- One clause preferred, two max
- No passive voice on screen

#### Summary: "I Can" Statements
| Wrong | Correct |
|-------|---------|
| "Identify the main purpose" | "I can find the main idea" |
| "Find key facts" | "I can find important facts" |
| "Express opinions" | "I can share my ideas" |

### B2 Adaptation (for higher-level classes)

When the lesson targets B2 learners, relax the B1 rules as follows:

- **Vocabulary ceiling**: academic words (identify, evaluate, analyze) may appear but must be defined or exemplified on screen
- **Sentence complexity**: max 20 words per sentence; semicolons OK for contrast
- **Summary**: may use slightly more specific outcomes (e.g., "I can use correct subject-verb agreement when a prepositional phrase separates subject and verb")
- **All other rules remain** (person rule, no auto-download, collective framing)

## reveal.js Animation & Interactive Features

This section maps reveal.js features to pedagogical contexts. Use it as a lookup table when designing slides — choose the right tool for the job.

### Auto-Animate vs. Fragments vs. Sibling Slides

**When to use each approach:**

| Use auto-animate for | Use simple sibling slides for | Use fragments (single slide) for |
|---|---|---|
| Error-correction reveals (transparent → visible borders) | Step-by-step strategy demonstrations (1 slide per step) | Answer reveals (T/F, MC, grammar) |
| Quick grammar transformations (word-by-word) | Explicit SBI instruction where teacher pauses at each step | Eliminating wrong MC options (`strike`) |
| Keyword underline reveals (border color change) | Grammar rule explanations (1-2 slides for all rules) | Multi-step strategy on a single slide |
| Any animation effect that requires matching `data-id` elements between slides | | |

**Decision framework:**
1. **Will each step of your content be a discrete teaching moment?** (Teacher will pause, ask questions, check understanding at each step) → Use **simple sibling slides** (one slide per step, `data-background-transition="none"`). Each step is a separate `<section>` without `data-auto-animate`.
2. **Is the effect purely visual (borders appearing, colors changing, words replacing)?** (The content doesn't change, only its visual treatment) → Use **auto-animate** across 2 consecutive `<section>` elements with matching `data-id` attributes.
3. **Does the teacher just need to click through existing content?** (Revealing answers, eliminating options, showing steps already on screen) → Use **fragments** on a single `<section>`.

**Rules for simple sibling slides (non-auto-animate, pedagogical):**
- Each step = one `<section>` with `class="pedagogical"` and `data-background="#1a6b5a"`
- All sections: `data-background-transition="none"` (prevents flash of color on entry)
- CSS handles top alignment via `.reveal .slides > section.pedagogical` — no inline style needed (reveal.js strips inline `top` during layout)
- Step label underlined: `<u><strong>Step N:</strong> ...</u>`
- Rule (if applicable) embedded in Step 2, not a separate slide

**Rules for auto-animate blocks:**
1. All sections in one block must be **consecutive siblings** — no other sections between them
2. **CRITICAL — `data-auto-animate-id` is REQUIRED** on every slide with `data-auto-animate`. The reveal.js `shouldAutoAnimateBetween()` function compares `data-auto-animate-id` between slides. **Without it, `null === null` evaluates to `true`, causing ALL slides with `data-auto-animate` to animate into each other — even unrelated slides from different rule blocks.** Use a unique id per block (e.g., `"rule-1"`, `"rule-2"`, `"tf-strategy"`).
3. Each section adds content to what was shown in the previous section, OR changes styling of existing elements (border color, font-weight)
4. `autoAnimateUnmatched: true` in `Reveal.initialize()` handles elements that appear/disappear between slides
5. All sections share `class="pedagogical"` and `data-background="#1a6b5a"` for visual consistency (if on teal background)

**Why markdown was abandoned**: reveal.js auto-animate requires consecutive sibling `<section data-auto-animate>` elements in `<div class="slides">`. The markdown plugin wraps all content in a single `<section data-markdown>`, making auto-animate impossible.

### reveal.js Feature Lookup Table

Use this table when deciding which reveal.js feature fits a pedagogical need. Each feature links to the official documentation for implementation details.

| Feature | Syntax | Pedagogical use case | Example context |
|---|---|---|---|
| **Fragment (default fade-in)** | `class="fragment"` | Revealing content step by step under teacher control | Answer rows on green answer slides, one at a time |
| **Fragment (strike)** | `class="fragment strike"` | Eliminating wrong options visually | Multiple choice — striking out incorrect answers |
| **Fragment (answer-correct)** | `class="fragment answer-correct"` | Revealing correct answer with green background (custom CSS) | T/F answer tables, grammar fill-in-the-blank |
| **Fragment (answer-incorrect)** | `class="fragment answer-incorrect"` | Revealing wrong answer with red background (custom CSS) | Error correction, wrong answer flagging |
| **Fragment (highlight-current-red/green/blue)** | `class="fragment highlight-current-red"` | Temporarily highlighting then returning to original | Vocabulary word in context, grammar element in a sentence |
| **Fragment (custom)** | Custom CSS + `class="fragment custom blur"` | Any visual effect — blur→focus, scale, color shift | Progressive focus on sentence parts (S → V → O) |
| **Fragment (fade-in-then-out)** | `class="fragment fade-in-then-out"` | Showing a temporary hint or scaffold that disappears | Scaffolding for weaker students during pair work |
| **Fragment (nested)** | Nested `<span class="fragment">` | Multi-step effect on the same text | Fade in ➝ highlight red ➝ strike through |
| **Fragment (grow/shrink)** | `class="fragment grow"` | Emphasising a single word on click | Key vocabulary word, grammar term |
| **Auto-animate** | `data-auto-animate` on 2+ consecutive `<section>` elements | Any visual transition between slides: border changes, position shifts, content building | Error→correction reveal, keyword underline, strategy step builds |
| **Auto-animate + code** | `data-auto-animate` + `<pre data-id="code">` + `data-line-numbers` | Building up code/text with syntax highlighting progression | Skimming/scanning lessons — highlight key sentences across slides |
| **Mark.js text highlighting** | `data-mark="1,3-5\|/pattern/"` on any element (uses Mark.js) | Highlighting arbitrary text (not code) with yellow `<mark>` background. Supports line numbers and regex. | Reading passages — call out key sentences, vocabulary in context. No monospace hack needed. |
| **Code blocks + line numbers** | `<pre><code data-line-numbers="1\|3-5\|7">` | Highlighting specific lines in a text passage, step by step | Reading comprehension — reveal main idea first, then details |
| **Per-slide transitions** | `data-transition="zoom"` or `data-transition="convex"` | Dramatic emphasis at a key moment | Transition into answer reveal, lesson climax, phase change |
| **Separate in/out transitions** | `data-transition="slide-in fade-out"` | Different transition entering vs leaving a slide | Moving from Teach to Practice phase |
| **Background gradient** | `data-background-gradient="linear-gradient(...)"` | Visual variety — phase transitions, mood shifts | Signalling a new lesson section |
| **Background video** | `data-background-video="assets/clip.mp4"` | Full-screen video hook (teacher-provided file only) | Lesson introduction (movie trailer, news clip) |
| **Background image** | `data-background-image="assets/file.jpg" data-background-opacity="1.0"` | Visual context for a topic (teacher-provided file only). ALL text MUST use `text-shield` or `text-shield-light`. | Lead-in discussion, topic introduction |
| **Background iframe** | `data-background-iframe="https://..."` | Live web content as slide backdrop | Google Forms poll, live dictionary, news site |
| **Auto-slide (timed advance)** | `data-autoslide="5000"` on a `<section>` | Self-advancing slides for timed reading | Speed-reading passages, timed grammar drills |
| **Lightbox (image)** | `data-preview-image` on `<img>` | Click-to-enlarge for detailed viewing | Textbook page close-ups, diagram details |
| **Lightbox (video)** | `data-preview-video` on any element | Click-to-play video overlay | Student example videos, extension media |
| **Lightbox (link)** | `data-preview-link` on `<a>` | Click-to-preview external link | Previewing a reference website |
| **Vertical slides** | Nested `<section>` inside a horizontal `<section>` | Backup/optional content, sub-steps, lesson extensions | Extra practice for fast finishers, grammatical sub-rules, optional extension activities |
| **Layout: r-fit-text** | `class="r-fit-text"` on heading | Auto-sizing text to fill the slide | Single powerful word, key concept, grammar rule summary |
| **Layout: r-stack** | `class="r-stack"` on container | Stacking elements on top of each other | Before/after comparisons, image overlays |
| **Layout: r-stretch** | `class="r-stretch"` on an element | Filling remaining vertical space | Maximising a screenshot or image within a slide |
| **Layout: r-frame** | `class="r-frame"` on element | Adding a border/frame, hover effect on links | Highlighting an image as clickable |
| **Text shield (dark)** | `class="text-shield"` on heading/p | Semi-transparent dark background behind text for readability on image backgrounds | Title or body text on `data-background-opacity="1.0"` slides |
| **Text shield (light)** | `class="text-shield-light"` on heading/p | Semi-transparent light gray background for dark-colored text on dark image areas | Dark text on full-opacity dark image backgrounds |
| **Text shield (fragment)** | `class="fragment text-shield-light"` | Text already visible; light gray background highlight appears on click (call-out effect) | Revealing a key point on an image-background slide |

**Decision flow:**
1. **Is the effect purely visual between slides?** (border appearing, colour change, word replacement) → **Auto-animate**
2. **Is the teacher revealing content step by step within a single slide?** → **Fragments**
3. **Is each step a discrete teaching moment that needs its own slide?** → **Sibling slides** (one per step, no auto-animate)
4. **Does the content need progressive highlighting within a text block?** → **Code + line numbers**
5. **Is the goal to enlarge or preview media?** → **Lightbox**
6. **Is the content optional / a backup?** → **Vertical slides**
7. **Does the slide need a dramatic entrance?** → **Per-slide transition**

## Pedagogical Strategy Slides — Design Principles

Strategy slides teach a test-taking or reading skill explicitly. The design follows a **modelled whole-task approach** consistent with Strategy-Based Instruction (SBI) in EFL/ESL reading pedagogy.

### Core Pattern: One Consistent Worked Example

Pick one real exam question and carry it through every step of the strategy. Never mix examples mid-flow. The student sees the complete process on a single item before attempting it alone.

Example: A True/False statement about the "generation gap" article runs through Steps 1–4. A Multiple Choice question runs through its own 3 steps. Do not switch between different exam items within the same strategy block.

### Step Structure

| Step | Cognitive function | What goes on the slide |
|---|---|---|
| 1 | Decode | Read the statement carefully. Note each separate claim. |
| 2 | Analyse | Break into Yes/No sub-questions. State the decision rule (Yes→TRUE / No→FALSE). |
| 3 | Locate | Identify which paragraph(s) contain the evidence. Name them explicitly. |
| 4 | Confirm | Show the original question in yellow. Quote the text that confirms each sub-answer. Conclude. |

### Slide Layout Rules

- **One step per slide** — each `<section>` covers a single step. This lets the teacher pause and check understanding at each decision point.
- **Header on first slide only** — `True/False Strategy` heading on Slide 1 of the block. Remaining slides show only the step label.
- **Original question in yellow** on first and last slides — `<p style="color:#ffdd00;"><em>"Statement text"</em></p>`
- **Underline step labels** — `<u><strong>Step N:</strong> ...</u>`
- **Real quotes on Step 4** — actual text excerpts from the article, in italics with the relevant phrase highlighted
- **Rule embedded at Step 2** — not a separate slide. Include it: "If you answer Yes to all → TRUE. If you answer No to even one → FALSE."
- **No auto-animate** — use `data-background-transition="none"` on all pedagogical sections. Teacher controls pacing.
- **Teal background** — `data-background="#1a6b5a"` + `class="pedagogical"` on all strategy slides.
- **Top alignment** — CSS: `align-self: flex-start; margin-top: 0; padding-top: 30px` on `.reveal .slides > section.pedagogical`. Do NOT use negative margins (they clip content off-screen). Do NOT use inline `style="top: 0;"` — reveal.js strips it during every layout cycle.

### Vertical Alignment Fix

Reveal.js `.slides` is a flex container that defaults to vertically centering its section children. The correct fix is positive padding, not negative margin:

```css
.reveal .slides > section.pedagogical {
    align-self: flex-start;
    margin-top: 0;
    padding-top: 30px;
}
```

Using `margin-top: -2.5%` pushes content off-screen top. A small positive `padding-top` on the section is reliable.

### Vertical Alignment for Pedagogical Slides

```html
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <h2>True/False Strategy</h2>
    ...
</section>
```

### Example: True/False Strategy (4 slides + worked example)

```html
<!-- Slide 1: Header + Step 1 + yellow question + tip -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <h2>True/False Strategy</h2>
    <p style="color:#ffdd00;"><em>"The author wrote the text to explore the generation gap and problems it can cause, and to suggest a possible solution."</em></p>
    <p><u><strong>Step 1:</strong> Read the statement carefully</u></p>
    <p>Sometimes there is more than one question to think about — note each part separately.</p>
</section>

<!-- Slide 2: Step 2 + sub-questions + rule -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <p><u><strong>Step 2:</strong> Work out what the question is asking you</u></p>
    <ul>
        <li>Did the author write about the generation gap? <em>(Yes/No)</em></li>
        <li>Did the author write about the problems it can cause? <em>(Yes/No)</em></li>
        <li>Did the author suggest a possible solution? <em>(Yes/No)</em></li>
    </ul>
    <p><strong>Rule:</strong> If you answer "Yes" to all → it's TRUE.<br />If you answer "No" to even one → it's FALSE.</p>
</section>

<!-- Slide 3: Step 3 + paragraph names -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <p><u><strong>Step 3:</strong> Find the evidence</u></p>
    <p>Keywords like "author" and "solution" are found in <strong>paragraphs A and F</strong>. Now we can answer each question from Step 2.</p>
</section>

<!-- Slide 4: Step 4 + yellow question + real quotes + answer -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <p><u><strong>Step 4:</strong> Answer the question</u></p>
    <p style="color:#ffdd00;"><em>"The author wrote the text to explore the generation gap..."</em></p>
    <p>You can see that the author:</p>
    <ul>
        <li>talks about the generation gap → <em>"There is a growing generation gap between people..."</em></li>
        <li>writes about the problems → <em>"This can cause serious problems in families and workplaces..."</em></li>
        <li>offers solutions → <em>"The only way to close the gap is through empathy..."</em></li>
    </ul>
    <p><strong>So the answer is: TRUE.</strong></p>
</section>
```

### Example: Multiple Choice Strategy (5 steps + auto-animate + table answers)

```html
<!-- Step 1: Header + demo question + options -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">

    <div style="overflow: hidden;">
    <h2>Multiple Choice Strategy</h2>
    <p>Now let's learn how to answer MC questions with an example.</p>
    <p style="color:#ffdd00;"><em>"What is the main message of this article?"</em></p>
    <ul>
        <li><strong>a)</strong> option text</li>
        <li><strong>b)</strong> option text</li>
        <li><strong>c)</strong> option text</li>
    </ul>
    <p><u><strong>Step 1:</strong> Read the question — Is it asking for detail or main idea?</u></p>
    </div>
</section>

<!-- Step 2a: Auto-animate entry — borders invisible -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" data-auto-animate>
    <div style="overflow: hidden;">
    <p><u><strong>Step 2:</strong> Underline key words</u></p>
    <p data-id="mcq" style="color:#ffdd00;"><em>"What is the <span data-id="w1" style="border-bottom: 2px solid transparent;">keyword</span> of this <span data-id="w2" style="border-bottom: 2px solid transparent;">word</span>?"</em></p>
    </div>
</section>

<!-- Step 2b: Auto-animate reveal — borders turn white -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" data-auto-animate>
    <div style="overflow: hidden;">
    <p><u><strong>Step 2:</strong> Underline key words</u></p>
    <p data-id="mcq" style="color:#ffdd00;"><em>"What is the <span data-id="w1" style="border-bottom: 2px solid white;">keyword</span> of this <span data-id="w2" style="border-bottom: 2px solid white;">word</span>?"</em></p>
    </div>
</section>

<!-- Step 3: Scan text -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <div style="overflow: hidden;">
    <p><u><strong>Step 3:</strong> Scan the text</u></p>
    <ul>
        <li>Detail questions: answer follows the order of the text</li>
        <li>Main idea: think about what the whole text is about</li>
    </ul>
    </div>
</section>

<!-- Step 4: Eliminate wrong answers — fragment strike table -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <div style="overflow: hidden;">
    <p><u><strong>Step 4:</strong> Eliminate wrong answers</u></p>
    <table class="answer-table">
        <thead><tr><th>Option</th><th>Why?</th></tr></thead>
        <tbody>
            <tr><td class="fragment strike" data-fragment-index="0"><strong>a)</strong> wrong option text</td><td class="fragment" data-fragment-index="0">Reason why wrong</td></tr>
            <tr><td class="fragment strike" data-fragment-index="1"><strong>b)</strong> wrong option text</td><td class="fragment" data-fragment-index="1">Reason why wrong</td></tr>
        </tbody>
    </table>
    </div>
</section>

<!-- Step 5: Confirm correct answer — table with citations -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <div style="overflow: hidden;">
    <p><u><strong>Step 5:</strong> Confirm your answer</u></p>
    <table class="answer-table wrap">
        <thead><tr><th>Answer</th><th>Why?</th></tr></thead>
        <tbody>
            <tr><td><strong>c)</strong> correct option text</td><td>Matches the article: <em>"quote from text"</em> (para X)</td></tr>
        </tbody>
    </table>
    </div>
</section>
```

### Answer Table Patterns (V1)

All answer slides use `answer-table` class with green background `#1e7e34`. The answer column and optionally the explanation column use fragments for clickthrough reveal.

**CRITICAL — Green slide text color: only white `#fff` or yellow `#ffdd00`.** Gray, blue, silver, or any muted color is invisible against `#1e7e34` at projection distance. Every text element on a green answer slide **must** be white or yellow — no exceptions. If a `<td>`, `<p>`, or `<span>` on a green slide uses any other color class, it is a bug.

**Grammar answer tables** (single-answer-per-row, e.g., fill-in-the-blank or choose-the-verb):

```html
<section data-background="#1e7e34">
    <h2>Practice 3A — Answers (1–6)</h2>
    <table class="answer-table">
        <thead><tr><th>#</th><th>Sentence</th><th>Answer</th></tr></thead>
        <tbody>
            <tr><td>1</td><td>One of my classmates ___ from my country.</td><td class="fragment answer-correct"><strong style="color:#ffdd00;">is</strong></td></tr>
            <tr><td>2</td><td>Some of the teachers ___ my language.</td><td class="fragment answer-correct"><strong style="color:#ffdd00;">speak</strong></td></tr>
            <!-- ... up to 6 rows for short items ... -->
        </tbody>
    </table>
</section>
```

**Multi-column grammar answer tables** (for subject/verb/object or multiple fields):

```html
<section data-background="#1e7e34">
    <h2>Practice 3 — Answers (1–5)</h2>
    <p class="aim-label">Subjects, Verbs, and Objects</p>
    <table class="answer-table">
        <thead><tr><th>#</th><th>Sentence</th><th>S</th><th>V</th><th>O</th></tr></thead>
        <tbody>
            <tr><td>1</td><td>My brother is in school.</td><td class="fragment answer-correct">My brother</td><td class="fragment answer-correct">is</td><td class="fragment">(none)</td></tr>
            <!-- ... all columns are fragments for simultaneous reveal per row ... -->
        </tbody>
    </table>
</section>
```

**Error-correction answer tables** (showing original error → correction):

```html
<section data-background="#1e7e34">
    <h2>Practice 4 — Answers (1–7)</h2>
    <p class="aim-label">Find and fix the errors</p>
    <table class="answer-table">
        <thead><tr><th>#</th><th>Original</th><th>Correction</th></tr></thead>
        <tbody>
            <tr><td>2</td><td>He ___ never on time.</td><td class="fragment answer-correct"><strong style="color:#ffdd00;">is</strong></td></tr>
            <tr><td>3</td><td>___ arrives ten minutes late.</td><td class="fragment answer-correct"><strong style="color:#ffdd00;">He</strong> (or Larry)</td></tr>
            <!-- ... correction column uses fragments for reveal ... -->
        </tbody>
    </table>
</section>
```

**Diagnostic test slide** (bespoke items, dark background, no timer):

```html
<section data-background="#1a1a2e">
    <h2>Diagnostic Test — Subject-Verb Agreement</h2>
    <p><em>Each sentence has ONE error. Find and fix it.</em></p>
    <ol style="font-size: 0.8em; text-align: left;">
        <li>George Lucas have changed the film industry.</li>
        <li>There is two main characters in Star Wars.</li>
        <li>Each of the movies have a different director.</li>
        <!-- ... 8 items, all visible on entry ... -->
    </ol>
    <aside class="notes">
        Stage 2 · 8 min · S
        Aim: To diagnose S-V agreement errors.
        Monitor and note which items cause most difficulty. Do NOT give answers yet.
    </aside>
</section>
```

**Grammar rule explanation slides** (teal background, pedagogical class, paired rules):

```html
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <h2>Subject-Verb Agreement: Rules 1–3</h2>
    <p><u><strong>Rule 1:</strong> Ignore prepositional phrases</u></p>
    <p><em>"The color <span style="color:#ffdd00;">of her eyes</span> changes."</em> → Subject is <strong>color</strong>, not <em>eyes</em>.</p>
    <p><u><strong>Rule 2:</strong> There + be → subject follows</u></p>
    <p><em>"There <span style="color:#ffdd00;">are</span> several kinds."</em> → <strong>kinds</strong> is the subject.</p>
    <p><u><strong>Rule 3:</strong> Each, one, neither, either → always singular</u></p>
    <p><em>"Each of the students <span style="color:#ffdd00;">has</span> a book."</em></p>
</section>
```

**2-column table (True/False, simple answers):**

```html
<section data-background="#1e7e34">
    <h2>Exercise N — Answers</h2>
    <table class="answer-table">
        <thead><tr><th>Statement</th><th>Answer</th></tr></thead>
        <tbody>
            <tr>
                <td>statement text</td>
                <td class="fragment answer-correct">✓ Correct</td>
            </tr>
            <tr>
                <td>another statement</td>
                <td class="fragment answer-incorrect">✗ Incorrect</td>
            </tr>
        </tbody>
    </table>
</section>
```

**3-column table (with explanation):**

```html
<section data-background="#1e7e34">
    <h2>Exercise N — Answers</h2>
    <table class="answer-table">
        <thead><tr><th>Statement</th><th>Answer</th><th>Why?</th></tr></thead>
        <tbody>
            <tr>
                <td>statement text</td>
                <td class="fragment answer-correct">✓ Correct</td>
                <td class="fragment">explanation with paragraph reference</td>
            </tr>
            <tr>
                <td>another statement</td>
                <td class="fragment answer-incorrect">✗ Incorrect</td>
                <td class="fragment">explanation with paragraph reference</td>
            </tr>
        </tbody>
    </table>
</section>
```

For answer tables with long explanation text that must wrap, add class `wrap`:
```html
<table class="answer-table wrap">
```

### Fragment Strike Confirmed Behavior

Per `knowledge-base\revealjs-packed.json` (line 127-134):
```css
.reveal .fragment.strike { opacity: 1; visibility: inherit; }
.reveal .fragment.strike.visible { text-decoration: line-through; }
```
**Do NOT override this CSS** in the `<style>` block. Text is always visible; strikethrough appears on click only. Any custom `.reveal .fragment.strike` CSS in the page will break this behavior.

### Code Blocks for Reading Passage Highlights

Use reveal.js code highlighting (`data-line-numbers`) to progressively reveal specific lines in a text passage. This is ideal for **skimming and scanning lessons** — the teacher can highlight the main idea first, then key details, then vocabulary in context.

**Pattern — step-by-step text passage reveal with auto-animate:**

```html
<section data-auto-animate>
  <pre data-id="reading" style="font-size: 0.7em;"><code data-trim data-line-numbers="1-5|6,8,10|12-15">
    Filmmaker George Lucas has changed the film industry in many ways.
    He has written, directed, and produced some of the best-loved movies of our time.
    He has also made major contributions to modern film technology.
    At first, Lucas did not plan to become a filmmaker.
    His first dream was to become a race car driver.

    After a bad accident, however, he decided to go to college.
    In college, Lucas studied movie-making and made a number of student films.

    Lucas's third feature film, Star Wars, changed everything.

    A seemingly simple story of good versus evil, Star Wars became a huge international hit.
    The movie used new technologies that revolutionized the film industry.

    To sum up, George Lucas's love of storytelling and his technological innovations
    have transformed movie-making forever.
  </code></pre>
</section>
<section data-auto-animate>
  <pre data-id="reading" style="font-size: 0.7em;"><code data-trim data-line-numbers="1-5|6,8,10|12-15">
    Filmmaker George Lucas has changed the film industry in many ways.
    He has written, directed, and produced some of the best-loved movies of our time.
    He has also made major contributions to modern film technology.
    At first, Lucas did not plan to become a filmmaker.
    His first dream was to become a race car driver.

    After a bad accident, however, he decided to go to college.
    In college, Lucas studied movie-making and made a number of student films.

    Lucas's third feature film, Star Wars, changed everything.

    A seemingly simple story of good versus evil, Star Wars became a huge international hit.
    The movie used new technologies that revolutionized the film industry.

    To sum up, George Lucas's love of storytelling and his technological innovations
    have transformed movie-making forever.
  </code></pre>
</section>
```

- `data-line-numbers="1-5|6,8,10|12-15"` creates 3 clickthrough steps: first highlights lines 1-5, then lines 6/8/10, then lines 12-15
- The `|` character separates highlight steps — each press of the right arrow advances to the next step
- `data-auto-animate` on both `<section>` elements makes the transition between slides smooth
- `data-trim` removes surrounding whitespace
- The `<pre>` must have a matching `data-id` across both slides for auto-animate to work
- Adjust `font-size` (0.7em–0.85em) based on passage length

**Pattern — single-slide text passage with fragments (no auto-animate):**

```html
<section data-background="#1a1a2e">
  <h2>Find the Main Idea</h2>
  <pre style="font-size: 0.75em;"><code data-trim data-line-numbers="1-15">
    Filmmaker George Lucas has changed the film industry...
    ...
    have transformed movie-making forever.
  </code></pre>
  <p class="fragment" style="color:#ffdd00;"><strong>Main idea:</strong> George Lucas transformed filmmaking through innovation.</p>
  <p class="fragment" style="color:#aaa;"><strong>Supporting detail 1:</strong> He created Star Wars.</p>
  <p class="fragment" style="color:#aaa;"><strong>Supporting detail 2:</strong> He developed new film technology.</p>
  <aside class="notes">
    Stage 2 · 8 min · Ss-Ss
    Aim: To identify the main idea of the text
    Step 1: Students read silently. Step 2: Elicit main idea. Step 3: Reveal details.
  </aside>
</section>
```

**Key rules for code/text passages:**
- Use `<pre><code data-trim data-line-numbers="...">` for wrapping text
- The `data-line-numbers` attribute accepts comma-separated lines, ranges (1-5), and step separators (`|`)
- Line numbers are 1-based (first line of text = 1)
- For auto-animate across slides: add `data-id` to the `<pre>` element, matching on both slides
- The highlight plugin is already loaded in the base template — no additional setup needed
- See [reveal.js code documentation](https://revealjs.com/code/) for full details

### Text Shield for Full-Opacity Image Backgrounds

**MANDATORY RULE: Every element on a slide with `data-background-image` MUST use `text-shield` or `text-shield-light`.** No text on an image-background slide is exempt — headings, body text, labels, and footers all need shielding. Solid-color and gradient backgrounds do not need shielding.

The `text-shield` classes add a semi-transparent background behind the text, ensuring readability at full image vibrancy (`data-background-opacity="1.0"`).

```html
<section data-background-image="assets/george-lucas.jpg" data-background-opacity="1.0">
    <h2 class="text-shield">George Lucas: A Filmmaker Who Changed Cinema</h2>
    <p class="text-shield">Dark background shield for white text — readable on any image area.</p>
    <p><span class="text-shield-light" style="color:#222;">Light background shield for dark text.</span></p>
    <p><span class="fragment text-shield-light">Text always visible; light gray highlight appears on click.</span></p>
    <aside class="notes">
        text-shield = dark (rgba(0,0,0,0.55)) for white text
        text-shield-light = light (rgba(200,200,200,0.65)) for dark text
        Fragment variant: text visible, background highlights on click.
    </aside>
</section>
```

**Rules:**
- `class="text-shield"` — dark semi-transparent background for white text. Use on dark theme slides.
- `class="text-shield-light"` — light gray semi-transparent background for dark-colored text. Use on light theme slides.
- `class="fragment text-shield-light"` — text visible at slide entry; light gray background highlight appears on click. Use for call-out effects without hiding text.
- **Subtitle-style shielding**: These classes use `display: inline-block` + `max-width: 90%`. The background box stays tight to the text (inline-block shrinks to content width). Long text wraps at 90% of the slide width, preventing full-width bars. Elements stack naturally with standard block-level spacing — no `::after` artifacts.
- Both classes apply `text-shadow: none` — the background shield replaces the need for text shadow.
- Always pair with `data-background-image` and `data-background-opacity="1.0"` on the `<section>`.
- **All text-bearing elements** on the slide (headings, paragraphs, list items, labels, footers) must use one of the two text-shield classes. No unshielded text on an image background.

### Text Highlighting with `data-mark` (Mark.js Plugin)

The mark plugin uses [Mark.js](https://markjs.io) to highlight arbitrary text with a yellow background `<mark>` element. Unlike `data-line-numbers` (which requires `<pre><code>` blocks and forces monospace), `data-mark` works on **any HTML element** — paragraphs, blockquotes, lists, headings.

**IMPORTANT:** The mark plugin is NOT included in the base template by default. Any plugin added to `Reveal.initialize({ plugins: [...] })` runs at startup — if its `init()` function crashes, the ENTIRE presentation shows a blank page with no error message. The mark plugin was removed from the base template after a runtime compatibility issue. To use it, follow the Plugin Safety Protocol below.

**Setup (if needed):**
1. Download `templates/mark-plugin.js` (exists as reference)
2. Load Mark.js from CDN: `<script src="https://cdn.jsdelivr.net/npm/mark.js@8.11.1/dist/mark.min.js"></script>`
3. Load the plugin: `<script src="mark-plugin.js"></script>`
4. Add `RevealMark` to the `plugins` array in `Reveal.initialize()`
5. **Test in browser** — open the page, check console for errors. If blank, remove the plugin immediately.

```html
<!-- Mark individual lines: line 1, then lines 3-5 -->
<p data-mark="1|3-5">Line 1 visible and marked from start.
Line 2 never marked.
Lines 3, 4, and 5 marked on click.</p>

<!-- Mark regex pattern: nothing, then "creative", then line 5 -->
<blockquote data-mark="|/creative/|5">
    Filmmaker George Lucas has changed the film industry in many ways.
    He has written, directed, and produced some of the best-loved movies.
    A seemingly simple story of good versus evil, Star Wars became a hit.
    The movie used new technologies that revolutionized the industry.
    To sum up, George Lucas has transformed movie-making forever.
</blockquote>

<!-- Mark different patterns step by step -->
<div data-mark="|/changed/|/technology/">
    <p>George Lucas has changed the film industry.</p>
    <p>He developed new film technology.</p>
</div>
```

**Key rules:**
- `data-mark="1,3-5"` — mark lines 1, 3, 4, 5 on slide entry (no fragments)
- `data-mark="|/creative/|5"` — 3 steps: nothing → highlight "creative" → highlight line 5. The `|` separates steps
- Steps can mix line numbers and regex patterns: `data-mark="1-3|/main idea/|5"`
- Regex patterns are delimited by any non-pipe, non-digit character: `/pattern/`, `#pattern#`, `"pattern"`
- The plugin creates `<mark data-markjs="true">` elements with default yellow styling
- The base template already loads `mark.js` (CDN) and `mark-plugin.js` (local) — no extra setup needed
- See [reveal-mark-plugin](https://github.com/stlab/reveal-mark-plugin) for full syntax

### revealjs-validator (Post-Build Validation)

The project includes `revealjs-validator` as a dev dependency. Run it after building slides to catch common Reveal.js errors (broken auto-animate pairs, invalid fragment classes, CSS misuse, missing assets, etc.):

```bash
# Validate all slides in a presentation
npx revealjs-validator --project "output/{subfolder}/slides/"

# Validate with auto-fix
npx revealjs-validator --fix --project "output/{subfolder}/slides/"

# List all 66 rules
npx revealjs-validator --list-rules
```

The validator checks 66 rules derived from the official Reveal.js documentation. Key rules relevant to this skill:
- `auto-animate-pairs` — consecutive `data-auto-animate` slides must match
- `valid-fragment-classes` — fragment effects need the base `fragment` class
- `cross-assets-exist` — image and audio files referenced in slides must exist
- `notes-inside-section` — `<aside class="notes">` must be direct child of `<section>`
- `vertical-slides-nesting` — vertical slides must be exactly one level deep
- `code-line-numbers-structure` — `data-line-numbers` must be on `<code>` inside `<pre>`
- `no-css-background-on-section` — use `data-background-*` attributes, not inline CSS
- `cross-css-classes-used` — CSS classes in HTML not defined in any stylesheet

See [revealjs-validator](https://github.com/maciejdzierzek/revealjs-validator) for full documentation.

### Plugin Safety Protocol

**Adding ANY plugin to the base template's `plugins` array is a safety-critical operation.** If a plugin's `init()` function throws an error, reveal.js cannot initialize and the entire presentation shows a blank page — with NO visible error message. The revealjs-validator cannot detect this.

Follow this protocol whenever adding, updating, or enabling a plugin:

1. **Add to the `plugins` array LAST** — build and test without the new plugin first. Confirm the presentation works.
2. **Add one plugin at a time** — never add multiple untested plugins simultaneously. If the page breaks, you won't know which one caused it.
3. **Test in browser** — open the slides, press `F12` → **Console tab**. Verify:
   - The page shows content (not blank/white)
   - There are ZERO red error messages in the console
   - The presentation navigates correctly (next/prev slides, fragments work)
4. **Check init-time dependencies** — if the plugin depends on an external JS library (e.g., mark.js, jQuery), verify that library is loaded and functional BEFORE the plugin script runs. CDN failures, CSP restrictions, or ad blockers can silently block library loading, causing the plugin's `init()` to crash.
5. **Isolate on failure** — if the page is blank, immediately remove ALL recently added plugins from the `plugins` array. Re-add them one at a time, testing after each addition.
6. **Document in this file** — after a plugin passes testing, update this SKILL.md with setup instructions, dependency requirements, and any known caveats.

**Why plugins crash at init (common causes):**
- Plugin references a global variable that's undefined (e.g., `window.Mark`, `window.jQuery`)
- Plugin uses an ES module `import` but is loaded via `<script>` tag (module is undefined)
- Plugin is incompatible with the installed reveal.js version
- CDN for a plugin dependency fails due to network/CORS/ad-blocker — the plugin script itself might load fine, but its dependency doesn't
- Plugin calls a reveal.js API method that was renamed or removed in the current version

## Common Pitfalls — Lessons from Build Sessions

### Unicode: em dashes, en dashes, hyphens

These three characters are **different Unicode codepoints** but look identical on screen:

| Character | Codepoint | Name | Python escape |
|-----------|-----------|------|---------------|
| `—` | U+2014 | Em dash | `\u2014` |
| `–` | U+2013 | En dash | `\u2013` |
| `-` | U+002D | Hyphen | (keyboard minus) |

**Rule:** Use em dash (`—`, U+2014) consistently throughout all slides — never mix with en dash. In Python verification scripts, define `ED = "\u2014"` once and reuse.

**If a `string in content` check fails unexpectedly:** The console shows `�` for these characters. Dump hex bytes near the target:

```python
idx = content.find("first_word_of_target")
if idx >= 0:
    print(content[idx:idx+60].encode("utf-8").hex())
    print(repr(content[idx:idx+60]))
```

Compare hex sequences to find codepoint mismatches.

### Temp file workflow (proven pattern)

This is the ONLY reliable approach given the tooling constraints:

1. **Write slide sections** to `C:\Users\elwru\AppData\Local\Temp\kilo\slides_sections.html` via the Write tool (this path has no permission restrictions)
2. **Copy template** to output dir via PowerShell `cp`
3. **Write splice script** to `C:\Users\elwru\AppData\Local\Temp\kilo\splice_slides.py` — uses template boundary detection (see Step 4B for the pattern)
4. **Run splice script** via `python ...\splice_slides.py`
5. **Write verification script** to `C:\Users\elwru\AppData\Local\Temp\kilo\verify_slides.py` — uses `in` + `repr()` for Unicode-safe checking (see Step 5)
6. **Clean up** temp files only after verification passes

**Do NOT:**
- Write large files (>300 lines) directly via the Write tool to `output/` — may hit permission blocks
- Use PowerShell `>`, `Out-File`, or `Set-Content` for files with Unicode characters — they add BOM or corrupt codepoints
- Use `\u2014` in PowerShell strings — PowerShell's quoting will break the escape

### Auto-animate vs Fragments — when to use which

**Use auto-animate** when the slide shows a **transformation** — content that changes, combines, or builds structurally across slides. Students need to see the process, not just the result:

- Verb tense changing (walk → walked → had walked)
- Sentence structure assembly (adding subject, then verb, then object across slides)
- Scoring rubric reveals where criteria highlight/unhighlight across slides
- Any "before and after" where elements morph (lowercase → capitals, singular → plural)
- Grammatical transformations (active → passive, direct → reported speech)

Auto-animate requirements:
- All sibling `<section>` elements consecutive in `<div class="slides">` — no other slides between them
- Matching `data-auto-animate-id` on all sections in the block
- `data-id` attributes on elements that persist between slides (content that changes color, size, or opacity)
- `autoAnimateUnmatched: true` in `Reveal.initialize()` for elements that appear/disappear between slides — already in the template

**Use `class="fragment"`** when the slide just **reveals content** that was already there but hidden — no morphing, no transformation:

- Answer reveals (✓/✗ appearing, correct answers)
- Instruction steps appearing one by one
- Lists showing incrementally (definition lists, vocabulary)
- Examples appearing after a rule is stated
- Strategy steps revealed one at a time on a pedagogical slide
- Any content that simply appears (opacity 0 → 1) without changing

**Key test:** If the element changes form between slides (text changes, borders appear, case changes), use auto-animate. If the element just appears/disappears, use fragments.

**Bad candidates for auto-animate:** Answer reveal slides, definition lists, example reveals, task instructions — all of these should use fragments instead.

## reveal.js Codebase

When making changes to reveal.js code (e.g., custom themes, configuration, or plugin modifications), **always query the live GitHub repository first**. Do not rely on static snapshots — the live codebase is the source of truth.

### Query Live reveal.js via Git

Use `gh` (GitHub CLI) to fetch individual files from the live repository. This is faster than cloning and always returns the current version.

```bash
# Get a specific file from the latest version
gh api repos/hakimel/reveal.js/contents/css/reveal.scss --jq '.content' | base64 -d

# Get the compiled CSS
gh api repos/hakimel/reveal.js/contents/dist/reveal.css --jq '.content' | base64 -d

# Get the main JS source
gh api repos/hakimel/reveal.js/contents/js/reveal.js --jq '.content' | base64 -d | head -200

# List the top-level directory structure
gh api repos/hakimel/reveal.js/contents/ --jq '.[].name'

# Search the codebase for a specific pattern (uses GitHub code search)
gh search code "data-auto-animate" --repo hakimel/reveal.js --limit 10

# Get a file from a specific tag/version
gh api repos/hakimel/reveal.js/contents/css/reveal.scss?ref=5.1.0 --jq '.content' | base64 -d
```

To see how a specific feature works (e.g., `autoAnimateUnmatched`), search the JS source:
```bash
gh api repos/hakimel/reveal.js/contents/js/reveal.js --jq '.content' | base64 -d | Select-String -Pattern "autoAnimateUnmatched" -Context 0,5
```

## Files

| File | Purpose |
|---|---|
| `docs/slide-design-reference.md` | Slide design rules (authoritative) |
| `templates/base-slides-template.html` | **Base template for ALL new presentations** |
| `templates/slides-template.html` | **DEPRECATED** — markdown-based (kept for backward compat) |
| `scripts/json_to_markdown.py` | **DEPRECATED** — markdown generator (not for new work) |
| `scripts/pixabay_download.py` | Pixabay image downloader (first-gen only) |
| `scripts/locate_slide.py` | Map reveal.js URL index to HTML section |
| `templates/ACT.png` | Institution logo (ACT) — copy to `assets/logo.png` |
| `templates/ACT.png` | Institution logo (ACT) — copy to `assets/logo.png` |

## Dependencies
- Python 3.x + Pillow
- reveal.js 5.1.0 via CDN (no npm needed)
- `templates/base-slides-template.html` (copied to `output/{subfolder}/slides/index.html`)
