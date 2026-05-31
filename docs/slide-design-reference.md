# Slide Design Reference — ESL Lesson Presentations

This document defines how lesson plan JSON stages map to reveal.js slides. It is the **authoritative design reference** for all presentations. Agents build slides by following these patterns using raw HTML `<section>` elements inside the base template.

The base template is at `templates/base-slides-template.html` — copy it to `output/{subfolder}/slides/index.html` for each new presentation.

---

## Context

- **Teacher controls all slides** — students never interact directly
- **Slides support the teacher's narration, not replace it**
- **Reveal.js 5.x** via CDN, raw HTML `<section>` elements, 1280×720
- **Base template**: `templates/base-slides-template.html` — copy to `output/{subfolder}/slides/index.html`, then add `<section>` elements
- **Markdown is permanently abandoned** — auto-animate requires sibling `<section>` elements, incompatible with the `<section data-markdown>` wrapper
- **CEFR levels**: A1, A2, B1, B2, C1, C2

---

## Core Principles

1. **Exercise content NOT on screen** — students have the workbook. Task slides show only the exercise number and a brief instruction. Do NOT reproduce exercise text (MC options, gap-fill sentences, checklists) on screen.
2. **Procedure text NEVER on screen** — teacher instructions, timing, interaction patterns go in `<aside class="notes">`
3. **Fragments reserved for answer reveal** — the teacher reveals answers one at a time after students have worked. This is the primary use of fragments. Use `data-fragment-index` to control reveal order.
4. **Auto-animate for keyword emphasis, not answer reveals** — use consecutive `<section data-auto-animate>` elements with matching `data-auto-animate-id` to animate underline highlights on key terms. Do NOT use auto-animate for answer reveals — use fragments instead.
5. **No gray text on any background** — all text must be solid white `#fff` or yellow `#ffdd00`. Gray `#888`, `#666`, and low-opacity white (`rgba(255,255,255,0.5)`) are banned. At projection distance, these render invisible.
6. **Four-slide block per exercise type** — every distinct exercise follows: Transition (red) → Pedagogical (teal) → Task (dark) → Answers (green).
7. **Audio on task slides, not pedagogical slides** — the audio player sits on the task slide with the exercise number. Pedagogical slides focus on strategy instruction with no playback controls.
8. **WHY line on every answer** — each answer row has a yellow WHY line (transcript quote for listening, grammar rule for language exercises) that appears simultaneously with the answer.
9. **Student-facing differentiation text** — challenge options read "Want a challenge?…", not "Stronger Ss…". Marked with checkered flag icon `fa-flag-checkered`.
10. **Prediction before task** — students guess before doing, confirm with answer reveal
11. **Answer slides: max 3 items** — split exercises with >3 items across multiple slides (e.g., `-1-3`, `-4-5`). Each row uses answer-list flex layout with a-cor/a-inc and WHY.
12. **Vocabulary pre-teach** — slides AFTER lead-in stage, one word per slide on dark background
13. **Section transitions** between stages — heading only, red background (`#c0392b`), no descriptive paragraphs
14. **Text highlighting** — all slides use text-shadow for readability; pedagogical slides use white-on-teal; vocabulary words use yellow boldface (`#ffdd00`)

---

## Audience Constraints (CEFR-Adaptive)

The default targets **Mathayom Thai students (CEFR B1)**. See the `Authorial Voice & Audience` section in the skill for B2+ relaxations. These constraints ensure student-facing text is immediately comprehensible.

### Vocabulary Ceiling
No words above CEFR B1 on screen without inline definition:
- **Banned**: "identify", "predict", "convincing", "distinguish", "evaluate", "analyze", "infer"
- **Useinstead**: "find", "guess", "makes sense", "tell the difference", "decide", "look at", "understand what the writer means"

### Sentence Complexity
- Max 15 words per sentence on screen
- No semicolons — break into two sentences
- One clause preferred, two max
- No passive voice on screen

### Per-Slide-Type Language Guidelines

| Slide type | B1 rule | Bad example | Good example |
|-----------|---------|-----------|--------------|
| **Objective** | Frame as "what you CAN do" | "By the end, you will have practiced identifying the main idea" | "I can find the main idea of an article" |
| **Task instruction** | Use direct imperatives only | "Students read the article and complete Exercise 2" | "Read the article. Do Exercise 2." |
| **Transition** | Simple warm-up questions | "What do you predict the text will be about?" | "What do you think the text is about?" |
| **Discussion** | Concrete yes/no or choice prompts | "How does this topic connect to broader societal themes?" | "Do you agree? Why or why not?" |
| **Summary** | Use "I can..." statements | "Identify the main purpose of a text" | "I can find the main idea" |

### Max Text Limits (B1-adjusted)

| Slide type | Max total words on screen |
|-----------|-------------------------|
| Title | 18 |
| Objective | 25 (3  8-word outcomes) |
| Vocabulary | 35 (4 words  9 words each) |
| Lead-in image | 8 (1 question) |
| Pre-reading prediction | 5 (2 prompts  2-3 words) |
| Task instruction | 15 |
| Answer explanation | 35 per question |
| Section transition | 8 (1 question) |
| Post-reading discussion | 18 (2-3 questions) |
| Summary | 12 (3  4-word outcomes) |
| End | 5 |

---

### Text highlighting (all slides)

All slide text (h2, h3, p, li) uses consistent styling via CSS in `templates/base-slides-template.html`:

- **Text shadow**: `<text-shadow: 2px 2px 4px rgba(0,0,0,0.8)>` on all headings and body text
- **Pedagogical slides**: `class="pedagogical"` + `data-background-color="#1a6b5a"` — white text with teal background, white border-bottom on h2
- **Vocabulary words**: `<span class="vocab-word">word</span>` — yellow (`#ffdd00`) bold with text shadow
- **Transitions**: `data-background-color="#c0392b"` — red background
- **End slide**: `data-background-color="#2c3e50"` — dark background

---

## Fragment Policy

