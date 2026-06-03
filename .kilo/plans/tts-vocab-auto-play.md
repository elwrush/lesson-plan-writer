# Plan: TTS Vocabulary Auto-Play for reveal.js Slides

## Overview

When a vocabulary slide appears in the slideshow, the word is spoken immediately via a pre-generated audio clip using Inworld TTS-2 with a bespoke US midwest female voice. No audio player UI is shown — the word plays automatically and simultaneously with the phonemic script.

---

## File 1: `scripts/design_tts_voice.py` — Voice Design (one-time setup)

Creates and publishes a bespoke Inworld voice from a demographic description. Run once; saves the `voiceId` to a JSON file for reuse.

```python
"""Design and publish a bespoke Inworld TTS voice for vocabulary audio."""
import os, sys, json, base64, requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API_KEY = os.environ.get("INWORLD_API_KEY")
if not API_KEY:
    print("ERROR: INWORLD_API_KEY environment variable not set")
    sys.exit(1)

AUTH_HEADER = f"Basic {API_KEY}"

# Step 1: Design the voice
design_prompt = (
    "Pleasant female voice, mid-20s to early-30s, "
    "US midwest accent, warm and clear with good syllable stress. "
    "Natural, conversational delivery. Perfect broadcast quality audio."
)

preview_text = "Can you recognize faces that you have only seen once? Let's find out."

print("Designing voice...")
r = requests.post(
    "https://api.inworld.ai/voices/v1/voices:design",
    headers={"Authorization": AUTH_HEADER, "Content-Type": "application/json"},
    json={
        "design_prompt": design_prompt,
        "voice_name": "us-midwest-female-vocab",
        "preview_text": preview_text,
    }
)
r.raise_for_status()
preview_id = r.json()["previewVoices"][0]["voiceId"]
print(f"  Preview voice ID: {preview_id}")

# Step 2: Publish the voice
print("Publishing voice...")
r2 = requests.post(
    f"https://api.inworld.ai/voices/v1/voices/{preview_id}:publish",
    headers={"Authorization": AUTH_HEADER, "Content-Type": "application/json"},
    json={
        "displayName": "US Midwest Female (Vocabulary)",
        "description": "US midwest female voice, warm, clear, good syllable stress, for vocabulary word audio",
        "tags": ["custom", "vocabulary", "esl"],
    }
)
r2.raise_for_status()
voice_id = r2.json()["voiceId"]
print(f"  Published voice ID: {voice_id}")

# Step 3: Save voice ID for reuse
config = {"voice_id": voice_id, "description": design_prompt}
config_path = os.path.join(os.path.dirname(__file__), "..", "config", "tts_vocab_voice.json")
os.makedirs(os.path.dirname(config_path), exist_ok=True)
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
print(f"  Saved to {config_path}")
print("Done — voice is ready for vocabulary TTS generation.")
```

---

## File 2: `scripts/generate_vocab_audio.py` — Batch word audio generation

Takes a list of vocabulary words and a voice ID, generates MP3 clips via Inworld TTS-2, saves to the slides assets directory.

```python
"""Generate TTS audio clips for vocabulary words using Inworld TTS-2."""
import os, sys, json, base64, requests
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API_KEY = os.environ.get("INWORLD_API_KEY")
if not API_KEY:
    print("ERROR: INWORLD_API_KEY environment variable not set")
    sys.exit(1)

def load_voice_id():
    """Load the published voice ID from config."""
    config_path = Path(__file__).parent.parent / "config" / "tts_vocab_voice.json"
    if not config_path.exists():
        print(f"ERROR: Voice config not found at {config_path}")
        print("Run scripts/design_tts_voice.py first.")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)["voice_id"]

def generate_word_audio(word: str, voice_id: str, output_dir: Path) -> Path:
    """Generate an MP3 file for a single vocabulary word."""
    r = requests.post(
        "https://api.inworld.ai/tts/v1/voice",
        headers={
            "Authorization": f"Basic {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "text": word,
            "voice_id": voice_id,
            "model_id": "inworld-tts-2",
            "audio_config": {
                "audio_encoding": "MP3",
                "sample_rate_hertz": 24000,
            },
        },
    )
    r.raise_for_status()
    audio_bytes = base64.b64decode(r.json()["audioContent"])

    # Save to output directory
    filename = f"vocab-{word.lower().replace(' ', '-')}.mp3"
    out_path = output_dir / filename
    with open(out_path, "wb") as f:
        f.write(audio_bytes)
    print(f"  Generated: {filename} ({len(audio_bytes)} bytes)")
    return out_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("words", nargs="+", help="Vocabulary words to generate")
    parser.add_argument("--output-dir", required=True, help="Path to slides/assets/ directory")
    args = parser.parse_args()

    voice_id = load_voice_id()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(args.words)} word audio files...")
    for word in args.words:
        generate_word_audio(word, voice_id, output_dir)
    print("Done.")
```

