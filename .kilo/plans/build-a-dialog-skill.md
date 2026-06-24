# Plan: `build-a-dialog` — Global Skill for Multi-Voice TTS Dialogs

**Status:** Plan  
**Date:** 24 June, 2026  
**Skill location:** `~/.kilo/skills/build-a-dialog/`

---

## Purpose

Generate a high-quality multi-voice audio dialog from an annotated Markdown script. Each character speaks through a distinct Inworld TTS-2 voice. Stage directions are converted to TTS-2 steering tags. Lines are stitched via ffmpeg with natural inter-turn pacing.

**Output:** `output/dialogs/{YYYYMMDD}-{topic}.mp3`

---

## Research Citations

| Source | Finding | Applied to |
|--------|---------|-----------|
| Inworld TTS-2 steering tags (Runware docs) | `[speak warmly, as if greeting an old friend]` — free-form stage directions, no closed emotion set | Stage direction → steering tag conversion |
| Inworld best practices (docs.inworld.ai) | Capitalize EMPHASIS words; punctuation controls pacing; `language` field for accent consistency | Dialog text preparation |
| build-a-monolog proven patterns | NO ellipses, NO `[sigh]/[laugh]` non-verbals, ≤3 steering tags per line, single paragraph | Text quality guardrails |
| FFmpeg concat demuxer (SuperUser) | `-f concat -i files.txt` with `inpoint` trimming removes MP3 encoder priming gaps | Stitching strategy |
| FFmpeg acrossfade (SuperUser) | `acrossfade=d=0.05` sub-100ms crossfades feel like natural turn-taking | Optional crossfade between lines |
| Inworld voice design API | Bespoke voices from demographic text: age, gender, region, tone, pacing | Character voice creation |
| Inworld system voices (148+) | Clive, Felix, Sophie, Victoria, Ashley, Jessica, Riley, Mia, etc. | Quick-start without designing voices |

---

## Dialog Input Format

The skill ingests annotated Markdown dialog in this format (from the lesson plan handout pattern):

```markdown
### Teacher Demo Model -- After the Drive-In

*Four characters: Cherry, Marcia, Brenda, Linda. Cherry's bedroom, late evening.*

| Character | Voice notes | Key line |
|:----------|:-------------|:---------|
| **Cherry** | Thoughtful, questioning. She speaks in full sentences — she's thinking as she talks. Her lines carry the argument. She's the one who changed tonight. | "He looked at me. Not like a Soc. Not like he was deciding whether I was worth his time. He just... looked." |
| **Marcia** | Playful, warm, loyal. She saw it happen. She agrees with Cherry but is less intellectual — she speaks from feeling. | "If life is hard for both sides... then maybe we're not so different after all." |
| **Brenda** | Sharp, defensive. She's protecting her worldview. She interrupts. She's not cruel — she's scared of what Cherry's questions mean. | "They're greasers, Cherry. They're not like us." |
| **Linda** | Soft, curious. She asks the questions Cherry hasn't answered yet. She doesn't take sides — she wants to understand. | "Did you believe it? When you said it?" |

**Cherry:** He looked at me. Not like a Soc. Not like he was deciding whether I was worth his time. He just... looked.

**Marcia:** (laughs) He did. Ponyboy. He was so quiet I thought he was scared, but he wasn't. He was watching everything.

**Brenda:** (skeptical) They're greasers, Cherry. They're not like us. They carry blades. Two-Bit nearly got arrested last month for stealing tyres from Mr Brennan's garage.
```

**Parser extracts:**
- **Character table** → `[name, voice_notes, key_line]` for voice design
- **Dialog body** → `[character, stage_direction?, line_text]` per turn
- **Setting** → `*Four characters: ... Cherry's bedroom, late evening.*` — context line

---

## Skill Architecture

```
~/.kilo/skills/build-a-dialog/
├── SKILL.md                       # Workflow instructions for the agent
├── scripts/
│   ├── parse_dialog.py            # Parse Markdown → JSON dialog structure
│   ├── design_voices.py           # Voice notes → Inworld bespoke voice IDs
│   ├── generate_lines.py          # Dialog + voice IDs → per-line MP3 files
│   └── stitch_dialog.py           # MP3 clips → single MP3 via ffmpeg
├── references/
│   ├── steering-tag-recipes.md    # Stage direction → steering tag conversion table
│   └── inworld-voice-library.md   # Prebuilt system voice catalog with demographics
└── assets/
    └── dialog-template.md         # Markdown template for authoring new dialogs
```