| Use fragments for | DO NOT use fragments for |
|---|---|
| Revealing answers (one at a time) | Task instructions |
| Showing wrong→right (highlight-red, then correct) | Vocabulary lists |
| Parts of speech (highlight-blue on grammar elements) | Objectives/outcomes |
| Auto-animate word transformations | Discussion questions |
| Key vocabulary emphasis (grow) | Stage aims |
| | Lead-in images and prompts |
| | Material references |

Fragment styles allowed:

| Style | Use |
|-------|-----|
| `highlight-green` | Correct answer confirmed |
| `highlight-red` | Incorrect answer (pair with explanation of why wrong) |
| `grow` | Emphasize key vocabulary word (single word only) |
| `highlight-blue` | Grammar point / part of speech labeling |
| `fade-in` | Smooth reveal of one image element |
| `custom` | Change specific CSS properties on click (border, color, opacity) without hiding underlying text. Define `.fragment.custom.*` (default) and `.fragment.custom.*.visible` (revealed) CSS rules. |

**Important:** `fragment custom` prevents reveal.js from applying `opacity: 0; visibility: hidden`, so the element text stays fully visible at all times. Only the CSS properties you define in your `.visible` rules change on click. This is the correct approach whenever you need to transform an element's appearance (e.g., adding an underline, changing border color) without concealing its content.

---

## HTML Section Rules

These are the ONLY allowed patterns. Agents must not invent alternatives. All slides are raw HTML `<section>` elements.

### Slide elements
```html
<section>                    ← standalone slide
<section data-background-color="#c0392b">   ← slide with attributes
<section data-auto-animate data-auto-animate-id="same-id">  ← auto-animate pair
<section data-background-image="assets/image.jpg" data-background-opacity="1.0">  ← image background
<section data-timer="300">   ← timer pill (seconds)
<section data-mark="1,3-5|/pattern/">  ← Mark.js text highlighting (steps separated by |)
```

### Fragments (classes on elements)
```html
<p class="fragment highlight-green">✓ <strong>Correct</strong></p>
<p class="fragment highlight-red">✗ <strong>Wrong</strong></p>
<p class="fragment strike">Eliminated answer</p>
<span class="fragment grow">word</span>
<span class="fragment">Generic reveal</span>
```

### Speaker notes
```html
<aside class="notes">
    Full teacher script goes here.
    Multi-line notes supported.
</aside>
```

### Vocabulary words
```html
<span class="vocab-word">generation gap</span>
```

### CEFR badges
```html
<span class="cefr-badge B1">B1</span>
```

---

## Slide Type Templates

### 1. Title Slide
```html
<section data-background-image="assets/pixabay_XXXXXXX_1.jpg" data-background-opacity="0.7">
    <img src="assets/logo.png" class="title-logo" alt="Logo" />
    <h1>{{ topic }} <span class="cefr-badge {{ cefr_level }}">{{ cefr_level }}</span></h1>
    <p><em>{{ strap_subheader }}</em></p>
</section>
```

- Logo centered at top with `class="title-logo"` — CSS: `display:block; max-height:100px; margin:0 auto 1em;`
- `data-background-image` with `data-background-opacity="0.7"` — full-bleed background, dimmed so text reads without a text-shield
- Title in standard size with CEFR badge, strap subheader below
- **No logo in title area**: add `<link rel="stylesheet" href="timer-plugin.css" />` in `<head>` and add the `.title-logo` CSS rule to the `<style>` block:
```css
.reveal .title-logo { display: block; max-height: 100px; margin: 0 auto 1em; }
```
- CEFR badge colors: A1=green, A2=light green, B1=blue, B2=dark blue, C1=purple, C2=red

### 2. Objective Slide (all visible at once)
```html
<section>
    <h2>Here's what you'll be able to do</h2>
    <ul>
        <li>{{ outcome_1 }}</li>
        <li>{{ outcome_2 }}</li>
        <li>{{ outcome_3 }}</li>
    </ul>
    <p><em>These are the same skills you need for the PET reading test!</em></p>
</section>
```

3 outcomes max, each ≤10 words. NO fragments — students need to see this as orientation.

### 3. Vocabulary Slides (one word per slide with Pixabay background)
**Generated after lead-in stage**

The script automatically converts formal stage names to friendly student-facing language:
- "Lead-in" → "Let's get Started"
- "Post-reading speaking task" → "Let's Discuss"
- "Wrap-up and reflection" → "Let's Review"
```html
<!-- First word (with header) -->
<section class="vocab-slide" data-background-image="assets/vocab-XXXXXX.jpg" data-background-opacity="1.0">
    <h2 class="text-shield">Important Words</h2>
    <p class="text-shield"><span class="vocab-word">{{ word }}</span></p>
    <p class="text-shield"><em>{{ phonemic }}</em></p>
    <p class="text-shield"><em>There's such a <span class="vocab-word">{{ word }}</span> between them; they never agree on anything.</em></p>
</section>

<!-- Subsequent words (no header) -->
<section class="vocab-slide" data-background-image="assets/vocab-XXXXXX.jpg" data-background-opacity="1.0">
    <p class="text-shield"><span class="vocab-word">{{ word }}</span></p>
    <p class="text-shield"><em>{{ phonemic }}</em></p>
    <p class="text-shield"><em>There's such a <span class="vocab-word">{{ word }}</span> between them; they never agree on anything.</em></p>
    <aside class="notes">
        Drill: teacher says → class repeats (×3).
        Show image as visual anchor for meaning.
    </aside>
</section>
```

Rules:
- **One vocabulary item per slide** — max 5 words total
- Word + phonemic script (IPA) + bolded target word in context sentence
- **Sentence must imply meaning, NOT define** — e.g., "There's such a **generation gap** between Rico and Ploy; Ploy doesn't understand the slang words Rico uses." (GOOD) vs "generation gap — the difference between two groups or generations" (BAD)
- **Pixabay background at 100% opacity** — image must precisely convey word meaning and context
- Title: "Important Words"
- All visible at once — NO fragments

### 4. Lead-In Image Slide
```html
<section data-background-image="assets/pixabay_XXXXXXX_1.jpg" data-background-opacity="1.0">
    <h2 class="text-shield">Let's get Started</h2>
    <h3 class="text-shield">{{ open_question }}</h3>
    <aside class="notes">
        {{ teacher_activation_script }}
        Display image for 20 seconds silently.
        Then ask the question. Elicit 3-4 responses.
        Connect responses to today's topic.
    </aside>
</section>
```

