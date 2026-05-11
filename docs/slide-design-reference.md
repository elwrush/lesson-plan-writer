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

1. **Expository content on screen at once** — task instructions, vocabulary, objectives, discussion questions: ALL visible when the slide appears. Do not use fragments for expository material.
2. **Procedure text NEVER on screen** — teacher instructions, timing, interaction patterns go in `<aside class="notes">`
3. **Fragments reserved for answer reveal** — the teacher reveals answers one at a time after students have worked. This is the primary use of fragments.
4. **Auto-animate for strategy demonstrations** — use for showing step-by-step strategies (True/False, Multiple Choice) across consecutive slides. Not for general slide transitions.
5. **Pedagogical slides** — strategy/teaching content uses teal background (`data-background="#1a6b5a"`, `class="pedagogical"`) with white text
6. **Visual-first** — every lead-in and pre-reading slide uses a Pixabay background image
7. **Prediction before task** — students guess before doing, confirm with answer reveal
8. **Answer slides = answer + why + source** (all 3 parts)
9. **Vocabulary pre-teach** — slides AFTER lead-in stage, one word per slide on Pixabay background
10. **Section transitions** between stages — brief, one discussion question, red background (`#c0392b`)
11. **Text highlighting** — all slides use text-shadow for readability; pedagogical slides use white-on-teal; vocabulary words use yellow boldface (`#ffdd00`)

---

## B1 Audience Constraints

This section applies when generating slides for **Mathayom 2-3 Thai students (CEFR B1)**. These constraints ensure student-facing text is immediately comprehensible.

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
- **Pedagogical slides**: `class="pedagogical"` + `data-background="#1a6b5a"` — white text with teal background, white border-bottom on h2
- **Vocabulary words**: `<span class="vocab-word">word</span>` — yellow (`#ffdd00`) bold with text shadow
- **Transitions**: `data-background="#c0392b"` — red background
- **End slide**: `data-background="#2c3e50"` — dark background

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

---

## HTML Section Rules

These are the ONLY allowed patterns. Agents must not invent alternatives. All slides are raw HTML `<section>` elements.

### Slide elements
```html
<section>                    ← standalone slide
<section data-background="#c0392b">   ← slide with attributes
<section data-auto-animate data-auto-animate-id="same-id">  ← auto-animate pair
<section data-background-image="assets/image.jpg" data-background-opacity="0.7">  ← image background
<section data-timer="300">   ← timer pill (seconds)
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

CEFR badge colors: A1=green, A2=light green, B1=blue, B2=dark blue, C1=purple, C2=red

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
<section class="vocab-slide" data-background-image="assets/vocab-XXXXXX.jpg" data-background-opacity="0.7">
    <h2>Important Words</h2>
    <p><span class="vocab-word">{{ word }}</span></p>
    <p><em>{{ phonemic }}</em></p>
    <p><em>There's such a <span class="vocab-word">{{ word }}</span> between them; they never agree on anything.</em></p>
</section>

<!-- Subsequent words (no header) -->
<section class="vocab-slide" data-background-image="assets/vocab-XXXXXX.jpg" data-background-opacity="0.7">
    <p><span class="vocab-word">{{ word }}</span></p>
    <p><em>{{ phonemic }}</em></p>
    <p><em>There's such a <span class="vocab-word">{{ word }}</span> between them; they never agree on anything.</em></p>
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
<section data-background-image="assets/pixabay_XXXXXXX_1.jpg" data-background-opacity="0.7">
    <h2>Let's get Started</h2>
    <h3>{{ open_question }}</h3>
    <aside class="notes">
        {{ teacher_activation_script }}
        Display image for 20 seconds silently.
        Then ask the question. Elicit 3-4 responses.
        Connect responses to today's topic.
    </aside>
</section>
```

One open question only. Image as background. Speaker notes: activation script.

### 5. Pre-Reading Prediction
```html
<section data-background-image="assets/pixabay_XXXXXXX_1.jpg" data-background-opacity="0.7">
    <h2>Before you read: {{ article_title }}</h2>
    <ul>
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
<section data-timer="{{ seconds }}">
    <h2>{{ stage_name }}</h2>
    <ul>
        <li>{{ brief_task_instruction_1 }}</li>
        <li>{{ brief_task_instruction_2 }}</li>
    </ul>
    <aside class="notes">
        Stage {{ number }} · {{ time }} min · {{ interaction }}
        Goal: {{ stage_aim }}
        Materials: {{ material_reference }}
    </aside>
</section>
```

