# Pedagogical Design Dictionary

A reference for selecting the right reveal.js feature for each pedagogical goal. The `lesson-plan-to-reveal` skill delegates design decisions here instead of embedding them in workflow steps.

---

## Decision Framework

```
What must the student see happen?
│
├─ A word/part changes appearance (color, border, strikethrough)?
│   → AUTO-ANIMATE (two consecutive <section> with matching data-id)
│   Example: Subject word turns yellow → student sees WHERE the subject is
│
├─ Content reveals on click (answer appears, step builds)?
│   → FRAGMENTS on a single <section>
│   Example: Answer column appears row by row
│
├─ Each step is a discrete teaching moment (teacher pauses)?
│   → SIBLING SLIDES (one <section> per step, no auto-animate)
│   Example: Strategy demonstration — one slide per step
│
├─ Text needs progressive highlighting within a block?
│   → CODE + DATA-LINE-NUMBERS on <pre><code>
│   Example: Reading passage — highlight key sentence, then details
│
├─ A wrong option gets visually eliminated?
│   → FRAGMENT STRIKE (class="fragment strike")
│   Example: Multiple choice — strike out eliminated answers
│
├─ Items on one side need to reposition to show correct matching?
│   → AUTO-ANIMATE (matching data-id on sibling elements within a shared container)
│   Example: Letters A–F on left, paragraph numbers on right. Right-side elements
│   have data-id="p1"…"p8". On reveal they reorder to match correct pairings.
│   Auto-animate animates each item sliding to its new position.
│   The transformation IS the answer — no fragments needed.
│   Design rule: do NOT add instructional text ("Click to check", "Click to reveal").
│   The visual rearrangement is self-evident. Unmatched items dim and sink to the bottom.
│
└─ A word needs temporary emphasis (grow, color)?
    → FRAGMENT GROW or FRAGMENT HIGHLIGHT-CURRENT-*
    Example: Key vocabulary word on click
```

## Feature Lookup Table

| Feature | What it does | Pedagogical sweet spot |
|---|---|---|
| `data-line-numbers` on `<code>` | Highlights specific lines progressively, step by step | Grammar rule parts lighting up one at a time |
| `data-mark` on any element | Yellow `<mark>` highlights via Mark.js | Key words in a reading passage |
| `data-transition="zoom"` | Dramatic slide entrance | Phase changes, answer reveals, big moments |
| `data-background-gradient` | Gradient backgrounds | Visual variety without images |
| Vertical slides (nested `<section>`) | Sub-steps, optional content, fast-finisher extensions | Grammatical sub-rules, extra practice |
| `data-audio-src` | Audio playback on slide entry | Listening tasks |
| `data-autoslide` | Self-advancing timed advance | Speed-reading passages, timed grammar drills |
| Lightbox (`data-preview-image`, `data-preview-video`) | Click-to-enlarge media | Textbook page close-ups, diagram details |
| `class="r-fit-text"` | Auto-sizing text to fill slide | Single powerful word, key concept, grammar rule summary |
| **Auto-animate: list matching** | `<li>` items match by content; new items slide in, removed items slide out | Building grammar rules one step at a time; vocabulary add/remove |
| **Auto-animate: position re-ordering** | Sibling elements with `data-id` change DOM order; auto-animate slides each to new position | **Matching exercises** — letters vs items that rearrange. No fragments, no instructional text. Rearrangement IS the answer. |
| **Auto-animate: code blocks** | `<pre data-id="code"><code data-line-numbers>` — progressively build code/text | Reading passages — highlight topic sentences per slide |
| **Auto-animate: per-element** | `data-auto-animate-duration`, `data-auto-animate-easing` | Make key word transform slower than surrounding content |
| **Custom CSS fragments** | `.fragment.blur { filter: blur(5px); }` — unlimited effects | Blur all words, focus one at a time with `current-fragment` |
| **Nested fragments** | Sequential effects on same element (fade in → highlight → fade out) | Multi-step reveal of a single sentence |
| **Directional fragments** | `fade-up`, `fade-down`, `fade-left`, `fade-right` | Draw student eye to specific location |
| **`highlight-current-*`** | Temporary color change, reverts on next click | Word emphasis without permanent color change |
| **`fade-in-then-out` / `current-visible`** | Appears on click, disappears on next click | Temporary scaffolding — hint appears, then vanishes |
| **`r-stack`** | Centers and layers elements on top of each other | Text over image without background-image/text-shield hack |
| **`r-stretch`** | Resizes element to fill remaining vertical space | Image fills slide between title and caption |
| **`r-frame`** | Subtle border, hover effect on links | Highlighting images as interactive/clickable |

## Key Decision Rule

**Auto-animate** for transformations — color changes, border reveals, word replacement, and element repositioning (items reordering within a container to show correct matching).

