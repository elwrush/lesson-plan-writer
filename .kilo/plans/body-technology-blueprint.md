# Design Blueprint — Body Technology Reading Lesson

## Lesson Overview

**Class:** M2-4A
**Topic:** Body Technology — Reading about bionic and body-enhancing technology
**Duration:** 46 minutes
**CEFR:** B1 (mixed)
**Lesson shape:** ESA — Engage-Study-Activate

---

## Stage-to-Slide Mapping

| Stage # | Stage Name | Slide Type(s) | Slide IDs |
|---------|-----------|---------------|-----------|
| — | Splash | Full-screen pacemaker heart image, no text | slide-splash |
| — | Title | Logo + title + CTA shields | slide-title |
| — | Objectives | 3 "I can..." objectives table | slide-objectives |
| 1 | Lead-in | Pacemaker image bg, discussion prompts in shields | slide-lead-in |
| — | Transition (Reading) | Red background | slide-transition-reading |
| 2 | Autocue + Gist | 6 auto-advance slides (2.5s each) → gist question with fragment reveal | slide-autoslide-1 through slide-autoslide-6, slide-gist |
| 3 | Pre-teach Vocab | 5 word slides with context sentences, one per slide | slide-vocab-1 through slide-vocab-5 |
| — | Transition (Task) | Red background | slide-transition-task |
| 4 | Timed Reading | Task instructions + timer, 8 min | slide-timed-reading |
| 5 | Gallery Walk | Self-assessment instructions | slide-gallery-walk |
| — | Transition (Writing) | Red background | slide-transition-writing |
| 6 | Timed Writing | Writing prompt + timer, 10 min | slide-timed-writing |
| 7 | Wrap-up | Discussion question | slide-wrap-up |

**Total slides: 22**

---

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Content |
|----------|--------|---------|-----------|-----------|---------|
| slide-splash | Prime the theme of medical/bionic technology before any text appears | Full-screen `data-background-image="assets/pacemaker-heart.webp"`, no text | **Visual anticipation** — the X-ray heart with pacemaker confronts students with the wonder of bionic tech before any explanation | Complete absence of text forces students to form their own response to the image. If text were present, the amazement would be explained rather than felt. | 0 words |
| slide-title | Present topic and CTA with same background image | Logo + shield with rhetorical question + shield with CTA | **Metaphorical framing** — the pacemaker image embodies the lesson's central question about technology enhancing the body | "How far should we go to upgrade the human body?" in first shield. "Let's explore." CTA in second shield. | 10 words |
| slide-objectives | State 3 clear goals | Grid table with numbered items, dark background | **Advance organiser** — students need a mental roadmap | 3 "I can" statements: read for gist, read for detail, write my opinion | 25 words |
| slide-lead-in | Engage with the pacemaker image personally | Same background image, 3 shields with discussion prompts | **Personal connection** — students form their own interpretation before the reading | Shield 1: "What is this device?" Shield 2: "What does it do?" Shield 3: "Why is it an amazing invention?" Pair discussion. | 15 words |
| slide-transition-reading | Signal shift to reading phase | Red `#c0392b` background, single word | **Phase change** — red resets attention for a new cognitive mode | Single word: "Reading" centred on red | 1 word |
| slide-autoslide-1 through slide-autoslide-6 | Rapid auto-advance exposure to article header + each section | `data-autoslide="2500"` `data-transition="slide-in slide-out"` on each heading | **Pre-reading priming** — students see key language auto-advancing, building schema without JS race conditions | 6 slides: 1) "Body Technology" header + lead sentence, 2) Exoskeletons, 3) Mechanoprint, 4) Bionic contact lenses, 5) Running blades, 6) Bionic eyes. Each auto-advances after 2.5s. | ~60 words total |
| slide-gist | Check global understanding | Gist question in bold, fragment reveal for answer | **Gist check** — confirms overall comprehension before detail work | Question: "What is body technology?" Fragment reveal: "Technology that helps the human body work better and do more." | 8 words |
| slide-vocab-1 | Pre-teach "exoskeleton" | One word per slide, bold word, definition below, context sentence | **Blocking vocabulary** — removing lexical barriers before timed reading | "**exoskeleton** — a wearable frame that supports the body. Context: 'Powered exoskeletons help people lift very heavy things.'" | 15 words |
| slide-vocab-2 | Pre-teach "prosthetic" | Same format | **Lexical priming** | "**prosthetic** — an artificial body part. Context: 'Some prosthetic legs help people run faster than ever.'" | 15 words |
| slide-vocab-3 | Pre-teach "bionic" | Same format | **Lexical priming** | "**bionic** — electronic technology that replaces or improves body parts. Context: 'This kind of bionic eye helps people with eye injuries.'" | 15 words |
| slide-vocab-4 | Pre-teach "mechanoprint" | Same format | **Lexical priming** | "**mechanoprint** — an electronic skin that works like a fingerprint. Context: 'Scientists create a second skin called mechanoprint.'" | 15 words |
| slide-vocab-5 | Pre-teach "zoom" | Same format | **Lexical priming** | "**zoom** — to make an image appear larger or closer. Context: 'Bionic contact lenses can zoom in and out.'" | 15 words |
| slide-transition-task | Signal shift to reading task | Red background, single word | **Phase change** | "Task" on red | 1 word |
| slide-timed-reading | Set up timed reading task | Task instructions + `data-timer="480"` (8 min) | **Time pressure** — simulates real exam conditions, builds reading fluency | "Read the text and answer the 6 questions. You have 8 minutes." Tiered differentiation: Standard = questions visible, Advanced = read + notes, Elite = read once from memory. | 20 words |
| slide-gallery-walk | Self-assessment instructions | Numbered instruction list | **Student agency** — learners evaluate their own work | "1. Stand up and walk to the answer sheets. 2. Mark your worksheet (Correct / Half correct / Wrong). 3. Write your CEFR level in the box." | 15 words |
| slide-transition-writing | Signal shift to writing | Red background, single word | **Phase change** | "Writing" on red | 1 word |
| slide-timed-writing | Writing prompt with timer | Prompt + `data-timer="600"` (10 min) | **Productive output** — students synthesise ideas from the reading into a personal response | "Would it be a good idea to use bionic technology to live to 150 or even 200 years of age? Write at least 70 words." | 20 words |
| slide-wrap-up | Consolidate + final thoughts | 2 discussion questions | **Positive closure** | "Which body technology would you most want to have?" Show of hands. "What's one new thing you learned today?" | 10 words |