One open question only. Image as background. Speaker notes: activation script.

### 5. Four-Slide Exercise Block (canonical pattern)

Every distinct exercise type follows this four-slide sequence. This is the **only** pattern for listening, reading, and language exercises.

| Step | Slide type | Background | Content | Audio/Timer |
|------|-----------|------------|---------|-------------|
| 1 | **Transition** | `#c0392b` (red) | Heading only — "Listen for Main Ideas", "Finding Details", "Useful Phrases" | Neither |
| 2 | **Pedagogical** | `#1a6b5a` (teal) `class="pedagogical"` | Strategy instruction. Auto-animate for keyword underline reveals. 🏁 challenge text here. | **No audio** |
| 3 | **Task** | `#1a1a2e` (dark) | Exercise number + brief instruction only. **No exercise text** — students have workbook. | `data-audio-src` OR `data-timer` (never both) |
| 4 | **Answers** | `#0d5e1a` (green) | answer-list flex, max 3 items, each with answer + WHY line in yellow | Neither |

```html
<!-- Transition -->
<section id="slide-transition-{name}" data-background-color="#c0392b">
    <h2>Student-friendly heading</h2>
</section>

<!-- Pedagogical (strategy) -->
<section id="slide-strategy-{name}" class="pedagogical" data-background-color="#1a6b5a" data-background-transition="none">
    <h2>Strategy Title</h2>
    <ul>
        <li>Step 1: ...</li>
        <li>Step 2: ...</li>
    </ul>
    <p style="color:#ffdd00;"><i class="fa-solid fa-flag-checkered" style="color:#ffdd00;"></i> Want a challenge? ...</p>
    <aside class="notes">Teacher notes here.</aside>
</section>

<!-- Task -->
<section id="slide-ex{n}-task" data-background-color="#1a1a2e" data-audio-src="assets/listen{n}.mp3">
    <h2>Exercise {n}</h2>
    <p>Open your workbook to page X. Listen and complete the task.</p>
    <aside class="notes">Teacher notes with differentiation.</aside>
</section>

<!-- Answers (max 3 items per slide) -->
<section id="slide-ex{n}-answers-1-3" data-background-color="#0d5e1a">
    <h2>Exercise {n} — Answers (1–3)</h2>
    <div class="answer-list">
        <div class="a-row">
            <span class="a-num">1.</span>
            <span class="a-q">Question snippet</span>
            <span class="fragment fade-up a-ans a-cor" data-fragment-index="1"><i class="fa-solid fa-check"></i> Answer</span>
            <span class="fragment fade-up" data-fragment-index="1" style="width:100%; color:#ffdd00; font-size:0.95em; text-align:left;">WHY: Transcript quote or grammar rule.</span>
        </div>
    </div>
</section>
```

### 6. Task Instruction Slide
```html
<section data-background-image="assets/pixabay_XXXXXXX_1.jpg" data-background-opacity="1.0">
    <h2 class="text-shield">Before you read: {{ article_title }}</h2>
    <ul class="text-shield">
        <li>What problem does the writer describe?</li>
        <li>What solution do they suggest?</li>
    </ul>
    <aside class="notes">
        Students read the title and look at the photo.
        Give them 30 seconds to share predictions in pairs.
        Write 2-3 predictions on the board.
    </aside>
</section>
```

### 6. Task Instruction Slide
```html
<section id="slide-ex{n}-task" data-background-color="#1a1a2e" data-audio-src="assets/listen{n}.mp3">
    <h2>Exercise {{ number }}</h2>
    <p>{{ brief_student_instruction }}</p>
    <aside class="notes">
        Stage {{ number }} · {{ time }} min · {{ interaction }}
        Goal: {{ stage_aim }}
        Differentiation notes here.
    </aside>
</section>
```

Rules:
- Exercise number only on screen — **no exercise text**. Students have the workbook.
- Brief instruction: 1 sentence max (e.g., "Open your workbook to page 9. Listen and choose the correct answers.")
- Audio (`data-audio-src`) OR timer (`data-timer`) — **never both** on the same slide
- Full procedure in speaker notes with differentiation guidance
- The audio file must be a unique filename per slide (copy to `listen1.mp3`, `listen2.mp3`, etc.) — the audio-slideshow plugin does not reliably play the same file on multiple slides

### 7. Answer Slide (answer-list flex layout)

Replace the old `table.answer-table` with the answer-list flex layout. This is the **only** answer slide pattern.

```html
<section id="slide-ex{n}-answers-{range}" data-background-color="#0d5e1a">
    <h2>Exercise {{ number }} — Answers (1–3)</h2>
    <div class="answer-list">
        <div class="a-row">
            <span class="a-num">1.</span>
            <span class="a-q">{{ question_snippet }}</span>
            <span class="fragment fade-up a-ans a-cor" data-fragment-index="1"><i class="fa-solid fa-check" style="color:#fff;"></i> {{ answer }}</span>
            <span class="fragment fade-up" data-fragment-index="1" style="width:100%; color:#ffdd00; font-size:0.95em; text-align:left;">WHY: {{ explanation }}</span>
        </div>
        <div class="a-row">
            <span class="a-num">2.</span>
            <span class="a-q">{{ question_snippet }}</span>
            <span class="fragment fade-up a-ans a-inc" data-fragment-index="2"><i class="fa-solid fa-times" style="color:#fff;"></i> {{ answer }}</span>
            <span class="fragment fade-up" data-fragment-index="2" style="width:100%; color:#ffdd00; font-size:0.95em; text-align:left;">WHY: {{ explanation }}</span>
        </div>
    </div>
    <aside class="notes">{{ teacher_feedback_notes }}</aside>
</section>
```

