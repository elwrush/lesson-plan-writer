# Design Blueprint — M2/5A Business: How Much Is It Worth?

## Lesson Overview

**Class:** M2/5A
**Topic:** How much is it worth? — Reading for supporting details in a business article
**Duration:** 46 minutes
**CEFR:** B1
**Lesson shape:** R (Receptive Skills)
**Key pedagogy:** Three-tier differentiation (Standard / Advanced / Elite) on main task slides

---

## Stage-to-Slide Mapping

| Stage # | Stage Name | Slide Type(s) | Template Pattern | Slide IDs |
|---------|-----------|---------------|------------------|-----------|
| — | Splash | Full-screen image, no content | Title splash pattern | splash |
| — | Title | Logo + title + CTA over splash image | Title slide pattern | title |
| — | Objectives | 3 bullet points | Objective slide pattern | objectives |
| 1 | Discussion | Lead-in: 3 discussion prompts | Lead-in slide pattern | lead-in |
| — | Phase transition | Red background, section break | Phase transition pattern | lets-watch |
| 2 | Video Task Setup | Challenge selection: three-tier FA icons | Challenge selection pattern | video-challenge |
| 2 | Video | YouTube embed only — no text | Video slide pattern | video-intro |
| 2 | Video Task | Handout reference only | Task prompt pattern | video-questions |
| 2 | Video Feedback | Fragment-revealed answers (click to show) | Answer reveal pattern | video-feedback |
| — | Phase transition | Red background, bridge text: video→reading vocab | Phase transition pattern | transition-vocab |
| 3 | Vocabulary Preview | Word bank + 7 fill-in sentences + scan-for words | Vocabulary slide | vocab |
| — | Phase transition | Red background, section break | Phase transition pattern | lets-read |
| 4 | Reading Task Setup | Challenge selection: three-tier FA icons | Challenge selection pattern | reading-challenge |
| 4 | Reading: Global | Match questions to paragraphs + word locations | Reading task slide | reading-global |
| 4 | Reading: Close | Fill-in-the-blank supporting details | Reading task slide | reading-close |
| — | Phase transition | Red background, section break | Phase transition pattern | transition-think |
| 5 | Critical Thinking | Model answer + opinion frames | Production task slide | critical-thinking |
| 5 | Discussion | Open question + examples grounded in lesson content | Production task slide | discussion |
| 6 | Wrap-up | 6-item vocabulary recall table + reading reflection | Summary slide | wrap-up |
| — | End | Dark background + topic badge | End slide pattern | end |

**Phase transitions (red background):** lead-in→video (`lets-watch`), video→vocab (`transition-vocab`), vocab→reading (`lets-read`), reading→critical-thinking (`transition-think`).

