# Design Blueprint — Super Recognizers (060326, M2-4A, B1)

## Stage-to-Slide Mapping

| Stage # | Stage Name | Time | Slide Type(s) | Slide IDs |
|---------|-----------|------|---------------|-----------|
| — | — | — | Title | `slide-title` |
| — | — | — | Objective | `slide-objective` |
| 1 | Lead-in | 11min | Lead-in Qs → Video task → Vocab slides (×5) | `slide-lead-in`, `slide-video-task`, `slide-vocab-1` through `slide-vocab-5` |
| 2 | Reading for gist | 5min | Transition → Pedagogical (strategy) → Task (Ex 1) → Answers (Ex 1) | `slide-transition-gist`, `slide-strategy`, `slide-ex1-task`, `slide-ex1-answers` |
| 3 | Reading for detail | 15min | Transition → Task (Ex 2) → Answers (Ex 2, 3+3) → Task (Ex 3) → Answers (Ex 3, 3+3) | `slide-transition-detail`, `slide-ex2-task`, `slide-ex2-answers-1-3`, `slide-ex2-answers-4-6`, `slide-ex3-task`, `slide-ex3-answers-1-3`, `slide-ex3-answers-4-6` |
| 4 | Reading for inference | 5min | Task (Ex 4) → Discussion prompt | `slide-ex4-task`, `slide-ex4-discuss` |
| 5 | Post-reading speaking | 5min | Task (discussion) | `slide-discuss` |
| 6 | Wrap-up | 5min | Summary → End | `slide-summary`, `slide-end` |

## Per-Slide Design

| Slide ID | Intent | Feature | Principle | Mechanism | Template Ref |
|----------|--------|---------|-----------|-----------|--------------|
| `slide-title` | Show lesson title, CEFR, teacher | static | Coherence | Centered stacked layout: logo → title with badge → subheader | `reference-slideshow.html` Type 1 |
| `slide-objective` | State learning goal | static | Signaling | 4 bullet points in shield | Existing pattern |
| `slide-lead-in` | Orient Ss to face recognition | static | Segmenting | 3 discussion questions on dark bg, no fragments | Type 2 |
| `slide-video-task` | Instruct Ss to watch video + answer Q | audio (YouTube) | Modality | Brief instruction + video URL/link, dark bg | Custom |
| `slide-vocab-1` to `slide-vocab-5` | Present word with phonemic + audio | custom fragment + autoplay audio | Temporal Contiguity | Phonemic visible on entry + audio autoplays; English word reveals on fragment click | Custom |
| `slide-transition-gist` | Signal shift to reading for gist | static | Segmenting | Red bg, single heading | Type 7 |
| `slide-strategy` | Teach reading strategy for gist | static | Signaling | Strategy box content, teal bg | Type 8 |
| `slide-ex1-task` | Instruct Ex 1 (summary) | timer | Segmenting | Exercise number + brief instruction, dark bg, timer | Type 9 |
| `slide-ex1-answers` | Reveal summary answers | fragment fade-up | Temporal Contiguity | 4 answers in answer-list, each with text quote evidence, 1 slide | Type 10 |
| `slide-transition-detail` | Signal shift to reading for detail | static | Segmenting | Red bg, single heading | Type 7 |
| `slide-ex2-task` | Instruct Ex 2 (T/F) | timer | Segmenting | Exercise number + brief instruction, dark bg, timer | Type 9 |
| `slide-ex2-answers-1-3` | Reveal T/F answers 1-3 | fragment fade-up | Signaling | 3 items in answer-list, each with T/F badge + correction + short why | Type 10 |
| `slide-ex2-answers-4-6` | Reveal T/F answers 4-6 | fragment fade-up | Signaling | Same pattern, items 4-6 | Type 10 |
| `slide-ex3-task` | Instruct Ex 3 (answer questions) | timer | Segmenting | Exercise number + brief instruction, dark bg, timer | Type 9 |
| `slide-ex3-answers-1-3` | Reveal Q answers 1-3 | fragment fade-up | Temporal Contiguity | 3 items in answer-list, each with Q label + answer text | Type 10 |
| `slide-ex3-answers-4-6` | Reveal Q answers 4-6 | fragment fade-up | Temporal Contiguity | Same pattern, items 4-6 | Type 10 |
| `slide-ex4-task` | Instruct Ex 4 (personal answers) | static | Segmenting | Dark bg, questions shown | Type 9 |
| `slide-ex4-discuss` | Prompt discussion on Ex 4 | static | none — discussion | Questions rephrased as prompts | Type 11 |
| `slide-discuss` | Post-reading discussion | timer | none — freer practice | 3 discussion questions, dark bg, timer | Type 11 |
| `slide-summary` | Consolidate takeaways | static | Signaling | Checkmark bullets, dark bg | Type 12 |
| `slide-end` | End of presentation | static | none | Dark blue-gray bg | Existing pattern |