---

## Workflow (7 Steps)

### Step 1 — Parse Dialog

The agent extracts the dialog from a Markdown file or inline text. A Python parser (`scripts/parse_dialog.py`) produces a JSON structure:

```json
{
  "title": "Teacher Demo Model -- After the Drive-In",
  "setting": "Cherry's bedroom, late evening",
  "characters": [
    {
      "name": "Cherry",
      "voice_notes": "Thoughtful, questioning. She speaks in full sentences...",
      "key_line": "He looked at me. Not like a Soc..."
    },
    {
      "name": "Marcia",
      "voice_notes": "Playful, warm, loyal. She saw it happen...",
      "key_line": "If life is hard for both sides..."
    },
    ...
  ],
  "turns": [
    {"character": "Cherry", "stage_direction": null, "line": "He looked at me. Not like a Soc..."},
    {"character": "Marcia", "stage_direction": "laughs", "line": "He did. Ponyboy..."},
    {"character": "Brenda", "stage_direction": "skeptical", "line": "They're greasers, Cherry..."},
    ...
  ]
}
```

**Parser detects:**
- Character table: `| **Name** | Voice notes | Key line |`
- Dialog lines: `**Name:** (stage direction?) Dialogs text.`
- Stage directions in `(parentheses)` inline
- Scene setting from italic paragraph before the table

### Step 2 — Design Voices

Map each character's voice notes to an Inworld voice. Two paths:

**Path A (Quick): Prebuilt system voices**
Pick the closest Inworld system voice by matching demographic + tone:
```
Cherry (thoughtful, questioning) → "Sophie" (British female, measured) 
  — but needs Oklahoma dialect → use US voice + steering tag for accent
```

For the Oklahoma teenage female characters, the prebuilt options are limited:
- "Mia" (young female, American) — too youthful
- "Ashley" / "Jessica" / "Lauren" — adult American female, not teenage

**Path B (Preferred): Bespoke voice design**
Create 4 custom voices via Inworld Voice Design API using each character's voice notes + demographic:

```python
# Character voice design prompt template:
design_prompt = (
    f"A {age_range} female voice from {region}, {tone}. "
    f"{pacing}. {quality}. "
    f"Natural conversational delivery. "
    f"Perfect broadcast quality audio."
)

# Cherry example:
# "A 16-year-old female voice from urban Oklahoma, thoughtful and questioning.
#  She speaks in measured full sentences, thinking as she talks.
#  Natural conversational delivery. Perfect broadcast quality audio."
```

**⚠️ Critical:** Designing 4 bespoke voices → 4 API calls. Each requires `POST .../voices:design` then `POST .../voices/{previewId}:publish`. Store voice IDs in the dialog JSON for reuse.

**Voice ID caching:** If the same characters appear in multiple dialogs (e.g., Cherry/Marcia/Brenda/Linda across lesson series), voice IDs should be persisted in `cloned-voices/readme.md` and loaded from cache.

### Step 3 — Engineer Steering Tags

Convert stage directions + character voice notes → TTS-2 steering tags using a mapping table:

| Stage Direction | Steering Tag |
|----------------|-------------|
| `(laughs)` | `[light laugh, speak warmly, like you're recalling a funny moment]` |
| `(skeptical)` | `[speak sharply, skeptical, like you know you're right]` |
| `(slowly)` | `[speak slowly, genuinely curious, soft voice]` |
| `(long pause)` | `[pause, then speak deliberately]` |
| `(interrupting)` | `[speak quickly, cutting in, sharp tone]` |
| `(defensive)` | `[speak defensively, slightly raised voice, like you're protecting yourself]` |
| `(softly)` | `[speak softly, almost a whisper, gentle tone]` |
| `(excited)` | `[speak excitedly, bright and energetic]` |
| `(confused)` | `[speak slowly, hesitant, like you're trying to understand]` |

**Tag placement rules:**
1. Tag goes BEFORE the line it applies to: `[tag] Line text.`
2. Tags apply forward until next tag or end of line
3. Maximum 1-2 tags per line (prevents over-direction)
4. For lines with NO stage direction, apply the character's baseline voice direction from voice notes

**Steering tag recipe for each character (baseline, used on un-tagged lines):**

| Character | Baseline tag |
|-----------|-------------|
| Cherry | `[speak thoughtfully, measured pace, like you're thinking as you talk]` |
| Marcia | `[speak warmly, casual and playful, like chatting with close friends]` |
| Brenda | `[speak sharply, defensive edge, quick pace]` |
| Linda | `[speak softly, genuine curiosity, gentle voice]` |

