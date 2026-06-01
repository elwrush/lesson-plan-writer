# Key Design Rules — lesson-plan-to-reveal

**CRITICAL RULE 0 — NO GRAY TEXT.** Any text on any slide that the student must read MUST use solid white `#fff` or solid yellow `#ffdd00`. Gray `#888`, `#666`, `rgba(255,255,255,0.5)` (50% white), `rgba(255,255,255,0.7)` (70% white), and any other muted/low-opacity colors are **strictly banned on all backgrounds** — dark navy `#1a1a2e`, teal `#0d4a3d`, green `#0d5e1a`, red `#c0392b`, and dark blue-gray `#2c3e50` alike. At classroom projection distance, these render as invisible gray smudges.

**Enforcement rules:**
- Every visible text element must have `color: #fff` or `color: #ffdd00` — either explicit or inherited from a parent
- `rgba(255,255,255, 0.85)` is the MAXIMUM dimming for any text element, and only for decorative/secondary metadata (source citations, material references) — NEVER for task instructions, answer text, strategy steps, labels, or student-facing content
- The base template's `.aim-label { color: #888; }` and `.source-cite { color: #666; }` are **traps** — override them in the inline `<style>` block (Step 2b) to `#fff`
- This rule applies universally — green slides are NOT the only affected case. Every background color in this project is dark enough that gray text is unreadable.