## Auto-Animate Pairs

None — no auto-animate in this lesson (no error-correction demonstrations, no S/V/O annotation, no formula transforms).

## Answer Slide Sizing

| Exercise | Items | Slides | Slide IDs | All ≤3? | Why design |
|----------|-------|--------|-----------|---------|------------|
| Ex 1 (summary) | 4 | 1 | `slide-ex1-answers` | Yes (4) | Compact — each is a word choice with a short quote, no full Why explanation needed |
| Ex 2 (T/F) | 6 | 2 | `slide-ex2-answers-1-3`, `slide-ex2-answers-4-6` | Yes | Each has T/F badge + 1-line correction, fits 3 per slide |
| Ex 3 (questions) | 6 | 2 | `slide-ex3-answers-1-3`, `slide-ex3-answers-4-6` | Yes | Each has a 1-line answer, fits 3 per slide |

## Fragment Verification

| Slide ID | Fragment usage | On allowed type? |
|----------|---------------|------------------|
| `slide-vocab-1` through `slide-vocab-5` | English word + context sentence `fragment fade-up` | Yes — vocab |
| `slide-ex1-answers` | Each a-row `fragment fade-up` | Yes — answers |
| `slide-ex2-answers-*-*` | Each a-row `fragment fade-up` | Yes — answers |
| `slide-ex3-answers-*-*` | Each a-row `fragment fade-up` | Yes — answers |
| No fragments on: lead-in, objectives, transitions, summary, end | — | ✓ |

## Color & Font Audit

| Slide ID | Background | Correct? | Font check |
|----------|------------|----------|------------|
| Title | `#1a1a2e` + image | ✓ | h2 2.2em, logo 120px, subheader 1em |
| Objective, Lead-in, Tasks | `#1a1a2e` | ✓ | body ≥1em |
| Vocab slides | `#1a1a2e` | ✓ | h2 2.2em, body 1.3em |
| Transitions | `#c0392b` | ✓ | heading only |
| Pedagogical/Strategy | `#1a237e` | ✓ | teal bg |
| Answer slides | `#052e0d` | ✓ | green bg, text ≥0.9em |
| Summary | `#1a1a2e` | ✓ | dark bg with ✓ bullets |
| End | `#2c3e50` | ✓ | dark blue-gray |

## TTS Audio Feature

Each vocab slide (`slide-vocab-1` through `slide-vocab-5`) includes:
```
<audio autoplay data-autoplay style="display:none;" src="assets/vocab-{word}.mp3"></audio>
```
- Fires immediately on slide entry (reveal.js `data-autoplay` native handling)
- No audio player UI shown (hidden via `display:none`)
- Reveal.js auto-pauses on navigation away
- Audio clips pre-generated via Inworld TTS-2 with bespoke US midwest female voice

## Vocab Slide HTML Pattern

```html
<section id="slide-vocab-1" class="vocab-slide" data-background-color="#1a1a2e" data-background-transition="none">
    <audio autoplay data-autoplay style="display:none;" src="assets/vocab-prosopagnosia.mp3"></audio>
    <div style="text-align: center; padding: 60px 40px;">
        <p style="font-size: 1.8em; color: #ffdd00; margin-bottom: 0.3em; letter-spacing: 0.05em;">
            /ˌprɒsəpæɡˈnəʊziə/
        </p>
        <p class="fragment fade-up" style="font-size: 2.2em; color: #fff; font-weight: bold; margin-top: 0.5em;">
            <span class="vocab-word">prosopagnosia</span>
        </p>
        <p class="fragment fade-up" style="font-size: 1.2em; color: #ccc; margin-top: 1em;">
            Prosopagnosia is a condition where people cannot recognise faces.
        </p>
    </div>
</section>
```
