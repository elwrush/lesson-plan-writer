# Reveal.js Known Issues & Fixes

## Audio on Vocabulary Slides

### Problem
When using native `<audio data-autoplay>` for vocabulary TTS playback, the audio can:
1. **Double-play on slide entry** — when `data-autoplay` + the audio-slideshow plugin both call `.play()`
2. **Re-trigger on fragment advances** — some words replay when a fragment is revealed (inconsistently)
3. **Play for a millisecond on re-entry** — navigating away and back causes a brief audio glitch

### Root Cause
Three competing mechanisms control the same `<audio>` element:

| Mechanism | Trigger | Effect |
|-----------|---------|--------|
| **reveal.js core** (`startEmbeddedContent`) | `slidechanged` + `data-autoplay` | Plays on slide entry |
| **reveal.js core** (`startEmbeddedContent`) | `fragments.update()` | Called on each fragment element — though `queryAll(fragment, 'video,audio')` shouldn't find section-level audio, timing races with short files cause sporadic retriggers |
| **audio-slideshow plugin** (`selectAudio()`) | `slidechanged`, `fragmentshown`, `fragmenthidden` | Pauses previous audio, searches for new audio by plugin-specific IDs (`audioplayer-{h}.{v}`) |
| **audio-slideshow plugin** (`startAtFragment`) | `slidechanged` | Calls `Reveal.slide(h, v, -1)` on every slide entry, generating a **second** `slidechanged` event |

The plugin's `startAtFragment: false` causes a recursive `slidechanged` -> `Reveal.slide(h, v, -1)` -> second `slidechanged` chain. Between these two events, `startEmbeddedContent(currentSlide)` fires twice — the second call restarts the audio from the beginning, creating the millisecond glitch.

Short audio files (~0.3s for 2-syllable words) are more susceptible because the first playback finishes before the second fragment is clicked, leaving the audio in an `ended` state where subsequent calls can restart it.

### Fix (verified working — two valid approaches)

**Approach A: `data-autoplay` inside the word fragment (current, simpler)**

Place the `<audio>` element directly inside the English word's `<p class="fragment fade-up">` with `data-autoplay`. Reveal.js's `startEmbeddedContent(el)` plays it only when that specific fragment becomes visible:

```html
<section id="slide-vocab-1" class="vocab-slide" data-background-color="#1a1a2e" data-background-transition="none">
    <div style="text-align: center; padding: 60px 40px;">
        <p style="font-size: 1.8em; color: #ffdd00;">
            /ˌprɒsəpæɡˈnəʊziə/
        </p>
        <!-- Audio INSIDE the word fragment — plays when this fragment is revealed -->
        <p class="fragment fade-up" style="font-size: 2.2em; color: #fff; font-weight: bold;">
            <audio data-autoplay preload="auto" style="position: absolute; width: 0; height: 0; overflow: hidden;"
                   src="assets/vocab-prosopagnosia.mp3"></audio>
            <span class="vocab-word">prosopagnosia</span>
        </p>
        <p class="fragment fade-up" style="font-size: 1.2em; color: #fff;">
            People with prosopagnosia cannot recognise faces.
        </p>
    </div>
</section>
```

**Requirements:**
- Remove `RevealAudioSlideshow` from the plugins array in `Reveal.initialize()`
- Audio hidden via `position: absolute; width: 0; height: 0; overflow: hidden` (not `display:none`) so the browser loads audio data
- No custom `slidechanged` handler needed — reveal.js manages playback via `startEmbeddedContent`

**Approach B: `data-vocab-audio` with custom handler (archived, also valid)**

If the fragment `data-autoplay` approach doesn't suit your use case, use a custom attribute + `slidechanged` handler:

```html
<!-- Section level -->
<section id="slide-vocab-1" class="vocab-slide" data-background-color="#1a1a2e" data-background-transition="none">
    <!-- Audio: data-vocab-audio (not data-autoplay) so reveal.js startEmbeddedContent ignores it -->
    <audio data-vocab-audio preload="auto" style="position: absolute; width: 0; height: 0; overflow: hidden;" src="assets/vocab-word.mp3"></audio>
    ...
</section>
```

```javascript
// Remove audio-slideshow plugin from plugins array in Reveal.initialize()
plugins: [
    TimerPlugin,
    // ... other plugins ...
    // RevealAudioSlideshow intentionally removed — interferes with native <audio>
]

// Custom handler — ONLY playback mechanism, fires exclusively on slidechanged
Reveal.on('slidechanged', function(e) {
    var audio = e.currentSlide && e.currentSlide.querySelector('audio[data-vocab-audio]');
    if (audio) {
        audio.currentTime = 0;
        var p = audio.play();
        if (p && p.catch) p.catch(function(){});
    }
});
```