---

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Words |
|----------|--------|---------|-----------|-----------|-------|
| splash | Set a business-themed visual anchor before any text appears | Full-screen `data-background-image`, no content, no notes | **Visual priming** — a business-themed image communicates the topic domain before the title loads. If text appeared first, students would read instead of anticipate. | Empty heading with background image. Students form own associations to the image. | 0 |
| title | Present the lesson topic with clear branding | Logo (ACT, 120px, centred at top) + title text in dark shield + CTA line in shield | **Topic announcement** — the logo anchors the school identity; the CTA ("Let's read and find out!") invites curiosity rather than stating a dry objective. | Logo uses `.title-logo` class → Lua filter centres in normal flow. Title in `.title-row` (dark shield). CTA in `.shield`. Background same as splash for continuity. | ~10 |
| objectives | Give students a mental roadmap of what they will achieve | 3 "I can..." statements, plain dark background | **Advance organiser** — students need to know the destination before the journey. Three specific outcomes (read for details, listen for specifics, discuss value) prevent the "what are we doing?" confusion. | Three short statements starting with "I can...". No shields, no images — clean and direct. | ~18 |
| lead-in | Activate prior knowledge and get students talking immediately | 3 bullet-point discussion questions | **Activation** — students discuss BEFORE any input, drawing on their own knowledge of business success. If the video or reading came first, students would respond to the material rather than to their own ideas. | Three open-ended prompts as bullet points. No infographic reproduction — that's in the textbook (p.44). Teacher introduces the infographic verbally. | ~18 |
| let's-watch | Signal the phase shift from discussion to video | Red background, single word | **Phase boundary** — red signals a clear break between input types. Students know the discussion is done and a new phase is starting. | Red background (`#c0392b`), single-heading text centred. | 2 |
| video-challenge | Give students agency over their listening approach | Three FA icon tiers: Standard (book-open) / Advanced (pencil) / Elite (star) | **Differentiated access** — students self-select their challenge level. The FA icons give instant visual recognition: book = scaffolded, pencil = independent, star = advanced. If the levels were labelled "Level 1/2/3", the progression would feel like ability ranking rather than challenge choice. | Three paragraphs with FA `<i>` icons + bold tier labels + one-line descriptions. No shields (this is a plain dark slide). | ~19 |
| video-intro | Play the YouTube video cleanly — no visual clutter | YouTube embed only, no other text on slide | **Minimal distraction** — during the video, students should look at the screen, not read text. Putting challenge text on this slide would distract from the video content. A bare embed maximises focus. | YouTube fenced div only. Speaker notes reference the handout (p.45). | 3 |
| video-questions | Pair-check video answers before whole-class reveal | Single line: "Complete the questions on p.45 — check with a partner" + timer | **Timed pair check** — students need a moment to consolidate before the teacher reveals answers. The timer creates focus; the partner check reduces anxiety. | One line of text + timer. No questions reproduced. Speaker notes cue the teacher. | 4 |
| video-feedback | Check answers with text evidence revealed on click | 4 answers as fragments (one click each). No separate evidence quotes — answers contain the key info. | **Paced revelation** — fragments prevent students from jumping ahead. The teacher controls the pace: reveal answer 1, discuss it, then click for answer 2. If all answers were visible at once, the weakest students would just copy. | 4 numbered items, each wrapped in `{.fragment .answer-reveal}`. Dark background. | ~20 (visible at start) |
| transition-vocab | Bridge video content to reading vocabulary | Red background + bridging sentence: "The video talked about entrepreneurs. Now these words will help you understand the reading." | **Cognitive bridge** — without a connecting sentence, students experience the topic shift as two unrelated chunks. The bridging text gives them a reason to care about the vocabulary. | Red background (`#c0392b`), centred text. Speaker notes include teacher script. | ~15 |
| let's-read | Signal the phase shift from vocabulary to reading | Red background, single word | **Phase boundary** — same pattern as let's-watch for consistency. | Red background, centred heading. | 2 |
| vocab | Activate key vocabulary before reading | 7 fill-in-the-blank sentences with word bank + 5 scan-for words | **Pre-teaching** — students need to know brand, logo, trust, customer service, quality, value before encountering them in the reading text. Fill-in format is more engaging than a simple list. The scan-for words prime recognition without pre-testing. | Word bank displayed as inline list. 7 numbered sentences with blanks + scan-for line at bottom. | ~55 (exercise, not prose) |
| reading-challenge | Give students agency over their reading approach | Three FA icon tiers: Standard / Advanced / Elite | **Differentiated access** — students self-select their challenge level for the reading task. Same FA icon pattern as video-challenge for visual consistency. | Three paragraphs with FA icons + bold labels + one-line descriptions. Plain dark slide. | ~19 |
| reading-global | Practise skimming for main ideas | Reference only: "Ex C (p. 46) — Match questions → paragraphs. Find evidence." | **No textbook duplication** — the exercise is on p. 46. The slide just tells students what to do and where. The word-location task was moved to the vocab pre-teach slide to avoid duplication. | Compact, single-line reference. Speaker notes carry the teaching script. | ~5 |
| reading-close | Practise scanning for supporting details | 6 fill-in-the-blank sentences from the text | **Close reading** — students find specific text evidence to complete the sentences. The fixed format (blanks in predictable positions) makes it easy to scan and answer. | 6 numbered sentences with blanks. Straightforward layout. Students use their textbooks. | ~25 |
| let's-think | Signal the shift from comprehension to evaluation | Red background | **Phase boundary** — moves students from "what did the text say?" to "what do I think about it?" | Red background, centred heading. | 3 |
| critical-thinking | Move from comprehension to opinion formation | Question prompt + 4-step thinking frame + model answer | **Critical evaluation** — students apply evidence from the text to form a reasoned opinion. The 4-step frame (identify → find evidence → decide → consider counter-argument) teaches thinking structure. The model answer demonstrates the expected level. | Short question. 4 numbered steps. Model answer in `{.fragment .answer-reveal}` — teacher reveals after giving students thinking time. | ~40 (visible at start: question + steps = ~20; model answer hidden) |
| discussion | Extend critical thinking to grounded examples | Open question: "From what you've learned today — what else adds value?" + 3 grounded prompts | **Transfer** — students apply the concept of "value" to examples rooted in the lesson (staff satisfaction, speed of service, fair prices) rather than arbitrary new concepts. | Open question. 3 prompts tied to lesson themes. | ~20 |
| wrap-up | Consolidate learning and preview next lesson | 6-item vocabulary recall table + reading reflection + next lesson preview | **Consolidation + anticipation** — the recall table checks vocabulary retention (all 6 exercise words tested); the reading reflection bridges comprehension to personal takeaway; the preview creates momentum across lessons. | Table with 6 definition-word pairs. Fill-in line for student reflection. Preview line at bottom. | ~30 |
| end | Close the lesson | Dark blue-gray background + topic + CEFR badge | **Positive closure** — signals the lesson is complete. No further instruction. | Dark background, brief text. | ~3 |

