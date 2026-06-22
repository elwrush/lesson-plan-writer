# Design Blueprint — M3 Lesson 1: Voice and Character — Introduction to Dramatic Reading

## Lesson Overview

**Class:** M3 (all M3 classes)  
**Topic:** Voice and Character — Introduction to Dramatic Reading  
**Duration:** 46 minutes  
**CEFR:** B2  
**Lesson shape:** E (Receptive Skills — Traditional)

---

## Stage-to-Slide Mapping

| Stage # | Slide Type(s) | Slide IDs | Template Pattern |
|---------|---------------|-----------|------------------|
| — | Splash | slide-splash | Splash — fullscreen image, no text |
| — | Title | slide-title | Title — logo + title-row + shield CTA over same image |
| — | Objectives | slide-objectives | Grid table — 3 numbered items |
| 1 | Lead-in: Feedback reveals | slide-feedback-problems, slide-feedback-link | Fragment reveal list → boxed keyword transition |
| 2 | Pre-watching: Frame the task | slide-pre-watch | Single slide: definition + focus question |
| 3 | While-watching: YouTube embeds + compare | slide-bb-table-read, slide-bb-filmed, slide-compare | Two YouTube embeds → comparison table with fragments |
| 4 | Post-watching: Principle elicitation | slide-principle, slide-apply | Two slides: key insight fragment reveal → personal connection |
| — | Transition | slide-transition-outsiders | Red background phase change |
| 5 | Pre-reading: Character introduction | slide-outsiders-scene, slide-characters | YouTube embed → character descriptors (fragment reveals) |
| 6 | Reading: Task + voice guide | slide-read-task, slide-voice-tips | Task slide + boxed keyword tips |
| 7 | Wrap-up | slide-wrap | Single question + preview text |
| — | End | slide-end | Closing slide |

**Total slides: 18** (under 40 cap)

---

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Content |
|----------|--------|---------|-----------|-----------|---------|
| **slide-splash** | Prime the mood: drama, intensity, performance | Full-screen background image (`data-background-size="cover"`), no text | **Visual anticipation** — a theater stage or spotlight image communicates "this is about performance" subliminally | Students see the image before anything is said. No text forces them to form their own connection. | 0 words |
| **slide-title** | Present topic + call to action over the Heisenberg image | Logo + `.title-row` + two `.shield` divs over splash image | **Metaphorical framing** — Heisenberg IS Walter White transformed. The image already shows what the slide says. | Logo (ACT.png, width=120), `.title-row` with `[**Voice and Character**]{.slide-title}`, `.shield` with rhetorical question, `.shield` with `[**Today you'll learn to find your voice.**]{.cta-text}` | ~15 words |