Rules:
- Green background `#0d5e1a` for all answer slides
- **Max 3 items per slide** — split exercises with >3 items (e.g., `slide-ex2-answers-1-3`, `slide-ex2-answers-4-5`)
- `a-cor` for correct answers (green background on reveal), `a-inc` for incorrect answers (red background on reveal)
- **Do NOT use** `answer-correct`/`answer-incorrect`, `highlight-green`/`highlight-red`, or `table.answer-table` — these are legacy
- `fragment fade-up` for animated reveal (not bare `fragment`)
- Font Awesome `fa-check`/`fa-times` for icons — **never raw Unicode U+2713/U+2717**
- Each row has answer + WHY appearing together (matching `data-fragment-index`)
- WHY is **yellow** (`#ffdd00`), flush left (`text-align:left`), near-standard font size (`0.95em`)
- **WHY content**: listening comprehension = direct transcript quote; language exercises = grammatical rule
- All text must be solid `#fff` (white) or `#ffdd00` (yellow) — **no gray, no muted colors**
- `.aim-label` (if used) must be overridden to `#fff` via inline `<style>` block

### 8. Pedagogical Strategy Slide

Used for explicit strategy instruction before a task. Goes between the Transition and Task slides in the four-slide block.

```html
<section id="slide-strategy-{name}" class="pedagogical" data-background-color="#1a6b5a" data-background-transition="none">
    <h2>{{ strategy_heading }}</h2>
    <ul>
        <li>{{ step_1 }}</li>
        <li>{{ step_2 }}</li>
    </ul>
    <p style="color:#ffdd00;"><i class="fa-solid fa-flag-checkered" style="color:#ffdd00;"></i> Want a challenge? {{ challenge_text }}</p>
    <aside class="notes">{{ teacher_notes }}</aside>
</section>
```

**Auto-animate variant** (for keyword underline reveals):
```html
<!-- Entry: transparent keyword borders -->
<section data-auto-animate data-auto-animate-id="{name}" id="slide-strategy-{name}-entry" class="pedagogical" data-background-color="#1a6b5a" data-background-transition="none">
    <h2 data-id="title">{{ strategy_heading }}</h2>
    <p data-id="ex1" style="color:#ffdd00; font-size:0.85em;">
        Listen for <span data-id="w1" style="border-bottom: 2px solid transparent;">key terms</span> in the text.
    </p>
</section>
<!-- Reveal: keywords gain coloured borders via auto-animate -->
<section data-auto-animate data-auto-animate-id="{name}" id="slide-strategy-{name}-reveal" class="pedagogical" data-background-color="#1a6b5a" data-background-transition="none">
    <h2 data-id="title">{{ strategy_heading }}</h2>
    <p data-id="ex1" style="color:#ffdd00; font-size:0.85em;">
        Listen for <span data-id="w1" style="border-bottom: 2px solid #4fc3f7;">key terms</span> in the text.
    </p>
    <p style="margin-top:1em; color:#ffdd00;"><i class="fa-solid fa-flag-checkered" style="color:#ffdd00;"></i> Want a challenge? {{ challenge_text }}</p>
    <aside class="notes">{{ teacher_notes }}</aside>
</section>
```

**Structure talk variant** (for speaking tasks):
```html
<section id="slide-strategy-talk" class="pedagogical structure-talk" data-background-color="#1a6b5a" data-background-transition="none" style="top: 0;">
    <h2>Structure Your Talk</h2>
    <p class="structure-step"><u><strong>Thesis:</strong> Say your main idea</u></p>
    <p class="structure-step"><u><strong>Reasons:</strong> Give 1-2 reasons</u></p>
    <p class="structure-step"><u><strong>Example:</strong> Share an example</u></p>
    <p class="transition-words">First... &nbsp; Also... &nbsp; For example...</p>
    <p style="margin-top:1em; color:#ffdd00;"><i class="fa-solid fa-flag-checkered" style="color:#ffdd00;"></i> Want your group to go further? Add a conclusion.</p>
</section>
```

Rules:
- Teal background `#1a6b5a`, `class="pedagogical"`, `data-background-transition="none"`
- Challenge/differentiation text is **student-facing** ("Want a challenge?…", "Want to go further?…") — never teacher-facing
- Checkered flag icon marks challenge options
- Auto-animate requires both sections to have `data-auto-animate` with matching `data-auto-animate-id`
- Keyword spans need matching `data-id` on both entry and reveal slides
- Entry uses `transparent` border; reveal uses coloured border (blue `#4fc3f7`, orange `#ff8a65`)
- No audio on pedagogical slides — audio goes on the task slide

### 9. Section Transition Slide
```html
<section data-background-color="#c0392b">
    <h2>{{ next_stage_name }}</h2>
</section>
```

- Red background `#c0392b`
- **Heading only, no descriptive paragraphs.** The teacher's spoken introduction bridges the gap. Brief foreshadowing text (1 sentence max) is acceptable only when the transition type isn't obvious from context.
- Speaker notes: NOT required (teacher directs the transition verbally)
- No timer, no fragments

### 10. Post-Reading Discussion Slide
```html
<section>
    <h2>Let's Discuss</h2>
    <ol>
        <li>{{ question_1 }}</li>
        <li>{{ question_2 }}</li>
        <li>{{ question_3 }}</li>
    </ol>
    <aside class="notes">
        Students discuss in pairs. 5 min.
        Content and language feedback. 2 min.
    </aside>
</section>
```

All questions visible at once. No fragments for discussion.

### 11. Summary Slide
```html
<section>
    <h2>What you can do now</h2>
    <ul>
        <li>✓ {{ outcome_1 }}</li>
        <li>✓ {{ outcome_2 }}</li>
        <li>✓ {{ outcome_3 }}</li>
    </ul>
    <aside class="notes">
        Elicit from students: What did you learn today?
        Connect back to their predictions from the beginning.
    </aside>
</section>
```

### 12. End Slide (buffer)
```html
<section data-background-color="#2c3e50">
    <h2>Thank you</h2>
    <p><em>{{ topic }}</em> | {{ cefr_level }}</p>
</section>
```