**Total slides:** 20 (including splashes, transitions, end)

---

## Design Principles Applied

1. **One idea per slide** — No slide mixes video + challenge text, or discussion + infographic. Each slide has exactly one job.
2. **No textbook duplication** — Handout questions and infographic tips stay on paper. Slides reference pages, not content.
3. **Phase transitions** — Red-background slides create clear cognitive breaks between lesson phases.
4. **Differentiation as agency** — FA icons + "Standard/Advanced/Elite" naming (not "Level 1/2/3") signal choice, not ranking.
5. **Visual consistency** — Challenge slides use the same FA icon pattern. Transition slides use the same red background. Title/logo pattern is consistent.
6. **25-word limit** — All slides are under 25 visible words except vocabulary (exercise format) and reading tasks (instructional text). Prose content stays ≤25 words.
7. **Fragments control pace** — Answers and model answers are hidden until the teacher clicks, preventing information overload.
8. **Speaker notes carry the teaching script** — Procedural instructions, timing, and teacher questions live in `::: notes`, not on visible slides.

---

## Image Requirements

| Slide ID | Image | Source | Status |
|----------|-------|--------|--------|
| splash | Business-themed image | Pixabay — already exists as `assets/splash.jpg` | Present |
| title | Same as splash | Reuse | Present |
| All others | None (dark background) | `data-background-color="#..."` | N/A |

---

## Auto-Animate Pairs

None in this lesson. Fragment reveals handle all sequenced content on the video-feedback and critical-thinking slides.

---

## Fragment Verification

| Slide ID | Fragment usage | Allowed? | Notes |
|----------|---------------|----------|-------|
| video-feedback | 4 answer items as `{.fragment .answer-reveal}` on list items | Yes | Each answer revealed on click. List-item-level fragments (not fenced-div-level). |
| critical-thinking | 1 model answer as `{.fragment .answer-reveal}` on a paragraph | Yes | Revealed after students complete their own thinking. |