---

## File 3: Modified Vocabulary Slide HTML Pattern

Each vocabulary `<section>` in the slideshow gets a hidden `<audio autoplay data-autoplay>` element. This uses reveal.js's native `autoPlayMedia` handling — reveal.js auto-pauses media when navigating away.

```html
<section id="slide-vocab-1" data-background-color="#1a1a2e" data-background-transition="none">
    <!-- Hidden autoplay audio — fires immediately on slide entry -->
    <audio autoplay data-autoplay style="display:none;"
           src="assets/vocab-prosopagnosia.mp3"></audio>

    <div class="slide-content" style="text-align: center; padding: 60px 40px;">
        <!-- Phonemic script (visible on slide entry) -->
        <p style="font-size: 1.8em; color: #ffdd00; margin-bottom: 0.3em; letter-spacing: 0.05em;">
            /ˌprɒsəpæɡˈnəʊziə/
        </p>
        <!-- English word (reveals on fragment click) -->
        <p class="fragment fade-up" style="font-size: 2.2em; color: #fff; font-weight: bold; margin-top: 0.5em;">
            prosopagnosia
        </p>
        <!-- Context sentence -->
        <p class="fragment fade-up" style="font-size: 1.2em; color: #ccc; margin-top: 1em;">
            Prosopagnosia is a condition where people cannot recognise faces.
        </p>
    </div>
</section>
```

**Key details:**
- `<audio autoplay data-autoplay>` triggers playback on slide entry
- `style="display:none"` hides the audio player — no UI visible
- Reveal.js's `autoPlayMedia: null` (default) allows `data-autoplay` elements to auto-play
- Reveal.js auto-pauses `<audio>` when navigating away from the slide
- Phonemic script shown immediately; English word + context sentence reveal on fragment click

---

## Integration: How It Connects to lesson-plan-to-reveal

The vocabulary slide generation flow becomes:

1. User selects pre-teach vocabulary (already done — 5 words)
2. Run `scripts/generate_vocab_audio.py` with the vocabulary list and target output dir
3. Build vocabulary slides as raw HTML `<section>` elements inside `index.html`
4. Each slide includes the hidden `<audio autoplay data-autoplay>` element with the correct `src`

**New step 30 inserted into the `lesson-plan-to-reveal` skill's workflow, after vocabulary words are determined and before writing slides:**

```powershell
# Step 0c: Generate TTS audio for vocabulary words
$vocabWords = @("prosopagnosia", "extraordinary", "recruit", "remarkable", "scanners")
$assetsDir = "output/{subfolder}/slides/assets"
python scripts/generate_vocab_audio.py @vocabWords --output-dir $assetsDir
```

**No changes needed to `base-slides-template.html`** — reveal.js handles `data-autoplay` natively. The audio-slideshow plugin is NOT required for this feature.

---

## Edge Cases

| Scenario | Handling |
|---|---|
| **TTS API unavailable** | Script fails gracefully with error message; feature skipped; slides still generate without audio |
| **Word has special chars** | Filename sanitized: lowercase, spaces → hyphens. E.g., "face recognition" → `vocab-face-recognition.mp3` |
| **Same word on multiple slides** | Each `<audio>` has its own `src` pointing to the same file. OK because native `<audio>` elements are independent DOM elements |
| **Voice not yet designed** | `generate_vocab_audio.py` checks for config file; if missing, prompts: "Run scripts/design_tts_voice.py first" |
| **API key not set** | Error message printed; slides generated without audio |
| **Slide navigated away before audio finishes** | Reveal.js auto-pauses `<audio>` on navigation; audio stops cleanly |

---

## Files Summary

| File | Action | Purpose |
|---|---|---|
| `scripts/design_tts_voice.py` | **Create** | One-time: design + publish bespoke Inworld voice |
| `scripts/generate_vocab_audio.py` | **Create** | Generate MP3 clips for vocabulary words |
| `.kilo/skills/lesson-plan-to-reveal/SKILL.md` | **Modify** | Add TTS generation step before vocabulary slides |
| `config/tts_vocab_voice.json` | **Auto-created** | Stores the published voice ID for reuse |
| `templates/base-slides-template.html` | **No change** | Native `data-autoplay` handles playback |
