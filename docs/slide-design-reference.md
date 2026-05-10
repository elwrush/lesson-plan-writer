# Slide Design Reference — ESL Lesson Presentations

This document defines how lesson plan JSON stages map to reveal.js slides. It is read by `scripts/json_to_markdown.py` at generation time. The teacher updates this file to change slide design without touching code.

---

## Context

- **Teacher controls all slides** — students never interact directly
- **Slides support the teacher's narration, not replace it**
- **Reveal.js 5.x** via CDN (inline markdown), white theme, 1280×720
- **CEFR levels**: A1, A2, B1, B2, C1, C2

---

## Core Principles

1. **Expository content on screen at once** — task instructions, vocabulary, objectives, discussion questions: ALL visible when the slide appears. Do not use fragments for expository material.
2. **Procedure text NEVER on screen** — teacher instructions, timing, interaction patterns go in speaker notes (`Notes:`)
3. **Fragments reserved for answer reveal** — the teacher reveals answers one at a time after students have worked. This is the primary use of fragments.
4. **Auto-animate for language demonstrations** — use for showing how parts of speech work, word transformations (active/passive, tense changes), or sentence structure. Not for general slides.
5. **Visual-first** — every lead-in and pre-reading slide uses a Pixabay background image
6. **Prediction before task** — students guess before doing, confirm with answer reveal
7. **Answer slides = answer + why + source** (all 3 parts)
7. **Vocabulary pre-teach** — slides AFTER lead-in stage, one word per slide on Pixabay background
9. **Section transitions** between stages — brief, one discussion question, colored background
10. **Text highlighting** — all slide text uses white text on a semi-transparent dark gray background with dark text outline

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

All slide text (h2, h3, p, li) uses a consistent highlight style:

- **Background**: dark gray at 50% opacity (`rgba(0,0,0,0.5)`)
- **Text**: white (`#ffffff`)
- **Text outline**: subtle dark outline using 4-direction text-shadow (`rgba(0,0,0,0.3)`)
- **Header display**: block (renders on own line)
- **Inline text display**: inline-block (p and li render inline)
- **Vocabulary words in context**: yellow boldface (`#ffdd00`) for emphasis
- **Header border-bottom**: maroon (`#800020`)

This applies to ALL slides regardless of background type.

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

## Markdown Syntax Rules

These are the ONLY allowed patterns. Agents must not invent alternatives.

### Slide separators
```
---           <- horizontal slide (blank line before AND after)
```

### Fragments (on same line as element)
```
✓ **Correct** <!-- .element: class="fragment highlight-green" -->
✗ **Wrong** <!-- .element: class="fragment highlight-red" -->
- **word** <!-- .element: class="fragment grow" -->
```

### Slide attributes (at top of content)
```
<!-- .slide: data-background="#e74c3c" -->
<!-- .slide: data-background-gradient="linear-gradient(to bottom, #2c3e50, #3498db)" -->
<!-- .slide: data-background-image="/images/photo.jpg" -->
```

### Speaker notes
```
Notes:
Full teacher script goes here.
```

---

## Slide Type Templates

### 1. Title Slide
```markdown
<!-- .slide: data-background-image="{pixabay_hero_image}" -->
# {{ topic }} <span class="cefr-badge {{ cefr_level }}">{{ cefr_level }}</span>

**{{ date }}** | {{ duration }}

Teacher: {{ teacher }}

*{{ materials }}*
```

CEFR badge colors: A1=green, A2=light green, B1=blue, B2=dark blue, C1=purple, C2=red

### 2. Objective Slide (all visible at once)
```markdown
## What you will be able to do by the end

- {{ outcome_1 }}
- {{ outcome_2 }}
- {{ outcome_3 }}
```

3 outcomes max, each ≤10 words. NO fragments — students need to see this as orientation.

### 3. Vocabulary Slides (one word per slide with Pixabay background)
**Generated after lead-in stage**

The script automatically converts formal stage names to friendly student-facing language:
- "Lead-in" → "Let's get Started"
- "Post-reading speaking task" → "Let's Discuss"
- "Wrap-up and reflection" → "Let's Review"
```markdown
<!-- .slide: data-background-image="{pixabay_word_image}" data-background-opacity="0.7" -->

## Important Words

**{{ word }}**
_{{ phonemic }}_

*There's such a {{ word }} between them; they never agree on anything.*

---

<!-- subsequent vocab slides omit the header -->
**{{ word }}**
_{{ phonemic }}_

*There's such a {{ word }} between them; they never agree on anything.*

Notes:
Drill: teacher says → class repeats (×3).
Show image as visual anchor for meaning.
```

Rules:
- **One vocabulary item per slide** — max 5 words total
- Word + phonemic script (IPA) + bolded target word in context sentence
- **Sentence must imply meaning, NOT define** — e.g., "There's such a **generation gap** between Rico and Ploy; Ploy doesn't understand the slang words Rico uses." (GOOD) vs "generation gap — the difference between two groups or generations" (BAD)
- **Pixabay background at 70% opacity** — image must precisely convey word meaning and context
- Title: "Important Words"
- All visible at once — NO fragments

### 4. Lead-In Image Slide
```markdown
<!-- .slide: data-background-image="{pixabay_photo}" -->

## {{ open_question }}

Notes:
{{ teacher_activation_script }}
Display image for 20 seconds silently.
Then ask the question. Elicit 3-4 responses.
Connect responses to today's topic.
```