### 13. YouTube Embed Slide
```html
<section data-background-color="#1a1a2e">
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

- Uses `src` directly (not `data-src`) — iframe loads immediately with the page
- `referrerpolicy="strict-origin-when-cross-origin"` — REQUIRED. YouTube now blocks embeds without a valid HTTP Referer (Error 153). This attribute tells the browser to send the referrer header.
- Also add `<meta name="referrer" content="strict-origin-when-cross-origin" />` inside `<head>` as a page-wide fallback
- `allowfullscreen` allows the user to enter fullscreen mode
- Reveal.js automatically detects YouTube URLs and sends `slide:start`/`slide:stop` postMessages
- Audio is paused when navigating away (reveal.js built-in behavior)

### 14. Diagnostic Talk Structure Slide (Pedagogical)
```html
<section class="pedagogical structure-talk" data-background-color="#1a6b5a" data-background-transition="none" style="top: 0;">
    <h2>Structure Your Talk</h2>
    <p class="structure-step"><u><strong>Thesis:</strong> Say your main idea</u></p>
    <p class="structure-step"><u><strong>Reasons:</strong> Give 1-2 reasons</u></p>
    <p class="structure-step"><u><strong>Example:</strong> Share an example you know</u></p>
    <p class="transition-words">First... &nbsp; Also... &nbsp; For example...</p>
</section>
```

- Teal background `#1a6b5a`, `class="pedagogical structure-talk"`
- Three structure steps (thesis → reasons → example) with underlined labels
- Transition words at bottom in yellow (`#ffdd00`) inside a semi-transparent box
- Teacher uses this to model diagnostic speaking task structure

---

### 15. Grammar Rule Explanation Slide (Pedagogical)
```html
<section class="pedagogical" data-background-color="#1a6b5a" data-background-transition="none">
    <h2>Subject-Verb Agreement: Rules 1–3</h2>
    <p><u><strong>Rule 1:</strong> Ignore prepositional phrases</u></p>
    <p><em>"The color of her eyes changes."</em> → Subject is <strong>color</strong>, not <em>eyes</em>.</p>
    <p><u><strong>Rule 2:</strong> There + be → subject follows</u></p>
    <p><em>"There are several kinds."</em> → <strong>kinds</strong> is the subject.</p>
    <p><u><strong>Rule 3:</strong> Each, one, neither, either → always singular</u></p>
    <p><em>"Each of the students has a book."</em></p>
</section>
```
- Teal background `#1a6b5a`, class `pedagogical`
- Group 2-3 related rules per slide
- Each rule: underlined label + example in quotation marks + brief explanation
- Key grammar words highlighted with `<span style="color:#ffdd00;">word</span>` inline

### 16. Diagnostic Test Slide
```html
<section data-background-color="#1a1a2e">
    <h2>Diagnostic Test</h2>
    <p><em>Each sentence has ONE error. Find and fix it.</em></p>
    <ol style="font-size: 0.8em; text-align: left;">
        <li>George Lucas have changed the film industry.</li>
        <li>There is two main characters in Star Wars.</li>
        <li>Each of the movies have a different director.</li>
    </ol>
    <aside class="notes">
        Stage 2 · 8 min · S
        Students work individually. Monitor and note difficulty areas. Do NOT give answers yet.
    </aside>
</section>
```
- Dark `#1a1a2e` background, pencil icon
- All test items visible on entry (no fragments)
- Speaker notes: monitoring instructions, do-not-reveal-yet reminder
- No timer (teacher controls pace)

