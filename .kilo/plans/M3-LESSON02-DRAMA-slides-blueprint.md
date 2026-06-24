# Slideshow Blueprint: Scene Creation -- The Outsiders from Another Perspective

**Lesson:** M3-LESSON02-DRAMA (46 min)  
**CEFR:** B2  
**Shape:** F (Productive Skills)  
**Approx slides:** 20

---

## Slide Map

| # | Slide ID | Feature | Content | Est. time |
|---|----------|---------|---------|-----------|
| 1 | `#slide-splash` | Splash (data-background-image) | Full-bleed vintage drive-in image, no text | 0 |
| 2 | `#slide-title` | Title row (logo + CEFR badge) + 2 shields | "Your voice. Another character. One scene." → "Write the scene you didn't know was missing." | 2 |
| 3 | `#slide-objectives` | Grid table | 3 objectives: recall → analyse → write | 1 |
| 4 | `#leadin-recall` | YouTube embed | Outsiders drive-in clip (19:08–23:30). Fragment reveals after clip: character names as descriptors | 4 |
| 5 | `#leadin-characters` | Fragment reveals | 6 character names with one-line voice descriptors (Dally, Cherry, Johnny, Ponyboy, Marcia, Two-Bit) | 1 |
| 6 | `#define-problem` | Plain dark, auto-animate pair | "Ponyboy tells Chapter 2" → "But what if Cherry told it?" Side-by-side: what each character would notice | 3 |
| 7 | `#model-demo` | Plain dark, fragment reveal | Demo script: 4 character names + voice notes. "What does each character want?" | 3 |
| 8 | `#transition-write` | Red transition | `data-background-color="#c0392b"` — "Your Turn to Write" | 0 |
| 9 | `#group-formation` | Plain dark | Handout distributed. Groups of 4. | 3 |
| 10 | `#task-write` | Task + timer `data-timer="1200"` | Three tiers differentiation (Standard / Advanced / Elite) | 20 |
| 11 | `#check-rehearse` | Task + timer `data-timer="300"` | Peer-review checklist + rehearse | 5 |
| 12 | `#wrap-up` | Plain dark | "Next lesson: table read then performance." One-word reflection. | 2 |

---

## Slide Patterns (exact Markdown)

### Slide 1 — Splash
```markdown
#  {#slide-splash data-background-image="assets/splash.jpg" data-background-size="cover"}
```

### Slide 2 — Title
```markdown
#  {#slide-title data-background-image="assets/splash.jpg" data-background-size="cover"}

![](assets/logo.png){.title-logo width=120}

::: {.shield}
Your voice. Another character. One scene.
:::

::: {.shield}
[**Write the scene you didn't know was missing.**]{.cta-text}
:::
```

### Slide 3 — Objectives
```markdown
# What You\'ll Do Today {#slide-objectives}

+------------------------------------------------------------------+
| **1.** Recall the characters from Chapter 2 and their voices.     |
+------------------------------------------------------------------+
| **2.** Analyse a model script for character voice.                |
+------------------------------------------------------------------+
| **3.** Write a scene from another character's perspective.        |
+------------------------------------------------------------------+
```

### Slide 4 — Lead-in with YouTube
```markdown
# Recall the Characters {#leadin-recall}

::: {.youtube}
CvyYEWSK1-w?start=1148
:::
```

### Slide 5 — Character Voice Descriptors
```markdown
# The Voices We Heard {#leadin-characters}

[Dally — loud, defensive, swaggering.]{.fragment .answer-reveal}

[Cherry — thoughtful, questioning, measured.]{.fragment .answer-reveal}

[Johnny — quiet, shaking, but finding courage.]{.fragment .answer-reveal}

[Ponyboy — observant, careful, watching.]{.fragment .answer-reveal}

[Marcia — playful, warm, loyal.]{.fragment .answer-reveal}

[Two-Bit — joking, easy-going, deflecting.]{.fragment .answer-reveal}
```

### Slide 6 — Define the Problem (auto-animate)
```markdown
# Ponyboy Tells the Story {#define-problem data-auto-animate}

| Ponyboy's version | What he notices | What he misses |
|:-----------------|:----------------|:---------------|
| Cherry at the drive-in | Her hair, her laugh | Why she was really there |
| Johnny nearly drowning | His fear | Cherry's guilt |
```

### Slide 7 — Model Demo
```markdown
# The Demo Script {#model-demo}

[**Cherry** — thoughtful, questioning, full sentences.]{.fragment .answer-reveal}

[**Marcia** — playful, warm, loyal.]{.fragment .answer-reveal}

[**Brenda** — sharp, defensive, protective.]{.fragment .answer-reveal}

[**Linda** — soft, curious, asks the real questions.]{.fragment .answer-reveal}
```

### Slide 8 — Red Transition
```markdown
# Your Scene. Your Voice. {#transition-write data-background-color="#c0392b"}
```

### Slide 9 — Group Formation
```markdown
# Form Your Groups {#group-formation}

Groups of 4.

Read your character cards.

Write one prediction: *"When this character tells the story, they will focus on ____."*
```

### Slide 10 — Write Task (differentiation + timer)
```markdown
# Write the Scene {#task-write data-timer="1200"}

<i class="fa-solid fa-book-open"></i> **Standard** — Full scaffold: word count, line count, character cards visible.

<i class="fa-solid fa-pencil"></i> **Advanced** — Partial scaffold: voice notes only.

<i class="fa-solid fa-star"></i> **Elite** — Minimal scaffold: write from character understanding only.
```

### Slide 11 — Check + Rehearse
```markdown
# Check + Rehearse {#check-rehearse data-timer="300"}

[Swap scripts with another group.]{.fragment .answer-reveal}

[Read for one assigned character: "Does this sound like them?"]{.fragment .answer-reveal}

[Circle any lines that feel out of character.]{.fragment .answer-reveal}

[Rehearse: read through once silently, once aloud.]{.fragment .answer-reveal}
```

### Slide 12 — Wrap-up
```markdown
# Preview {#wrap-up}

Next lesson: table read then performance.

One word — what did you discover about your character today?
```

---

## Image

- `assets/splash.jpg` — vintage drive-in / 1950s car scene (Pixabay)

## Infrastructure

- Copy from `scripts/`: slides-pandoc.css, slides-header.html
- Copy from `.kilo/skills/create-beautiful-slideshows/scripts/`: youtube-embed.lua, audio-autoplay.lua, slide-helper.lua, shield-block.lua, box-keywords.lua, reading-feedback.lua, autocue.lua
- Copy logo from `.kilo/skills/create-beautiful-slideshows/templates/ACT.png`

## Filters used

- `youtube-embed.lua` — clip embed
- `audio-autoplay.lua` — (not needed in this lesson)
- `shield-block.lua` — title slide shields
- `reading-feedback.lua` — table row styling
- `box-keywords.lua` — (not needed in this lesson)
- `autocue.lua` — (not needed in this lesson)