**Title slide exact text:**
```
::: {.title-row}
[**Voice and Character**]{.slide-title}
:::

::: {.shield}
What if your voice could change who you are?
:::

::: {.shield}
[**Today you'll learn to find your voice.**]{.cta-text}
:::
```
| **slide-objectives** | State 3 goals | Grid table — 3 numbered items | **Advance organiser** — students need a mental roadmap | Single-column grid table: `**1.**` + text per row. No header row. | ~20 words |
| **slide-feedback-problems** | Show common speaking problems surfaced from feedback | Fragment reveals — each problem appears on click | **Pattern recognition** — students see the themes emerge rather than being told | `[...]{.fragment .answer-reveal}` for each problem: flat voice, long pauses, nervous laugh, too quiet | ~12 words |
| **slide-feedback-link** | Connect speaking problems to acting solutions | Boxed keyword: `[voice is your instrument]{.box}` | **Reframing** — shifts student self-perception from "I'm bad at speaking" to "I need to learn my instrument" | Single bold statement with boxed key phrase. Fragment reveal of the call-to-action. | ~15 words |
| **slide-pre-watch** | Define a table read and set focused viewing task | 2 fragments: definition first, then the focus question | **Schema activation** — students need to know WHAT to watch for before the video plays | Fragment 1: "Actors sit around a table, script only, no costumes, no sets." Fragment 2: "ASK: How do these actors show emotion and character using ONLY their voice?" | ~25 words |
| **slide-bb-table-read** | Play the Breaking Bad table read clip | YouTube embed: `::: {.youtube MqfSr8Gu9zI} :::` | **Primary input — SHOWING** — students watch raw emotional performance through voice alone | `youtube-embed.lua` converts to iframe. Set to the Blood Money argument scene with Aaron Paul. Label: "Breaking Bad — Table Read" | ~5 words (label) |
| **slide-bb-filmed** | Play the same scene from the TV episode | YouTube embed: `::: {.youtube 3A-Ck_2Na6s} :::` | **Comparative input — SHOWING** — same dialogue, full performance, students compare | `youtube-embed.lua` converts to iframe. Label: "Breaking Bad — Filmed Scene" | ~5 words (label) |
| **slide-compare** | Structure the comparison discussion | 2-column pipe table: "Same" vs "Different", fragment reveals in "Different" column | **Guided noticing** — the table organizes student observations. The "Same" column confirms what they heard; "Different" column reveals what changed. | Pipe table with `reading-feedback.lua` for white row lines. Fragment cells in "Different" column. | ~25 words |
| **slide-principle** | Elicit and confirm the core principle | Fragment reveal: "He's not being Aaron Paul — he's being Jesse. The character frees him." | **Metacognitive insight** — the principle emerges after students have discussed, not before | Yellow boxed keyword `[getting into a role]{.box}` appears first. Then the explanation fragment. | ~20 words |
| **slide-apply** | Connect the principle to students' own speaking | Fragment reveal: "What if you weren't YOU?" | **Personalization** — students internalize the principle by applying it to themselves | `[What if you were someone else?]{.fragment .answer-reveal}` then `[The next time you speak in English — you're not Ed. You're the character.]{.fragment .answer-reveal}` | ~15 words |
| **slide-transition** | Signal phase shift: Breaking Bad → The Outsiders | Red background (`data-background-color="#c0392b"`) | **Phase change** — red resets attention. Students know the teaching phase is done and application starts. | "Now: The Outsiders" as the heading | ~4 words |
| **slide-outsiders-scene** | Play the drive-in scene (19:08–23:30) | YouTube embed: `::: {.youtube CvyYEWSK1-w} :::` | **Secondary input — SHOWING** — students observe all 6 characters speaking and interacting | `youtube-embed.lua` converts to iframe. Start at 19m08s. Label: "The Outsiders — Meet the Characters" | ~6 words (label + timestamp note) |
| **slide-characters** | List characters with voice descriptors | Fragment reveals — each character appears on click AFTER student discussion | **Confirmation, not instruction** — students describe each character's voice FIRST, then the slide reveals the summary | 6 characters as fragment reveals: `**Dally** — hard, aggressive, swaggering` then `**Cherry** — confident, sharp, warm` etc. | ~15 words (labels) + descriptors |
| **slide-read-task** | Instructions for the Chapter 2 group read-aloud | Task slide with character assignments | **Role clarity** — students know exactly who reads what | List of 6 characters with their reading scope in bold. Teacher notes in `::: notes`. | ~30 words |
| **slide-voice-tips** | Visual reminders of how to read in character | Boxed keywords for voice dimensions | **Performance support** — boxed terms reinforce what to focus on while reading | `[PACE]{.box}` `[VOLUME]{.box}` `[EMOTION]{.box}` `[PAUSES]{.box}` displayed as spaced items. Fragment reveals of tip text under each. | ~20 words |
| **slide-wrap** | Consolidate learning and preview Lesson 2 | Single question + preview | **Metacognitive closure** — "One word" reflection creates personal takeaways | Fragment 1: reflection question. Fragment 2: preview of next lesson. | ~15 words |
| **slide-end** | Close the lesson | Closing slide — nothing needed | **Signal of completion** | Simple heading "See you next time." Dark background. | ~4 words |

---

## YouTube Embeds

| Slide | Video ID | Start time | Label | Purpose |
|-------|----------|-----------|-------|---------|
| slide-bb-table-read | `MqfSr8Gu9zI` | 0:00 | Breaking Bad — Table Read | Table read: Aaron Paul's emotional performance, voice only |
| slide-bb-filmed | `3A-Ck_2Na6s` | 0:00 | Breaking Bad — Filmed Scene | Same scene, final TV episode cut |
| slide-outsiders-scene | `CvyYEWSK1-w` | 19:08 | The Outsiders — Meet the Characters | Drive-in scene: Dally, Cherry, Johnny, Ponyboy, Marcia, Two-Bit |

YouTube embed pattern:
```markdown
# Breaking Bad — Table Read {#slide-bb-table-read}

::: {.youtube MqfSr8Gu9zI}
:::
```

Note: YouTube embeds require the HTTP server to be running (`python -m http.server 8000`). Don't open `file:///`.

---

## Fragments Summary

