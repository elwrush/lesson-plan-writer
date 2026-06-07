## Design Blueprint — CA: Writing a Profile

### Stage-to-Slide Mapping
| Stage # | Stage Name | Slide Type(s) | Template Pattern | Slide IDs |
|---------|-----------|---------------|------------------|-----------|
| — | Splash screen | Custom splash (full-bleed image, no text) | AGENTS.md splash spec | slide-splash |
| — | Title | Title slide with CEFR badge | Type 1: reference-slideshow.html | slide-title |
| — | Objectives | Objective slide (3 "I can" bullets) | Type 2: reference-slideshow.html | slide-objective |
| — | Review transition | Transition (red) | Type 3: reference-slideshow.html | slide-transition-review |
| 1 | Review — Compound Sentences | Static task (all 7 sentences visible, open-class) | Type 11: reference-slideshow.html (no timer) | slide-review-1-4, slide-review-5-7 |
| — | Lead-in transition | Transition (red) | Type 3: reference-slideshow.html | slide-transition-nureyev |
| 2 | Lead-in — Nureyev Portrait | Lead-in with image background | Custom — image bg + discussion prompts + text-shield | slide-nureyev |
| 3 | Preparation — Mind Map + Adverbs | Task slide with timer | Type 11: reference-slideshow.html | slide-prep-task |
| — | PET transition | Transition (red) | Type 3: reference-slideshow.html | slide-transition-pet |
| 4 | PET Task Introduction | Pedagogical strategy slides (static, 3 slides) | Type 8: reference-slideshow.html | slide-pet-structure, slide-pet-linking, slide-pet-phrases |
| 5 | First Draft — Writing | Task slide with timer + checklist | Type 11: reference-slideshow.html | slide-write-draft |
| 6 | Wrap-up | Summary slide (static) | Type 13: reference-slideshow.html | slide-summary |
| — | End | End slide | Type 14: reference-slideshow.html | slide-end |

