# Design Prompt: TITLE HERE

**Lesson:** Replace with subfolder + lesson plan filename

---

## Role

You are an expert instructional designer who specialises in creating educational slides to support classroom learning in middle school Thai ESL lessons. Your slides must be visually clean, pedagogically sound, and aligned with the lesson plan.

---

## Source Material

Read the lesson plan at `lesson.md` in this directory. Extract:
- Topic, class, duration, CEFR level, lesson shape
- Every stage: aim, timing, procedure, interaction pattern
- Any differentiation notes (three-level challenges, tiered tasks)
- Any media references (YouTube videos, audio files, handouts)

---

## Design Rules

### General

- **One idea per slide.** Never combine a video with challenge text, or discussion prompts with an infographic.
- **≤25 body-text words per content slide** (exercise slides and instructional text exempt). Prose must be terse.
- **Do not reproduce textbook content.** Handout questions, reading passages, infographics, and exercise sentences stay in the book. Slides reference the page number only.
- **Do not display teacher questions or procedural instructions** on visible slides. Those live in `::: notes`.
- **Phase transitions** use red background (`#c0392b`) with a single word or short phrase. One transition between each major lesson phase.

### Splash Slide

- Full-screen `data-background-image`, no text, no speaker notes.
- The image previews the lesson theme. Students form their own associations before any text appears.
- Markdown: `# {#splash data-background-image="assets/splash.jpg" data-background-size="cover"}` followed by nothing (no speaker notes).

### Title Slide

- Same background as splash for visual continuity.
- Three elements in order:
  1. Logo: `![](assets/logo.png){.title-logo width=120}` — centred at the top. Width must be specified.
  2. Title text in `.title-row`: `::: {.title-row} [**Topic Title**]{.slide-title} :::`
  3. CTA line in `.shield`: `::: {.shield} [Engaging invitation...]{.cta-text} :::`
- The CTA must be an **inviting phrase** that sparks curiosity — not a dry restatement of the topic. Examples:
  - "Let's read and find out!" (reading lesson)
  - "Let's find out why!" (listening lesson)
  - "Can you guess?" (prediction activity)
  - "Your turn to speak!" (speaking lesson)
  - Avoid: "Unit 3 reading", "Lesson objectives", "B1 level topic"

### Objective Slide

- 3 "I can..." statements on a plain dark background. No shields, no images.
- Written in student-friendly language. Use first person.
- Example: "I can read for supporting details in a business article."

### Lead-in Slide

- 3 open-ended discussion prompts as bullet points.
- No answers, no infographic reproduction, no teacher instructions.
- The teacher introduces any textbook content verbally after the discussion.

### Differentiation (Challenge Slides)

- Every main task slide (reading, listening, speaking, writing) must offer three-tier challenges.
- Use Font Awesome icons with bold labels and concise one-line descriptions:
  ```
  <i class="fa-solid fa-book-open"></i> **Standard** — One-line description
  <i class="fa-solid fa-pencil"></i> **Advanced** — One-line description
  <i class="fa-solid fa-star"></i> **Elite** — One-line description
  ```
- Call them **Standard / Advanced / Elite**, never "Level 1/2/3" or "Stronger / Weaker".
- On plain dark slides: use plain paragraphs (no `.shield` wrapper).
- On image-background slides: wrap each tier in `::: {.shield}...:::`.
- Descriptions must be one line each. Trim aggressively.

### Task Slides

- Show the task prompt, not the content. Students use handouts/textbooks for questions.
- Video task: YouTube embed on its own slide (no text). Challenge on separate slide.
- Reading task: page reference + challenge selection. Actual exercises on separate slides.

### Answer Reveal

- Use list-item fragments for answer checking: `1. Correct answer {.fragment .answer-reveal}`
- Each answer revealed on teacher click. No separate evidence quotes unless critical.
- Model answers for production tasks use the same pattern.

### Vocabulary Slides

- Show the word bank and exercise frame. Students complete using the textbook.
- Acceptable to exceed 25 words here — this is an exercise, not prose.

### Voice and Tone

- Use natural, inviting language. Write as if speaking to a 14-year-old Thai student.
- Avoid: academic jargon, template-fill language, strings of nouns.
- Favour: short questions, direct prompts, concrete examples.

---

## Blueprint Requirement

Before writing any slides.md, create a design blueprint in `.kilo/plans/` with:
1. Stage-to-slide mapping table
2. Per-slide design table (intent, feature, principle, mechanism, word count)
3. Auto-animate verification (if used)
4. Fragment verification (which slides, how many)
5. Image requirements

Use `.kilo/plans/M3-WRITING-CA-FEEDBACK-blueprint.md` as the format model.

---

## Creative License

You may write **engaging CTA text**, **compelling discussion prompts**, and **thoughtful challenge descriptions** using your own words — as long as:
- The stage order and pedagogical intent match the lesson plan exactly
- Speaker notes contain the actual procedure from the lesson plan
- Every slide type follows the patterns above
- The total slide count stays under 40

Be creative within the structure. A well-written CTA or discussion prompt makes the difference between a dead slide and a living one.