| Slide | Fragment count | Content | When they appear |
|-------|---------------|---------|-----------------|
| slide-feedback-problems | 4 | flat voice, long pauses, nervous laugh, too quiet | On click, one per click |
| slide-feedback-link | 2 | boxed keyword, call-to-action | Keyword first, then CTA |
| slide-pre-watch | 2 | table read definition, focus question | Definition first, question second |
| slide-compare | 3 | Different column cells: body language, camera angles, physical performance | After pair discussion, reveal one per click |
| slide-principle | 2 | boxed `[getting into a role]{.box}`, explanation text | Keyword first, explanation second |
| slide-apply | 2 | "What if you were someone else?", follow-up statement | Question first, then affirmation |
| slide-characters | 6 | Character name + voice descriptor | After teacher elicitation of each character |
| slide-voice-tips | 4 | PACE, VOLUME, EMOTION, PAUSES — each with tip | On click |
| slide-wrap | 2 | Reflection question, preview | Question first, preview second |

---

## Auto-Animate Pairs

**None.** This lesson has no grammar/transformation content. The visual show-don't-tell is achieved entirely through YouTube embeds (showing professional actors working) and fragment reveals (showing patterns emerge through discussion).

---

## Boxed Keywords

| Slide | Keyword | Why boxed |
|-------|---------|-----------|
| slide-feedback-link | `[voice is your instrument]{.box}` | Core metaphor — students need to internalize this frame |
| slide-principle | `[getting into a role]{.box}` | Critical vocabulary for the speaking persona framework |
| slide-voice-tips | `[PACE]{.box}`, `[VOLUME]{.box}`, `[EMOTION]{.box}`, `[PAUSES]{.box}` | Visual reinforcers for voice dimensions students apply during the read-aloud |

---

## Differentiation

**Not applied in this lesson.** The main task (group read-aloud) is inherently scaffolded by role — each student reads for one character with a defined voice. The teacher calls in character-appropriate delivery. Standard/Advanced/Elite tiered challenges don't apply to a whole-class ensemble activity.

---

## Color & Background Audit

| Slide ID | Background | Correct? | Notes |
|----------|-----------|----------|-------|
| slide-splash | Image (`data-background-image`) | Yes | Pixabay theater/stage image (to be downloaded) |
| slide-title | Same image (`data-background-image`) | Yes | `.title-row` + `.shield` for readability |
| slide-objectives | Dark (`#1a1a2e` or default black) | Yes | Plain dark background, no image |
| slide-feedback-problems | Dark | Yes | No shields needed (plain dark bg) |
| slide-feedback-link | Dark | Yes | No shields needed |
| slide-pre-watch | Dark | Yes | No shields needed |
| slide-bb-table-read | Dark | Yes | YouTube embed on plain dark |
| slide-bb-filmed | Dark | Yes | YouTube embed on plain dark |
| slide-compare | Dark | Yes | Pipe table, no shields |
| slide-principle | Dark | Yes | No shields needed |
| slide-apply | Dark | Yes | No shields needed |
| slide-transition | Red `#c0392b` | Yes | Phase change |
| slide-outsiders-scene | Dark | Yes | YouTube embed on plain dark |
| slide-characters | Dark | Yes | Fragment reveals, no shields |
| slide-read-task | Dark | Yes | Task instructions, no shields |
| slide-voice-tips | Dark | Yes | Boxed keywords, no shields |
| slide-wrap | Dark | Yes | No shields needed |
| slide-end | Dark blue-gray `#1a237e` | Yes | Closing slide |

**Shield rule compliance:** Zero slides use `.shield` because no slides (except splash/title) have background images. ✓

---

## Splash Image

**Source:** `C:\PROJECTS\LESSON-PLAN-WRITER-3\inputs\M3-LESSON01-DRAMA\heisenberg.jpg`  
**Subject:** Walter White / Heisenberg — menacing, shadowed face  
**Size:** 1200×675 (near-native 1280×720; good quality with `cover`)  
**Purpose:** Splash + title slide background — instantly signals "this lesson is about Breaking Bad and transformative performance"  
**Destination:** Copy + compress to `output/M3-LESSON01-DRAMA/slides/assets/splash.jpg`

---

## Implementation Steps

1. Create `output/M3-LESSON01-DRAMA/slides/` directory
2. Create `assets/` subdirectory for logo + splash image
3. Copy `templates/ACT.png` to `assets/logo.png`
4. Copy `inputs/M3-LESSON01-DRAMA/heisenberg.jpg` → compress → save as `assets/splash.jpg`
5. Copy infrastructure: `slides-pandoc.css`, `slides-header.html`, all `.lua` filters
6. Write `slides.md` per this blueprint
7. Validate: `python scripts/validate_slides.py output/M3-LESSON01-DRAMA/slides/slides.md`
8. Build: `pandoc slides.md -t revealjs ...` (full build command)
9. Test: `python -m pytest tests/ -v --tb=short`
10. Serve: `python -m http.server 8000` from slides directory
11. Review in browser