Brief task: 1-3 short bullet points. Full procedure in speaker notes. Material reference in italic gray.

### 7. Answer Slide — True/False
```html
<section>
    <h2>Exercise {{ number }}</h2>
    <p class="aim-label">True/False</p>
    <p class="fragment">{{ statement_text }}</p>
    <p class="fragment highlight-green">✓ <strong>{{ correct_answer }}</strong></p>
    <p class="fragment">{{ another_statement }}</p>
    <p class="fragment highlight-red">✗ <strong>False</strong></p>
    <p class="fragment highlight-green">✓ <em>{{ corrected_statement }}</em></p>
</section>
```

Rules:
- Each answer revealed via fragment (teacher controls when answer appears)
- Correct answer: bold + `highlight-green`
- Explanation: 1 sentence
- Source: paragraph reference in speaker notes

### 8. Answer Slide — Multiple Choice
```html
<section>
    <h2>Exercise {{ number }}</h2>
    <p class="aim-label">Multiple Choice</p>
    <p>a. {{ option_a }}</p>
    <p>b. {{ option_b }}</p>
    <p>c. {{ option_c }}</p>
    <p class="fragment highlight-green">✓ <strong>{{ correct_letter }}</strong></p>
</section>
```

### 9. Section Transition Slide
```html
<section data-background="#c0392b">
    <h2>{{ next_stage_name }}</h2>
    <p>{{ discussion_question }}</p>
    <aside class="notes">
        Transition: "Now we're moving from {{ prev_stage }} to {{ next_stage }}."
        Ask the discussion question. 1-2 min.
    </aside>
</section>
```

Red/orange background. One discussion question to warm up for the next stage.

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
<section data-background="#2c3e50">
    <h2>Thank you</h2>
    <p><em>{{ topic }}</em> | {{ cefr_level }}</p>
</section>
```

---

## Auto-Animate for Strategy Demonstrations

Use `data-auto-animate` on consecutive sibling `<section>` elements to build up strategies step by step. **Auto-animate is the primary reason markdown was abandoned** — consecutive `<section data-auto-animate>` elements must be direct siblings in `<div class="slides">`, not nested inside `<section data-markdown>`.

### Example: True/False Strategy (5 slides)
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
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
    <h2>True/False Strategy</h2>
    <!-- ... all previous steps ... -->
    <p><strong>Step 3:</strong> Find the evidence</p>
    <p>Look in paragraphs X and Y. Do the meanings match?</p>
</section>
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
    <h2>True/False Strategy</h2>
    <!-- ... all previous steps ... -->
    <p><strong>Step 4:</strong> Check your answer</p>
</section>
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
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
- All sections share `class="pedagogical"` and `data-background="#1a6b5a"`

### Example: Multiple Choice Strategy (non-stacked, single slide with fragments)
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
    <p class="fragment strike">a) Reason for elimination. <strong>Eliminate.</strong></p>
    <p class="fragment strike">b) Reason for elimination. <strong>Eliminate.</strong></p>
    <p class="fragment"><strong>Step 3: Confirm the answer</strong></p>
    <p class="fragment highlight-green">c) Explanation. ✓ <strong>c is correct!</strong></p>
</section>
```

**When to use auto-animate (stacked slides):**
- True/False strategy — building up 4-5 steps incrementally
- Paragraph matching strategy — showing each paragraph match one at a time
- Step-by-step grammar analysis

**When to use fragments (single slide):**
- Multiple choice strategy — eliminate wrong answers in sequence
- Answer reveal — one slide per exercise with fragment-per-answer

**When NOT to use auto-animate:**
- General slide transitions (use regular slide changes)
- Vocabulary lists (all visible at once)
- Answer reveals (use fragments)
- Expository content (all visible at once)

---

## Max Text Limits

| Slide type | Max total words on screen |
|---|---|
| Title | 20 |
| Objective | 30 (3 × 10-word outcomes) |
| Vocabulary | 40 (4-5 words × ~8 words each) |
| Lead-in image | 10 (1 question) |
| Pre-reading prediction | 6 (2 prompts × 3 words) |
| Task instruction | 20 |
| Answer explanation | 40 per question |
| Section transition | 10 (1 question) |
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

The title slide uses a Pixabay background image with a dark overlay for readability:

```html
<section data-background-image="assets/pixabay_XXXXXXX_1.jpg" data-background-opacity="0.7">
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
3. **Images**: Copy logo to `slides/assets/logo.png`, download Pixabay backgrounds to `slides/assets/`
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