One open question only. Image as background. Speaker notes: activation script.

### 5. Pre-Reading Prediction
```markdown
<!-- .slide: data-background-image="{pixabay_context_photo}" -->

## Before you read: {{ article_title }}

- What problem does the writer describe?
- What solution do they suggest?

Notes:
Students read the title and look at the photo.
Give them 30 seconds to share predictions in pairs.
Write 2-3 predictions on the board.
```

### 6. Task Instruction Slide
```markdown
## Exercise {{ number }}

{{ brief_task_instruction }}

*{{ material_reference }}*
<!-- .element: class="material-ref" -->

Notes:
{{ full_procedure_with_timing }}
Students work individually for {{ time }} min.
Do NOT reveal answer yet.
```

Brief task: 1-3 short bullet points. Full procedure in speaker notes. Material reference in italic gray.

### 7. Answer Explanation Slide
```markdown
## Exercise {{ number }} — Answers

**{{ question_1 }}**

✓ **{{ correct_answer }}** <!-- .element: class="fragment highlight-green" -->
*{{ explanation }}* — {{ source }}

---

**{{ question_2 }}**

✓ **{{ correct_answer }}** <!-- .element: class="fragment highlight-green" -->
*{{ explanation }}* — {{ source }}
```

Rules:
- Each answer revealed via fragment (teacher controls when answer appears)
- Correct answer: bold + highlight-green
- Explanation: 1 sentence
- Source: "Paragraph C, lines 3-5" or "See instructions"
- Multiple answers separated by `---`

### 8. Answer Slide — Multiple Choice Variant
```markdown
## Exercise {{ number }} — Answer

a. {{ option_a }}
b. {{ option_b }}
c. {{ option_c }}

✓ **{{ correct_letter }}** — {{ explanation }} <!-- .element: class="fragment highlight-green" -->

{{ source }}
<!-- .element: class="source-cite" -->
```

### 9. Section Transition Slide
```markdown
<!-- .slide: data-background="#c0392b" -->

## {{ next_stage_name }}

{{ discussion_question }}

Notes:
Transition: "Now we're moving from {{ prev_stage }} to {{ next_stage }}."
Ask the discussion question. 1-2 min.
```

Red/orange background. One discussion question to warm up for the next stage.

### 10. Post-Reading Discussion Slide
```markdown
<!-- .slide: data-background-image="{pixabay_extension_photo}" -->

## Discussion

- {{ question_1 }}
- {{ question_2 }}
- {{ question_3 }}

*{{ material_reference }}*
<!-- .element: class="material-ref" -->

Notes:
Students discuss in pairs. 5 min.
Content and language feedback. 2 min.
```

All questions visible at once. No fragments for discussion.

### 11. Summary Slide
```markdown
## What you can do now

✓ {{ outcome_1 }}
✓ {{ outcome_2 }}
✓ {{ outcome_3 }}

Notes:
Elicit from students: What did you learn today?
Connect back to their predictions from the beginning.
```

### 12. End Slide (buffer)
```markdown
<!-- .slide: data-background="#2c3e50" -->

## Thank you

*{{ topic }}* | {{ cefr_level }}
```

---

## Auto-Animate for Language Demonstrations

Use auto-animate (`data-auto-animate`) on adjacent slides to demonstrate language transformations. Only use for grammar/language points, not for general slides.

### Example: Active → Passive transformation
```markdown
<!-- .slide: data-auto-animate -->
## Active → Passive

**The dog chased the cat.**
<!-- .element: class="fragment highlight-blue" data-fragment-index="1" -->

---

<!-- .slide: data-auto-animate -->
## Active → Passive

**The cat was chased by the dog.**
<!-- .element: class="fragment highlight-blue" -->
```

### Example: Vocabulary word in context
```markdown
<!-- .slide: data-auto-animate -->
## empathy /ˈempəθi/

---

<!-- .slide: data-auto-animate -->
## empathy /ˈempəθi/

"She felt real empathy when she heard his story."
```

**When to use auto-animate:**
- Tense changes (present → past → present perfect)
- Active → passive transformations
- Word families (empathy → empathetic → empathize)
- Collocation examples (strong coffee, NOT powerful coffee)
- Showing a word isolated → in a sentence
- Sentence structure comparison

**When NOT to use auto-animate:**
- Answer reveals (use fragments instead)
- General slide transitions (use regular slide changes)
- Vocabulary lists (all visible at once)

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

```markdown
<!-- .slide: data-background-image="path/to/image.jpg" data-background-color="rgba(0,0,0,0.8)" -->
```

- Images are downloaded from Pixabay API, resized to max 1920px width, compressed as JPEG (quality=85)
- Optimized images are cached in `output/.image-cache/` by Pixabay image ID
- Target file size: ~150-300KB per image
- If Pixabay API is unavailable or returns no results, falls back to gradient background
- Requires `PIXABAY_API_KEY` environment variable

Attribution in speaker notes: `Image by {author} from Pixabay`

---

## Implementation

1. `scripts/json_to_markdown.py` reads this document at generation time
2. The script generates markdown following these templates
3. Build: `python scripts/json_to_markdown.py output/{subfolder}/{file}.json` — generates both `slides.md` and `index.html`
4. Open: double-click `output/{subfolder}/slides/index.html` in any browser (no server needed)