### Per-Slide Design
| Slide ID | Intent | Feature | Principle | Mechanism | Template Ref |
|----------|--------|---------|-----------|-----------|--------------|
| slide-splash | Student sees Nureyev portrait fill the screen with no text — visual priming for the topic | Static — full-bleed background image only | Signaling — the image primes the "describing people" theme before any words appear | No content on the slide — the image alone is the signal. Text-shield is NOT needed because there is no text. This forces students to form their own impressions before any labels are applied. | AGENTS.md splash spec |
| slide-title | Student sees lesson topic, CEFR level, and a call-to-action that hints at the lesson type | Static — justify-content: center, text-shield on all text | Signaling — topic + badge + strap line signal the morning's goal at a glance | Logo 120px, h2 2.2em, CEFR badge inline, strap line + CTA subtitle on crimson text-shield to visually separate it as a challenge statement. | Type 1: reference-slideshow.html |
| slide-objective | Student sees 3 measurable learning outcomes, all at once — nothing hidden | Static — all bullets visible on entry, no fragments | Pretraining — stating outcomes upfront lets students self-monitor throughout the lesson | Three numbered "I can" statements, yellow numbers, white text. No fragments — objectives are not a reveal game. | Type 2: reference-slideshow.html |
| slide-transition-review | Student sees a phase change signal (red background, heading only) | Static — red slide, heading only, no notes | Signaling — red background is a learned cue for "new phase starts now" | Heading alone — the teacher's spoken bridge provides the rationale. No text competes with what the teacher is saying. | Type 3: reference-slideshow.html |
| slide-review-1-4 | Student sees 4 sentences — some correct, some with errors — and must diagnose each aloud | Static — all items visible immediately for open-class discussion | Segmenting — 4 items on screen prevents cognitive overload; the teacher controls pacing by pointing to one at a time | Sentences are numbered 1-4 with clear left alignment. No fragments — teacher discusses each item live. Split across two slides (1-4 then 5-7) to prevent crowding. | Type 11 (task) variant |
| slide-review-5-7 | Student sees remaining 3 sentences for diagnosis | Static — same layout as slide-review-1-4 | Segmenting — second batch follows naturally; the slide transition signals "moving on" | Same as above but items 5-7. | Type 11 (task) variant |
| slide-transition-nureyev | Student sees a phase change from grammar review to descriptive discussion | Static — red slide, heading only | Signaling — red background is a learned cue for phase change | Heading only — teacher introduces the portrait. | Type 3: reference-slideshow.html |
| slide-nureyev | Student sees Nureyev portrait as full-screen background with four discussion categories overlaid on text-shields | Static — image background + text-shield on all text | Spatial Contiguity — the portrait and the discussion categories (appearance, personality, interests, clothes/family) are on the same slide, so students can look at the image and the prompt simultaneously | Four category labels overlaid on the portrait with text-shield — students see the person AND the question at the same time. If the categories were on a separate slide, students would have to hold the visual details in memory while reading the prompt. | Custom (lead-in with image) |
| slide-prep-task | Student sees clear instructions to complete Exercise 3 and Exercise 5 from their textbook | Static — task instruction + timer | Segmenting — the timer creates a shared pacing anchor; students know exactly how long they have | Timer set to 600s (10 min). Brief instruction only — students have the workbook open. Full procedure in speaker notes. | Type 11: reference-slideshow.html |
| slide-transition-pet | Student sees a phase change to exam preparation | Static — red slide, heading only | Signaling — the transition signals that the focus shifts from preparation to exam-format instruction | Heading only — teacher introduces the PET task. | Type 3: reference-slideshow.html |
| slide-pet-structure | Student sees the four-part PET article structure they must memorise and apply | Static — all four parts visible on entry | Pretraining — presenting the structure BEFORE writing reduces cognitive load during the draft | Four labelled steps (Title, Opening, Body, Closing) on a pedagogical teal background. Static — students need to copy this, not watch it animate. | Type 8: reference-slideshow.html |
| slide-pet-linking | Student sees linking phrases grouped by function — a reference they can use while writing | Static — all phrases visible for copying | Pretraining — providing the language inventory upfront means students can select from it during writing instead of generating from scratch | Phrases grouped by function (opening, adding, contrasting, reasons, opinions, closing) in clear columns or bullet groups. Static — this is a reference slide. | Type 8: reference-slideshow.html |
| slide-pet-phrases | Student sees descriptive language frames for describing people | Static — all frames visible for copying | Pretraining — providing sentence stems reduces the language barrier so students can focus on content | "He comes across as...", "You can tell that...", "What stands out most is..." — each a sentence starter. Static reference slide. | Type 8: reference-slideshow.html |
| slide-write-draft | Student sees the PET prompt, the writing requirements checklist, and a countdown timer | Static — all requirements visible + timer | Segmenting — the timer creates a shared deadline; the checklist gives students self-monitoring anchors | Timer at 720s (12 min). Checklist displayed: catchy title, engaging opening, 3 paragraphs, 3+ adverbs of degree, 1+ compound sentence, 2+ linking phrases. PET prompt shown above. | Type 11: reference-slideshow.html |
| slide-summary | Student sees three accomplished outcomes with checkmarks, matching the objective slide structure | Static — all outcomes visible on entry | Signaling — matching the objective slide structure reinforces that the lesson achieved what it set out to do | Three checkmark items mirroring the objectives but reworded in past tense / accomplished voice. No fragments. | Type 13: reference-slideshow.html |
| slide-end | Student sees the lesson topic one final time | Static — dark blue-gray background, topic + CEFR badge | Signaling — the final slide signals "lesson complete" with a minimalist design | Topic title + B1 badge. No notes. | Type 14: reference-slideshow.html |

### Auto-Animate Pairs
None. This lesson uses no auto-animate pairs — all slides are static. The review stage is open-class (teacher manages discussion live), the PET introduction is reference content (students copy), and the writing stage is independent work.

### Answer Slide Sizing
No answer slides in this lesson — the review is open-class (live teacher feedback), and the writing is a first draft (no answer key). There are no comprehension exercises with answer reveals.

### Fragment Verification
No fragments used in this lesson. All slides are static — objectives, transitions, summaries have no fragments by rule; the PET pedagogical slides are reference content for copying; the review is open-class discussion; the task slides show instructions only.

### Color & Font Audit
| Slide ID | Background | Correct for type? | Font-size check | Notes |
|----------|------------|------------------|-----------------|-------|
| slide-splash | #1a1a2e + image | ✓ splash | N/A (no text) | — |
| slide-title | #1a1a2e + image | ✓ title | h2=2.2em, strap line=1em, CTA=0.9em | Splash uses no title image — only Nureyev |
| slide-objective | #1a1a2e | ✓ objective | h2 default | 3 bullets, yellow numbers |
| slide-transition-* | #c0392b | ✓ transition | h2 default | — |
| slide-review-* | #1a1a2e | ✓ task | body ≥1em | 7 sentences in 2 slides |
| slide-nureyev | #1a1a2e + image | ✓ lead-in | labels ≥0.9em + text-shield | Image = nureyev.jpg |
| slide-prep-task | #1a1a2e | ✓ task | body ≥1em | Timer 600s |
| slide-pet-* | #1a237e (teal) | ✓ pedagogical | body ≥0.9em | Pedagogical class |
| slide-write-draft | #1a1a2e | ✓ task | body ≥0.9em | Timer 720s |
| slide-summary | #1a1a2e | ✓ summary | body ≥1em | Checkmarks |
| slide-end | #2c3e50 | ✓ end | h2 default | — |