1. **Student-facing content on screen only** — task instructions, questions, vocabulary, answers. Teacher procedure text goes in `<aside class="notes">`. "Ss" is never used on screen.
2. **Objective slide uses accessible language** — avoid complex words like "identify", "distinguish", "inference". Use simple phrases. Tie outcomes to PET reading test.
3. **Title slide: topic + CEFR badge + strap subheader** — NO date, teacher name, duration, or materials.
4. **Task slides: brief student instructions** — extract task description from procedure, skip teacher-only instructions. Max 3 task lines on screen.
5. **Stage names: student-friendly language** — "Lead-in" → "Let's get Started", "Reading for gist" → "What's the main idea?", "Reading for detail" → "Finding details", "Reading for inference" → "Making conclusions", "Post-reading" → "Let's Discuss", "Wrap-up" → "Let's Review"
6. **Vocabulary slides** — generated AFTER lead-in stage. One word per slide with dark navy background. No sub-heading — the preceding red transition slide already signals the vocabulary phase. Yellow bold (#ffdd00) via `<span class="vocab-word">`.
7. **Answer slides** — use `<div class="answer-list">` flex layout (NOT `<table class="answer-table">`). Green background `#0d5e1a`. Statements visible on entry. Structure each row as:
    ```html
    <div class="a-row">
        <span class="a-num">#</span>
        <span class="a-q">Statement text</span>
        <span class="fragment fade-up a-ans a-cor"><i class="fa-solid fa-check"></i> Answer</span>
    </div>
    ```
    - `a-cor` for correct answers, `a-inc` for incorrect (not `answer-correct`/`answer-incorrect`)
    - `fragment fade-up` for animated reveal (not bare `fragment`)
    - Font Awesome `fa-check`/`fa-times` for icons (never raw Unicode U+2713/U+2717)
    - **Do NOT use `highlight-green`/`highlight-red`** (reveal.js keeps them at `opacity: 1`; they never hide)
    - **CRITICAL — No gray text.** Per Rule 0, ALL text on green slides must be white `#fff` or yellow `#ffdd00` — including `.a-num`, `.a-q`, `.aim-label`, and any other element. Gray, blue, or muted colors are invisible at projection distance on `#0d5e1a`.
8. **Transition slides: heading only (no subheader text).** The red background + icon + heading is sufficient — the teacher's spoken introduction bridges the gap. Remove all `<p>` elements from transition slides.
9. **Backgrounds**: dark navy `#1a1a2e` (title, lead-in, vocabulary), red `#c0392b` (transitions), teal `#0d4a3d` (pedagogical/strategy), green `#0d5e1a` (answer tables), dark `#2c3e50` (end)
10. **Title slide visuals**: Full-screen `data-background-image` with `data-background-color="#1a1a2e"` fallback. Logo at `120px`, h2 at `2.2em`, CEFR badge inline inside h2 (`vertical-align: middle`), subheader at `1em`. **Must add `style="justify-content: center;"`** to vertically center content. Opacity `0.85`. Do NOT use `r-stack` — it creates a letterbox effect.
11. **Text highlighting**: white text, dark text-shadow, pedagogical sections use white-on-teal
12. **Vocabulary words**: yellow boldface (`#ffdd00`) via `<span class="vocab-word">` — in both the word heading AND context sentence(s).

    **IPA-first fragment reveal pattern** — Each vocab slide MUST show the phonemic script first (visible on entry), then reveal the English spelling AND the context sentence simultaneously on click via fragments with matching `data-fragment-index="1"`.

    **Sequence:**
    1. **Entry** — Student sees IPA only (e.g., `/juː/`). No English word, no definition, no heading — the preceding red transition slide already announced vocabulary time.
    2. **Click** — The English word (yellow, bold) and the implicative example sentence (white with yellow target word) appear simultaneously via `class="fragment" data-fragment-index="1"`.

    **Visual layout:**
    ```html
    <section class="vocab-slide" data-background-color="#1a1a2e">
        <p><em>/juː/</em></p>
        <p class="fragment" data-fragment-index="1"><span class="vocab-word">yew</span></p>
        <p class="fragment" data-fragment-index="1" style="font-size:0.9em; margin-top:0.3em;">
            <em>The churchyard is full of <span class="vocab-word">yew</span> trees, some over 2,000 years old.</em>
        </p>
    </section>
    ```

    **Rules:**
    - The `data-fragment-index` MUST be `"1"` on both the word `<p>` and the sentence `<p>` so they reveal on the same click
    - The `<span class="vocab-word">` on the target word within the sentence applies yellow boldface (`#ffdd00`) automatically via CSS
    - Only the target word is yellow — never the entire sentence
    - **No "Important Words" heading on any vocab slide** — the transition slide (red background, "Some important words") already signals the phase. A heading on the first vocab slide would be redundant.

    **Test for implicative sentence:** Can a B2 student infer the word's meaning without a dictionary, without knowing the story, and with ONLY this one sentence on screen? If the sentence would still make sense with a blank in place of the target word, the context is insufficient.

    | Good (implicative — single sentence is enough) | Bad (just a book quote — doesn't imply meaning) |
    |---|---|
    | *The churchyard is full of yew trees, some over 2,000 years old.* | *Conor can see the great yew tree outside his window.* |
    | *The desert heat made the road ahead shimmering like water.* | *The monster's branches gather into a face, shimmering into a mouth and eyes.* |
    | *The wild horse had never been ridden — it was completely untamed.* | *The monster's voice has a quality to it — wild and untamed.* |

    The implicative example must come from **general life experience** (weather, nature, school, home, work, animals, plants, common objects) — not from the story world. This ensures the student can access the meaning independently. A single well-chosen sentence does the job — a second "In the story..." sentence adds visual clutter and gray text students won't read.
13. **Timer pill vs audio**: Never add `data-timer` to a slide that also has `data-audio-src`. Slides with audio playback should not have a timer pill — the two controls conflict visually and functionally.
14. **Proper HTML lists for letters/numbers**: Never use manual lettering or numbering in `<p>` tags (e.g., `<p><strong>A</strong> Option text</p>`). Use semantically correct HTML lists instead: `<ol type="A">` for lettered options, `<ol>` for numbered items, `<ul>` for bullet points. Each item gets its own `<li>` element. This ensures proper alignment and accessibility.
15. **Check/cross symbols: Font Awesome only, never Unicode**: Check marks (✓) and cross marks (✗) must use Font Awesome icons `<i class="fa-solid fa-check">` and `<i class="fa-solid fa-times">` — never raw Unicode characters U+2713 and U+2717. These Unicode characters do not render reliably across all browser/system font combinations. Font Awesome is loaded in the base template via CDN and renders consistently in every browser. Use `style="color:#4caf50;"` on check marks and `style="color:#ff5252;"` on cross marks for dark/teal/white backgrounds. On green `#0d5e1a` answer slides, use `style="color:#fff;"` for both (only white or yellow allowed on green backgrounds per rule 7).
