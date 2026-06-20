# Common Pitfalls — Slide Building

## 1. Audio Inside Fragments (GitHub Issue #724)

**Problem:** `<audio data-autoplay>` inside `<p class="fragment fade-up">` plays on slide entry, NOT on fragment reveal. Both audio files play simultaneously when the slide enters.

**Fix:** Place audio at the `<section>` level with `data-vocab-audio` attribute. Use a `fragmentshown` handler that checks for `data-vocab-trigger` and plays the audio:

```javascript
Reveal.on('fragmentshown', function(e) {
    if (!e.fragment.querySelector('[data-vocab-trigger]')) return;
    var slide = e.fragment.closest('section');
    var audio = slide && slide.querySelector('audio[data-vocab-audio]');
    if (audio) { audio.currentTime = 0; audio.play().catch(function(){}); }
});
```

## 2. Gray Text Violations

**Problem:** POS markers (`(noun)`), timer labels, "Video says:" labels, and generation entry icons use `color: #888`, `#666`, or `#ddd`. At projection distance these are invisible.

**Fix:** Use only `#fff` (white) and `#ffdd00` (yellow) for all visible text. Differentiate with font size, bold weight, or `text-decoration: line-through`.

## 3. Two Context Sentences on Vocab Slides

**Problem:** Adding a second context sentence fragment to vocabulary slides violates the template pattern.

**Fix:** One context sentence per vocab slide. The second clarifying sentence goes in the speaker notes.

## 4. Vocab Context Sentences Structured as Definitions

**Problem:** "A misogynist is someone who..." — this is a dictionary definition, not a natural context sentence. Students don't absorb meaning from definitions.

**Fix:** Use natural context where meaning is obvious from usage:
- BAD: "A tradwife is an influencer who promotes traditional domestic lifestyles."
- GOOD: "She started following tradwife influencers who post videos about cooking for their husbands."

## 5. Vocabulary Word Not Wrapped in `<span class="vocab-word">`

**Problem:** The target word in context sentences is plain text, not wrapped in `<span>`, so it doesn't render in yellow bold.

**Fix:** Always wrap the target word: `<span class="vocab-word">manosphere</span>`

## 6. IPA Not Following British Council Standard

**Problem:** Transcriptions use American-style notation (`/ɛ/`, `/oʊ/`, `/ɪr/`) or include final `/r/`.

**Fix:** Use British Council phonemic symbols from `docs/british-council-phonemic-chart.md`:
- `/e/` not `/ɛ/` — "echo" = `/ˈekəʊ/`
- `/əʊ/` not `/oʊ/` — "echo" = `/ˈekəʊ/`
- `/ɒ/` not `/ɑ/` — "misogynist" = `/mɪˈsɒdʒɪnɪst/`
- `/ɪə/` not `/ɪr/` — "manosphere" = `/ˈmænəsfɪə/`
- Non-rhotic — no final `/r/` — "breadwinner" = `/ˈbredwɪnə/`

## 7. RevealAudioSlideshow Left in Plugins

**Problem:** `RevealAudioSlideshow` in the plugins array interferes with native `<audio data-vocab-audio>` playback. Its `fragmentshown`/`fragmenthidden` handlers fight the custom handler.

**Fix:** Remove `RevealAudioSlideshow` from the plugins array in `Reveal.initialize()`. Also remove the orphaned `audio:` config block and the `audio-slideshow/plugin.js` script tag.

## 8. YouTube Iframes Overflowing or Broken Aspect Ratio

**Problem:** Task slide iframes at 90% width produce ~650px video height on 720px slides, crowding out headings. Resizing width alone breaks the 16:9 ratio because `padding-bottom` is calculated relative to the **section width**, not the container width.

**Fix:** Always set BOTH `width` and `padding-bottom` as inline styles on `.iframe-container`:
- `padding-bottom = width × 9/16`
- Example: width 53% → padding-bottom: 53 × 9/16 = 29.8%
- Example: width 44% → padding-bottom: 44 × 9/16 = 24.75%
- Original template: width 90% → padding-bottom 50.625% (90 × 9/16 = 50.625)

Add a visible timestamp label above the video so the teacher knows the segment range if the embed breaks:
```html
<p style="font-size: 0.75em; color: #ffdd00; margin-bottom: 0.3em;">&#9654; 0:02 – 2:33</p>
```

## 9. Timer SFX Files Missing

**Problem:** `blip.mp3` and `BELL.mp3` never copied to slides assets, so the timer plugin runs silently.

**Fix:** Always copy from `C:\PROJECTS\SFX\` in Step 2 of the build workflow.

## 10. DOM Imbalance After Editor Operations

**Problem:** Any Python `content.replace()` on HTML risks unbalanced tags. The revealjs-validator does NOT catch this.

**Fix:** Always count section/div tags after every scripted HTML operation.

## 11. Answer Text Too Wordy

**Problem:** Answers echo the full transcript quote instead of being concise B2-level takeaways.

**Fix:** Short factual answers. The WHY line provides the source reference — the teacher explains the connection.

## 12. Auto-Animate Entry Slide Has `data-auto-animate`

**Problem:** The slide BEFORE an auto-animate pair must NOT have `data-auto-animate`, or the animation triggers on the wrong boundary.

**Fix:** Only set `data-auto-animate` on the entry and reveal slides of the pair itself. The previous slide (static) has no auto-animate attribute.