**Example conversion:**

Input:
```
**Marcia:** (laughs) He did. Ponyboy. He was so quiet I thought he was scared, but he wasn't. He was watching everything.
```

Output (text sent to TTS):
```
[light laugh, speak warmly, like you're recalling a funny moment] He did. Ponyboy. He was so quiet I thought he was scared, but he wasn't. He was watching everything.
```

### Step 4 — Generate Per-Line Audio

Call Inworld TTS-2 API for each line with the character's voice ID and engineered steering tag:

```python
import os, requests, base64

API_KEY = os.environ["INWORLD_API_KEY"]
LINE_DIR = "output/dialogs/20260624-after-the-drive-in/lines/"

def generate_line(voice_id, text_with_tags, filename):
    r = requests.post(
        "https://api.inworld.ai/tts/v1/voice",
        headers={
            "Authorization": f"Basic {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "text": text_with_tags,
            "voice_id": voice_id,
            "model_id": "inworld-tts-2",
            "audio_config": {
                "audio_encoding": "MP3",
                "sample_rate_hertz": 24000
            }
        }
    )
    audio_bytes = base64.b64decode(r.json()["audioContent"])
    with open(f"{LINE_DIR}{filename}", "wb") as f:
        f.write(audio_bytes)
    return f"{LINE_DIR}{filename}"

# Per-line generation
for i, turn in enumerate(dialog["turns"]):
    voice_id = character_voices[turn["character"]]
    tags = build_steering_tags(turn)
    text = tags + " " + turn["line"]
    generate_line(voice_id, text, f"line_{i:03d}.mp3")
```

**File naming:** `line_001.mp3`, `line_002.mp3`, ... — deterministic ordering for ffmpeg concat.

### Step 5 — Validate (Optional but Recommended)

Play back each line individually to verify:
1. Steering tags produce the intended emotion
2. No robotic delivery (≥3 tags = over-direction)
3. Punctuation creates natural pauses
4. Character voices are distinct

**Rejection criteria:** Re-generate any line that sounds flat, robotic, or mismatched to character.

### Step 6 — Stitch with FFmpeg

Two concatenation strategies, depending on desired pacing:

**Strategy A: Tight dialog (fast-paced argument scenes)**
Use the concat demuxer with minimal gap trimming:

```python
# Build concat file
with open("concat.txt", "w") as f:
    for i in range(len(turns)):
        f.write(f"file 'lines/line_{i:03d}.mp3'\n")
        if i > 0:
            f.write("inpoint 0.02\n")  # trim MP3 encoder priming gap

# Stitch
subprocess.run([
    "ffmpeg", "-f", "concat", "-safe", "0",
    "-i", "concat.txt", "-c", "copy",
    f"output/dialogs/{date}-{topic}.mp3"
])
```

**Strategy B: Natural pacing (thoughtful, conversational scenes)**
Insert silence padding between turns:

```python
# Generate silence clips of varying duration
silence_short = 0.15  # quick reply
silence_medium = 0.30  # thinking pause
silence_long = 0.50   # dramatic beat

# Build concat with silence files
with open("concat.txt", "w") as f:
    for i, turn in enumerate(turns):
        f.write(f"file 'lines/line_{i:03d}.mp3'\n")
        if i < len(turns) - 1:
            gap = get_gap_duration(turn, turns[i+1])
            f.write(f"file 'silence/silence_{gap*1000:.0f}ms.mp3'\n")
```

**Gap duration rules:**
| Context | Gap |
|---------|-----|
| Same character, continuing thought | 150ms |
| Turn-taking between characters | 300ms |
| After dramatic statement / `(long pause)` | 500ms |
| Before interruption `(interrupting)` | 50ms (barely any gap) |

**Pre-generate silence files:**
```bash
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 0.15 silence_150ms.mp3
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 0.30 silence_300ms.mp3
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 0.50 silence_500ms.mp3
```

### Step 7 — Output

Final file: `output/dialogs/{YYYYMMDD}-{topic-slug}.mp3`

Confirm path to user. Offer post-processing (volume normalization, EQ, speed adjustment) using the same ffmpeg filters from `build-a-monolog`.

---

## Voice Design: Oklahoma 16-Year-Old Female Characters

Since the target demographic (16-year-old girls from urban Oklahoma) lacks a direct Inworld system voice, we design bespoke voices:

