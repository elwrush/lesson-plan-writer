# Authorial Voice & Audience — Slides

## Prime Directive: Show, Don't Tell

**Every slide must pass this test: if a student had to read more than one short sentence (≤15 words) to understand what's happening, the slide is wrong.** We teach by *showing*, not by making learners read.

- One visual transformation per slide (before→after arrow, underline change, icon filling in)
- No bullet lists of instructions — the teacher speaks them
- No text explanations on screen — put them in `<aside class="notes">`
- A crossed-out sentence + arrow to short notes teaches more than labelled boxes

## Audience Constraints

Target: **Mathayom Thai students (CEFR B1)**. B2+ lessons may relax some rules.

### Vocabulary Ceiling (B1 default)
No words above B1 on screen without inline definition. **Banned**: identify, predict, convincing, distinguish, evaluate, analyze, infer. **Use**: find, guess, makes sense, tell the difference, decide, look at.

### Sentence Complexity
- Max 15 words per sentence on screen
- No semicolons — break into two sentences
- One clause preferred, two max
- No passive voice on screen

### Per-Slide Language Guidelines

| Slide type | B1 rule | Bad | Good |
|---|---|---|---|
| Objective | "what you CAN do" | "identify the main idea" | "find the main idea" |
| Task instruction | Direct imperatives only | "Students read and complete" | "Read the article. Do Exercise 2." |
| Transition | Simple warm-up Q | "What do you predict?" | "What do you think?" |

## Authorial Voice

When writing pedagogical annotations, adopt the voice of an **experienced EFL teacher with training in instructional design**. The four mandatory annotation lines must use teaching language:

- **PEDAGOGICAL INTENT**: "Student sees the error sentence transform into the corrected version" — NOT "The auto-animate morphs the element"
- **WHY THIS FEATURE**: "Auto-animate keeps both versions visible so students can compare before and after" — NOT "Auto-animate uses CSS transitions between matched data-id elements"
- **COGNITIVE PRINCIPLE**: Name from Mayer's 12 (Signaling, Segmenting, Spatial Contiguity, Coherence, etc.)
- **DESIGN MECHANISM**: Name a specific concrete choice and what happens if you remove it — "The period is wrapped in a transparent-border span that reserves layout space. Without the reserved width, the morph would cause line jump and students would lose the comparison."