### 17. Error-Correction Answer Table (Grammar)
```html
<section data-background-color="#0d5e1a">
    <h2>Practice 3A — Answers (1-3)</h2>
    <table class="answer-table" style="font-size:0.875em;">
        <thead><tr><th style="width:8%;">#</th><th style="width:42%;">Sentence</th><th style="width:15%;">Answer</th><th style="width:35%;">Why?</th></tr></thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>One of my classmates ___ from my country.</td>
                <td class="fragment answer-correct" data-fragment-index="1"><strong style="color:#ffdd00;">is</strong></td>
                <td class="fragment answer-correct" data-fragment-index="1" style="font-size:0.9em;">"One" is always singular</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Some of the teachers ___ my language.</td>
                <td class="fragment answer-correct" data-fragment-index="2"><strong style="color:#ffdd00;">speak</strong></td>
                <td class="fragment answer-correct" data-fragment-index="2" style="font-size:0.9em;">"teachers" is countable plural</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Each of the gifts ___ carefully wrapped.</td>
                <td class="fragment answer-correct" data-fragment-index="3"><strong style="color:#ffdd00;">was</strong></td>
                <td class="fragment answer-correct" data-fragment-index="3" style="font-size:0.9em;">"Each" is always singular</td>
            </tr>
        </tbody>
    </table>
</section>
```
- Green `#0d5e1a` background, `answer-table` class
- **Max 3 items per slide** with a Why column (4 columns: # / Sentence / Answer / Why?)
- Answer and Why cells use `class="fragment answer-correct"` with matching `data-fragment-index` for per-row reveal
- Table font: `0.875em` for readability; Why column: `0.9em`
- No instructional text like "Click to reveal" — answer reveal behavior is obvious
- When items have no Why explanation (e.g., fill-in-the-blank), a 3-column table (# / Sentence / Answer) is acceptable

### 18. Inline Annotated Grammar Answer (S/V/O) — Gold Standard

For grammar exercises where students identify subjects, verbs, and objects, **annotate the sentence inline** rather than using a separate answer column. This keeps the annotation visually connected to the words, avoiding split attention.

**How it works:**
- Each sentence enters as **plain unadorned text**
- On click, `fragment custom` CSS classes animate in: colored underlines, boxes, and superscript labels appear
- `data-fragment-index` groups one sentence's decorations to reveal together per click
- The confirmation note (`fragment fade-up`) slides in simultaneously

**CSS (add to inline `<style>` block before answer slides):**
```css
.reveal .fragment.custom.svo-s { border-bottom: 2px solid transparent; }
.reveal .fragment.custom.svo-s.visible { border-bottom: 2px solid #4fc3f7; }
.reveal .fragment.custom.svo-s sup { opacity: 0; transition: opacity 0.2s ease, color 0.2s ease; }
.reveal .fragment.custom.svo-s.visible sup { opacity: 1; color: #4fc3f7; }

.reveal .fragment.custom.svo-v { border-bottom: 2px solid transparent; }
.reveal .fragment.custom.svo-v.visible { border-bottom: 2px solid #ff8a65; box-shadow: 0 5px 0 0 #ff8a65; }
.reveal .fragment.custom.svo-v sup { opacity: 0; transition: opacity 0.2s ease, color 0.2s ease; }
.reveal .fragment.custom.svo-v.visible sup { opacity: 1; color: #ff8a65; }

.reveal .fragment.custom.svo-o { border: 1.5px solid transparent; padding: 0 3px; border-radius: 3px; }
.reveal .fragment.custom.svo-o.visible { border: 1.5px solid #aed581; }
.reveal .fragment.custom.svo-o sup { opacity: 0; transition: opacity 0.2s ease, color 0.2s ease; }
.reveal .fragment.custom.svo-o.visible sup { opacity: 1; color: #aed581; }
```

**HTML pattern (max 3 sentences per slide):**
```html
<section data-background-color="#0d5e1a">
    <h2>Practice 3 — Answers (1–3)</h2>
    <p class="aim-label">Subjects, Verbs, and Objects</p>
    <div style="font-size: 0.95em; line-height: 2.5; text-align: left; width: 100%;">
        <p><strong>1.</strong>
            <span class="fragment custom svo-s" data-fragment-index="1"><sup style="font-size:0.65em;">S </sup>My brother</span>
            <span class="fragment custom svo-v" data-fragment-index="1"><sup style="font-size:0.65em;">V </sup>is</span> in school.
            <span class="fragment fade-up" style="color:#fff;" data-fragment-index="1"><i class="fa-solid fa-check"></i> Linking verb — no object</span>
        </p>
        <p><strong>2.</strong>
            <span class="fragment custom svo-s" data-fragment-index="2"><sup style="font-size:0.65em;">S </sup>He</span>
            <span class="fragment custom svo-v" data-fragment-index="2"><sup style="font-size:0.65em;">V </sup>likes</span>
            <span class="fragment custom svo-o" data-fragment-index="2"><sup style="font-size:0.65em;">O </sup>his job</span>.
            <span class="fragment fade-up" style="color:#fff;" data-fragment-index="2"><i class="fa-solid fa-check"></i> Action verb — has object</span>
        </p>
        <p><strong>3.</strong>
            <span class="fragment custom svo-s" data-fragment-index="3"><sup style="font-size:0.65em;">S </sup>She</span>
            <span class="fragment custom svo-v" data-fragment-index="3"><sup style="font-size:0.65em;">V </sup>works</span> at a mall.
            <span class="fragment fade-up" style="color:#fff;" data-fragment-index="3"><i class="fa-solid fa-check"></i> Prepositional phrase — no object</span>
        </p>
    </div>
</section>
```

Rules:
- **Max 3 items per slide** — if the exercise has more items, split across multiple slides
- Each sentence's decorations share a single `data-fragment-index` so they reveal together
- Superscript labels use `opacity: 0` → `opacity: 1` via CSS transitions (NOT `color: transparent`, which causes anti-aliasing artifacts)
- Transparent borders + padding are applied from the start to prevent layout shift when the color appears
- Confirmation notes use `fragment fade-up` (not `fragment custom`) so they actually slide in from hidden
- Green `#0d5e1a` background with white (`#fff`) or yellow (`#ffdd00`) text only — no gray or muted colors

**Deprecated alternative — Multi-Column Grammar Table:**
```html
<section data-background-color="#0d5e1a">
    <h2>Practice 3 — Answers (1–5)</h2>
    <p class="aim-label">Subjects, Verbs, and Objects</p>
    <table class="answer-table">
        <thead><tr><th>#</th><th>Sentence</th><th>S</th><th>V</th><th>O</th></tr></thead>
        <tbody>
            <tr><td>1</td><td>My brother is in school.</td><td class="fragment answer-correct">My brother</td><td class="fragment answer-correct">is</td><td class="fragment">(none)</td></tr>
        </tbody>
    </table>
</section>
```
- Up to 6 columns for grammar annotation (S/V/O, tense, etc.)
- All answer cells use fragment reveal for clickthrough
- Use only when inline annotation is not feasible (e.g., very long sentences, or analysis that doesn't map to specific words)

### 19. Code/Text Passage with Line Highlights
```html
<section data-background-color="#1a1a2e">
    <h2>Find the Main Idea</h2>
    <pre style="font-size: 0.7em;"><code data-trim data-line-numbers="1-5|8-10|12-15">
        Line 1 of your text passage here.
        Line 2 of your text passage here.
        Line 3 of your text passage here.
        ...
    </code></pre>
    <p class="fragment" style="color:#ffdd00;"><strong>Main idea:</strong> The key point.</p>
    <aside class="notes">
        Step 1: Students read silently. Step 2: Elicit main idea.
        Step 3: Reveal supporting details via fragments.
    </aside>
</section>
```
- `data-line-numbers="1-5|8-10|12-15"` — pipe-separated steps, each step highlights different lines
- The highlight plugin is pre-loaded in the base template
- Use for: skimming/scanning lessons, reading comprehension, text analysis

### 20. Vertical Slides (Nested)
```html
<section>
    <section>
        <h2>Main Content</h2>
        <p>This is the primary slide.</p>
    </section>
    <section>
        <h2>Optional Extension</h2>
        <p>Accessed via down arrow. Skipped via right arrow.</p>
        <aside class="notes">Backup for fast finishers.</aside>
    </section>
</section>
```
- Nested `<section>` inside a horizontal slide
- Use for: backup content, optional drill-down, extension activities
- Navigation: down arrow enters the stack, right arrow skips past it

### 21. Text Shield for Image Backgrounds
```html
<section data-background-image="assets/photo.jpg" data-background-opacity="1.0">
    <h2 class="text-shield">Title with dark semi-transparent background</h2>
    <p class="text-shield">Readable body text on any image.</p>
    <p><span class="fragment text-shield-light">Light gray highlight on click.</span></p>
</section>
```
- `text-shield`: dark semi-transparent background for white text on full-opacity images
- `text-shield-light`: light gray semi-transparent background for dark text
- `fragment text-shield-light`: text visible at entry, light gray background highlight on click
- Both use `display: inline-block` + `max-width: 90%` — background stays tight to text, no full-width bars, no `::after` artifacts
- Both disable text-shadow (shield replaces it)
- See the skill for full rules

### 22. Text Highlighting with `data-mark` (Mark.js Plugin)
```html
<!-- Mark lines 1 and 3-5 on entry -->
<p data-mark="1,3-5">Highlighted text passage here.</p>

<!-- 3-step reveal: nothing, then "creative", then line 5 -->
<blockquote data-mark="|/creative/|5">Text passage here.</blockquote>
```
- Works on ANY element, not just `<pre><code>` — no monospace font hack
- Line numbers and regex patterns supported
- Steps separated by `|`
- The plugin and Mark.js are loaded in the base template — just add `data-mark`
- See the skill for full syntax rules

## Auto-Animate for Strategy Demonstrations

Use `data-auto-animate` on consecutive sibling `<section>` elements to build up strategies step by step. **Auto-animate is the primary reason markdown was abandoned** — consecutive `<section data-auto-animate>` elements must be direct siblings in `<div class="slides">`, not nested inside `<section data-markdown>`.

### Example: True/False Strategy (5 slides)
```html
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background-color="#1a6b5a">
    <h2>True/False Strategy</h2>
    <p><strong>Step 1:</strong> Read the statement carefully</p>
    <p><em>Statement text goes here.</em></p>
</section>
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background-color="#1a6b5a">
    <h2>True/False Strategy</h2>
    <p><strong>Step 1:</strong> Read the statement carefully</p>
    <p><em>Statement text goes here.</em></p>
    <p><strong>Step 2:</strong> Find the keywords</p>
    <p>"keyword1" · "keyword2" · "keyword3"</p>
</section>
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background-color="#1a6b5a">
    <h2>True/False Strategy</h2>
    <!-- ... all previous steps ... -->
    <p><strong>Step 3:</strong> Find the evidence</p>
    <p>Look in paragraphs X and Y. Do the meanings match?</p>
</section>
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background-color="#1a6b5a">
    <h2>True/False Strategy</h2>
    <!-- ... all previous steps ... -->
    <p><strong>Step 4:</strong> Check your answer</p>
</section>
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background-color="#1a6b5a">
    <h2>True/False Strategy</h2>
    <!-- ... all previous steps ... -->
    <p class="fragment highlight-green">TRUE — Explanation of why it's true.</p>
</section>
```

**Critical rules:**
- All sections in one block MUST be consecutive siblings — no other sections between them
- `data-auto-animate-id` MUST match across all sections in the block
- Each section builds on the previous by adding new elements while keeping shared elements
- `autoAnimateUnmatched: true` in `Reveal.initialize()` handles new/removed elements
- All sections share `class="pedagogical"` and `data-background-color="#1a6b5a"`

### Example: Multiple Choice Strategy (non-stacked, single slide with fragments)
```html
<section class="pedagogical" data-background-color="#1a6b5a">
    <h2>Multiple Choice Strategy</h2>
    <p><strong>Step 1: Read all options first</strong> <span class="fragment"> — look at all three choices</span></p>
    <ul class="fragment">
        <li>a) Option A text</li>
        <li>b) Option B text</li>
        <li>c) Option C text</li>
    </ul>
    <p class="fragment"><strong>Step 2: Eliminate wrong answers</strong></p>
    <p class="fragment strike">a) Reason for elimination. <strong>Eliminate.</strong></p>
    <p class="fragment strike">b) Reason for elimination. <strong>Eliminate.</strong></p>
    <p class="fragment"><strong>Step 3: Confirm the answer</strong></p>
    <p class="fragment highlight-green">c) Explanation. ✓ <strong>c is correct!</strong></p>
</section>
```

**Decision framework (from the skill):**
1. **Is the effect purely visual between slides?** (border appearing, colour change, word replacement) → **Auto-animate**
2. **Is the teacher revealing content step by step within a single slide?** → **Fragments**
3. **Is each step a discrete teaching moment that needs its own slide?** → **Sibling slides** (one per step, no auto-animate)
4. **Does the content need progressive highlighting within a text block?** → **Code + line numbers**
5. **Is the goal to enlarge or preview media?** → **Lightbox**
6. **Is the content optional / a backup?** → **Vertical slides**
7. **Does the slide need a dramatic entrance?** → **Per-slide transition**

See the skill's full reveal.js Feature Lookup Table for the complete list of available features mapped to pedagogical contexts.

---

## Max Text Limits

| Slide type | Max total words on screen |
|---|---|---|
| Title | 20 |
| Objective | 30 (3 × 10-word outcomes) |
| Vocabulary | 40 (4-5 words × ~8 words each) |
| Lead-in image | 10 (1 question) |
| Lead-in error analysis | 60 (6 sentences × 10 words) |
| Pre-reading prediction | 6 (2 prompts × 3 words) |
| Diagnostic test | 100 (8 items × 12 words) |
| Task instruction | 20 |
| Grammar rule explanation | 80 per slide (2-3 rules) |
| Answer explanation | 40 per question |
| Section transition | 5 (heading only) |
| Post-reading discussion | 20 (2-3 questions) |
| Summary | 15 (3 × 5-word outcomes) |
| End | 5 |

---

## Example: "What Connects Us" (B2, 46 min, 6 stages)

### Generated slides (~19 slides)

```
Slide 1:  Title — "What Connects Us" + B2 badge + hero background image
Slide 2:  Objective — 3 outcomes (all visible, no fragments)
Slide 3:  Vocabulary — 4 words with phonemic script + example sentences (all visible)
Slide 4:  Lead-in — background image + "What do you see? What do you wonder?"
Slide 5:  Pre-reading — article title + 2 prediction prompts
Slide 6:  TASK — Exercise 2: True/False (brief instruction)
Slide 7:  ANSWERS — Exercise 2 (statements 1-3, fragments reveal each answer)
Slide 8:  Transition — "Reading for detail" (red background, brief)
Slide 9:  TASK — Exercise 3: Paragraph matching (brief instruction)
Slide 10: ANSWERS — Exercise 3 (1-B, 2-C, 3-A, 4-E, 5-F, 6-D, fragments reveal)
Slide 11: Transition — "Drawing conclusions" (red background, brief)
Slide 12: TASK — Exercise 4: Best conclusion a/b/c (brief instruction)
Slide 13: ANSWERS — Exercise 4 (c is correct + explanation, fragment reveal)
Slide 14: Transition — "Let's discuss" (red background, brief)
Slide 15: Post-reading discussion — 3 questions (all visible)
Slide 16: Transition — "Wrapping up" (brief)
Slide 17: Summary — "What you can do now" (3 outcomes)
Slide 18: End — "Thank you"

Backup slides (uncounted, at end):
- 19: Extra vocabulary challenge
- 20: Extension discussion prompt
- 21: Blank buffer
```

**Fragment count**: Only on slides 7, 10, 13 (answer reveal slides) — that's 3 out of 18 slides using fragments. Expository content stays on screen.

---

## Vocabulary Selection Guidelines

Words must be selected based on:
1. **CEFR level** — challenging but learnable:
   - A1/A2: basic concrete nouns, high-frequency verbs
   - B1/B2: abstract nouns, phrasal verbs, collocations
   - C1/C2: idiomatic expressions, academic vocabulary
2. **Relevance** to the lesson topic and reading text
3. **Comprehension-enabling** — words needed to understand the core text
4. **Source**: lesson plan materials, answer key, stage procedure text

Phonemic script: Use IPA. Example sentences must imply meaning without defining.

---

## Pixabay Image Strategy

| Slide type | Pixabay query pattern | Position |
|---|---|---|
| Title | Topic-relevant hero | Background |
| Lead-in | Emotional/hook photo | Background |
| Pre-reading | Context photo | Background |
| Vocabulary (each word) | Word-meaning context image | Background |
| Post-reading discussion | Extension/theme photo | Background |
| Section transitions | No image — color background | n/a |
| Task/Answer | No image — clean text | n/a |

### Title Slide Background

The title slide uses a Pixabay background image at full opacity with text-shield for readability:

```html
<section data-background-image="assets/pixabay_XXXXXXX_1.jpg" data-background-opacity="1.0">
    <h1 class="text-shield">Topic Title <span class="cefr-badge B2">B2</span></h1>
    <p class="text-shield"><em>Strap subheader</em></p>
</section>
```

- Images are downloaded from Pixabay API, resized to max 1920px width, compressed as JPEG (quality=80)
- Optimized images are cached in `output/.image-cache/` by Pixabay image ID
- Target file size: ~150-300KB per image
- If Pixabay API is unavailable or returns no results, falls back to gradient background
- Requires `PIXABAY_API_KEY` environment variable

Attribution in speaker notes: `Image by {author} from Pixabay`

---

## Implementation

1. **Template**: Copy `templates/base-slides-template.html` → `output/{subfolder}/slides/index.html`
2. **Slides**: Add raw HTML `<section>` elements inside `<div class="slides">`
3. **Supporting files**: Copy `timer-plugin.js`, `timer-plugin.css`, `mark-plugin.js`, and logo to the slides directory
4. **Edit**: Edit `index.html` directly — no generation step needed
5. **Open**: Double-click `index.html` in any browser (no server needed)

### Timer Pill

Task instruction slides display a floating timer pill at the bottom center of the viewport.

- **Attribute**: `data-timer="seconds"` on the `<section>` element
- **Appearance**: Semi-transparent dark rounded pill with digital MM:SS readout
- **Controls**: ⏵ Start, ⏸ Pause, ↺ Reset
- **Behavior**: Counts down from prescribed time, chimes at 10s (yellow) and 0s (red)
- **No auto-start**: Teacher must click ⏵
- Requires timer-plugin.js and timer-plugin.css in the slides directory
- **Do NOT use on slides with audio/video**: Never add `data-timer` to a `<section>` that also has `data-audio-src`. The timer pill and audio player controls conflict. Use one or the other.

### Audio Slideshow

The base template includes the [audio-slideshow](https://github.com/rajgoel/reveal.js-plugins/tree/master/audio-slideshow) plugin (CDN-loaded) for playing audio tracks during presentations.

- **Attribute**: `data-audio-src="assets/filename.mp3"` on the `<section>` element
- **Audio files**: placed in `slides/assets/` (same directory as images)
- **Controls**: Appears at bottom of viewport (fully visible). Teacher clicks play/pause. Keyboard shortcut: `A` to toggle.
- **Configured via** `audio:` block in `Reveal.initialize()` — see `templates/base-slides-template.html` for current settings.
- **No auto-advance**: `advance: -1` — teacher controls pacing

### Example: "What Connects Us" (B2, 46 min, 6 stages)

Generated slides (~29 slides):

```
Slide 0:  Title — "What Connects Us" + B2 badge + Pixabay background + logo
Slide 1:  Objective — 3 outcomes (all visible, no fragments)
Slide 2:  Lead-in — Pixabay background + open question
Slide 3-6: Vocabulary — 4 words, one per slide, Pixabay backgrounds
Slide 7:  Transition — "What's the main idea?" (red #c0392b)
Slide 8:  Transition — "Finding details" (red #c0392b)
Slides 9-13: Auto-animate — True/False Strategy (5 slides, teal #1a6b5a)
Slide 14: Auto-animate — MC Strategy block (teal #1a6b5a)
Slide 15: Task — True/False + Paragraph Matching (timer)
Slide 16: Transition — "Making conclusions" (red)
Slide 17: Task — Multiple Choice (timer)
Slide 18: Transition — "Let's Discuss" (red)
Slide 19: Task — Discussion questions (timer)
Slide 20: Transition — "Let's Review" (red)
Slide 21: Task — Reflection activity (timer)
Slides 22-26: Answer slides — fragment reveals
Slide 27: Summary — "What you can do now"
Slide 28: End — "Thank you" (dark #2c3e50)
```