```python
# scripts/design_voices.py

def design_oklahoma_teen_female(name, tone, pacing, quality):
    prompt = (
        f"A 16-year-old female voice from urban Oklahoma, {tone}. "
        f"{pacing}. {quality}. "
        f"Natural conversational delivery with a subtle Southern American accent. "
        f"Perfect broadcast quality audio."
    )
    # Must be 30-250 chars for Portal, 30-1000 for API
    # Validate length before sending
    assert 30 <= len(prompt) <= 1000, f"Prompt too long: {len(prompt)} chars"
    return prompt

cherry_prompt = design_oklahoma_teen_female(
    "Cherry",
    "thoughtful and questioning",
    "She speaks in measured full sentences, thinking as she talks",
    "Her voice carries quiet authority — she has changed tonight"
)
# Result: "A 16-year-old female voice from urban Oklahoma, thoughtful and questioning.
#  She speaks in measured full sentences, thinking as she talks.
#  Her voice carries quiet authority — she has changed tonight.
#  Natural conversational delivery with a subtle Southern American accent.
#  Perfect broadcast quality audio."
```

**Character voice designs:**

| Character | Design prompt essence |
|-----------|----------------------|
| Cherry | thoughtful, questioning, measured full sentences, quiet authority |
| Marcia | playful, warm, loyal, casual and quick, speaks from feeling |
| Brenda | sharp, defensive, interrupts, quick pace, scared underneath |
| Linda | soft, genuinely curious, gentle, asks questions, doesn't take sides |

---

## Test Case: Teacher Demo Model

**Input:** `output/M3-LESSON02-DRAMA/lesson.md` lines 130-169

**Expected flow:**
1. Parse → 4 characters, 15 turns
2. Design → 4 voice IDs (or use prebuilt closest match for MVP)
3. Generate → 15 mp3 files
4. Stitch → single mp3, ~2-3 minutes
5. Cost → fits within Inworld free tier (40 min/month)

**Success criteria:**
- 4 distinct character voices
- Steering tags produce audible emotion shifts
- Natural turn-taking pacing (150-300ms gaps)
- No robotic artifacts, no ".." pauses, no non-verbal glitches

---

## Script Specifications

### `scripts/parse_dialog.py`
- Input: Markdown file path or inline text
- Parse: Character table → `{name, voice_notes, key_line}`
- Parse: Dialog body → `[{character, stage_direction?, line}]`
- Output: JSON to stdout or file
- Dependencies: stdlib only (regex)

### `scripts/design_voices.py`
- Input: JSON character array with `voice_notes`
- Output: Map `character_name → voice_id`
- Calls Inworld Voice Design API
- Caches results in `character_voices.json`
- Check cache before designing new voices

### `scripts/generate_lines.py`
- Input: Dialog JSON + voice map
- Output: Per-line MP3 files in `lines/` directory
- Calls Inworld TTS API with steering tags
- Retry on API error (3 attempts with backoff)

### `scripts/stitch_dialog.py`
- Input: Directory of line MP3s + turn metadata
- Output: Single MP3
- Builds concat file with gap padding
- Runs ffmpeg concat demuxer

---

## Cost Estimate

| Stage | Calls | Cost |
|-------|-------|------|
| Voice design (4 characters, one-time) | 4 × design + 4 × publish = 8 API calls | Free tier (no per-call charge) |
| TTS generation (15 lines) | 15 API calls | ~2-3 min audio → fits free tier (40 min/mo) |
| FFmpeg (local) | 1 command | $0 |
| **Total (first dialog)** | 24 API calls | **$0** (free tier) |
| **Subsequent dialogs with same characters** | 15 TTS calls | **$0** (voice IDs cached) |

---

## Open Design Questions

1. **MVP prebuilt voices?** For first test, use the closest Inworld system voices (e.g., "Ashley" for Cherry, "Jessica" for Marcia) with steering tags to imply the Oklahoma accent. Design bespoke voices only if the quality is insufficient.

2. **Silence padding vs. crossfade?** The concat demuxer with silence files is simpler and more predictable. Crossfade (`acrossfade=d=0.05`) would sound smoother but requires re-encoding. MVP: concat with silence files.

3. **Output directory:** `output/dialogs/` — must be created. Same pattern as `build-a-monolog`'s `output/monologs/`.

4. **Dialog format extensibility:** Should the parser also handle inline dialog formats like `Cherry: text here` without bold markers? Yes — the parser should be format-tolerant.