**Fragments** for reveals — answers appearing, options being eliminated.

**Sibling slides** for discrete teaching moments — each step is its own slide where the teacher pauses.

## Mayer's 12 Principles of Multimedia Learning

| Principle | What it says | reveal.js implementation |
|---|---|---|
| **Segmenting** | Break complex content into learner-paced segments | Fragments (any variant) — teacher controls reveal pace |
| **Signaling** | Highlight essential material to guide attention | Auto-animate (color/underline transform), data-line-numbers, data-mark, highlight-current-* |
| **Temporal Contiguity** | Present corresponding elements simultaneously | Auto-animate (matching data-id transitions happen together) |
| **Spatial Contiguity** | Place corresponding text and images near each other | r-stack (text layered over image, not separated) |
| **Modality** | Use narration + visuals rather than text + visuals | Audio-slideshow plugin (data-audio-src on sections) |
| **Redundancy** | Avoid duplicating text and narration | Fragments reveal step by step, never all at once |
| **Coherence** | Remove extraneous words, sounds, and pictures | Static orientation slides, transition slides (cognitive reset) |
| **Personalization** | Use conversational style rather than formal | Direct "you" imperatives in B1 authorial voice rules |
| **Multimedia** | Use words AND pictures rather than words alone | r-stack with image + text overlay |
| **Pre-training** | Provide prerequisite knowledge first | Diagnostic test slides before teach slides (TTT structure) |
| **Worked Example** | Guide through solved problems step by step | Auto-animate code blocks with data-line-numbers |
| **Interactivity** | Allow learners to control the pace | Fragment click-through, teacher-paced reveals |

Sources: Mayer, R.E. (2005). Cognitive Theory of Multimedia Learning. Cambridge University Press.

## Common Anti-Patterns

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Static text stating "X is the subject" | Tells instead of shows. Violates Signaling — no visual cue. | Auto-animate: word becomes yellow/underlined. Student watches the subject *emerge*. |
| All content on one crowded slide | Cognitive overload. Violates Segmenting. | One concept per slide. Build up with auto-animate or sibling slides. |
| Fragments on expository content | Unnecessary clicks create extraneous load (Sweller). | Simple sibling slides or auto-animate for actual transformations. |
| `highlight-green`/`highlight-red` | Forces `opacity: 1` — content always visible, no hiding. | Use `a-cor`/`a-inc` with `fragment fade-up`. |
| Putting the answer in the slide title | Student reads answer before attempting task. | Answer appears on separate slide after task slide. |
| Instructional text like "Click to check" on auto-animate reveals | Unnecessary — the transformation IS the answer. The visual effect explains itself. | Remove. Students understand that clicking advances the slide and shows the transformation. |

## Auto-animate HTML Patterns

### Color/Underline Transform

Two consecutive slides with matching `data-auto-animate-id`. Use `data-id` on child elements to match them across slides:

```html
<!-- Entry: transparent border -->
<section data-auto-animate data-auto-animate-id="example" data-background-color="#1a1a2e">
    <p data-id="target" style="border-bottom: 2px solid transparent;">Key word</p>
</section>
<!-- Reveal: visible border -->
<section data-auto-animate data-auto-animate-id="example" data-background-color="#1a1a2e">
    <p data-id="target" style="border-bottom: 3px solid #ffdd00;">Key word</p>
</section>
```

### Position Re-ordering (Matching Exercise)

Items on one side of a two-column layout reposition via `data-id` matching. Both slides have the SAME background to avoid flash:

```html
<!-- Entry: items in numerical/default order -->
<section data-auto-animate data-auto-animate-id="match" data-background-color="#1a1a2e">
    <div style="display: grid; grid-template-columns: auto 1fr; gap: 0.3em 2em;">
        <div><!-- A, B, C, ... --></div>
        <div data-id="container">
            <p data-id="p1">Item 1</p>
            <p data-id="p2">Item 2</p>
            ...
        </div>
    </div>
</section>
<!-- Reveal: items in correct matching order -->
<section data-auto-animate data-auto-animate-id="match" data-background-color="#1a1a2e">
    <div style="display: grid; grid-template-columns: auto 1fr; gap: 0.3em 2em;">
        <div><!-- A, B, C, ... --></div>
        <div data-id="container">
            <p data-id="p4">Item 4</p>   <!-- moved to match A -->
            <p data-id="p2">Item 2</p>   <!-- moved to match B -->
            ...
            <p data-id="p1" style="opacity:0.4;">Item 1</p>  <!-- unmatched, dimmed -->
        </div>
    </div>
</section>
```

Design rules:
- No instructional text ("Click to check", "Click to reveal") — the rearrangement IS the answer
- Same background on both slides (prevents flash)
- Unmatched items remain on reveal slide but dimmed (`opacity: 0.4`)