**Why Approach A works:**
1. **No `data-autoplay` on section-level audio** — reveal.js's `startEmbeddedContent(currentSlide)` doesn't find it (it's inside a fragment, not a direct section child)
2. **Only fires on fragment reveal** — `startEmbeddedContent(el)` on the fragment element plays it; slide entry does NOT trigger it
3. **No audio-slideshow plugin** — no `fragmentshown`/`fragmenthidden` handlers
4. **No custom handler needed** — fewer moving parts

### File Locations
- TTS script: `scripts/generate_vocab_audio.py`
- Voice ID config: `config/tts_vocab_voice.json`
- Voice design (one-time): `scripts/design_tts_voice.py`

---

## `data-autoplay` and Fragments (GitHub Issue #724)

### Problem
Audio elements with `data-autoplay` placed inside fragment elements play on slide entry instead of when the fragment is revealed.

```html
<span class="fragment">
    <audio data-autoplay src="audio1.ogg"></audio>
</span>
```

Both `audio1.ogg` and `audio2.ogg` play simultaneously when the slide enters, not when their respective fragments are shown.

### Upstream Status
Reported by the audio-slideshow plugin author (rajgoel). No fix merged into reveal.js core as of 5.1.0.

### Workaround
Place `data-autoplay` audio at the `<section>` level (not inside fragments), and use reveal.js events or custom listeners to trigger playback at the correct fragment step.

---

## Timer + Audio/Video Exclusion

### Problem
A slide with both `data-timer` (TimerPlugin countdown) and audio/video (either `data-audio-src`, native `<audio>`, `<video>`, or YouTube embed) causes conflicts — the timer counting down distracts from the media playback.

### Fix
Never use `data-timer` on a slide that plays audio or video, regardless of the playback mechanism:
- `data-audio-src` (audio-slideshow plugin)
- Native `<audio data-autoplay>` or `<audio data-vocab-audio>`
- `<video>` elements
- YouTube/Vimeo iframes or `data-background-iframe`

The check must cover ALL audio/video mechanisms, not just the audio-slideshow plugin.

---

## DOM Corruption from Scripted HTML Replacements

### Problem
Python scripts that use `content.replace()` on raw HTML files can silently corrupt the DOM structure. This manifests as:
- Text from one slide appearing on every slide (e.g., "Exercise 3 — Question (4)" on all 35 slides)
- An imbalanced number of opening/closing tags (e.g., 36 `<section>` opens but 37 `</section>` closes)
- Orphaned HTML elements (duplicate `<aside class="notes">` blocks) floating between slides
- revealjs-validator still passes because it checks HTML attributes, not DOM tree integrity

### Root Cause
Multiple edit scripts run sequentially, each calling `content.replace()` without verifying the DOM remains structurally valid. Common causes:

| Script action | How it corrupts |
|---------------|-----------------|
| Replacing annotation blocks | A regex that captures "everything between comment X and comment Y" can match across section boundaries, leaving orphan elements |
| Inserting or removing `<audio>` elements | Moving elements between nested children (section → fragment) changes the tag balance if the replacement pattern doesn't exactly match the source string |
| Running `replace()` without `count=1` | Can replace unintended occurrences of the pattern if the heading text or attribute values appear elsewhere in the file |
| Inline `<style>` blocks in the slides container | A `<style>` tag placed between `</section>` and the next `<section>` is technically valid HTML5 but can confuse browser repair algorithms when combined with other structural issues |

### Detection
revealjs-validator does NOT catch this. Detection requires:

```python
# Count open/close tags for sections
opens = content.count('<section')
closes = content.count('</section>')
assert opens == closes, f"Section mismatch: {opens} opens, {closes} closes — slides will be cut off"

# Count open/close tags for divs (extra </div> can close the slides container early)
div_opens = content.count('<div')
div_closes = content.count('</div>')
assert div_opens == div_closes, f"Div mismatch: {div_opens} opens, {div_closes} closes — content may be cut off"
```

The project's `lint_slides.py` runs all three checks automatically:
- Global `<section>` balance
- Global `<div>` balance
- Per-section `<div>` balance (catches extra `</div>` inside a single slide that causes all subsequent slides to be cut off)
- Literal Unicode escape detection (catches `\u2026`, `\u2014` etc. that should be actual characters)
