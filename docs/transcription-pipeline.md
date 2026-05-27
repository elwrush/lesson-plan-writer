# Transcription Pipeline — AssemblyAI + DeepSeek Post-Processing

## Architecture

Two-stage pipeline optimized for ESL verbatim transcription:

```
Audio file → AssemblyAI (ASR) → raw transcript → DeepSeek V4 Flash → formatted transcript
                            ↓                           ↓
                    disfluencies: True            adds ... , [brackets]
                    preserves errors              keeps all errors verbatim
```

## Stage 1: AssemblyAI (ASR)

- **Model**: `universal-2`
- **Key flag**: `disfluencies: True` — preserves um, uh, er, repeated words, and non-standard grammar
- **Additional settings**: `format_text: False`, `punctuate: True`
- **API endpoint**: `POST https://api.assemblyai.com/v2/transcript`
- **API format**: OpenAI-compatible, direct REST
- **Auth**: AssemblyAI API key via `Authorization` header

### Word timestamps

AssemblyAI returns per-word confidence scores and timestamps. This enables:
- Gap analysis for pause detection (gaps > 1s between words indicate potential ellipsis insertion)
- Low-confidence word flagging (for manual review of potentially misheard ESL speech)

### Why AssemblyAI?

| Criterion | AssemblyAI | Deepgram Nova-2 | Gemini (Google) | GPT-4o-transcribe |
|-----------|-----------|----------------|-----------------|-------------------|
| Cost (50 min/mo) | $0.38 | $0.22 | ~$0.08 | $0.30 |
| Disfluencies flag | `disfluencies: True` | None | Via prompt only | Via prompt only |
| ESL verbatim | Best | Good | Best (prompt-following) | Poor (normalizes) |
| API signup | Pay-as-you-go | Pay-as-you-go | Tiered (nightmare) | Pay-as-you-go |
| Audio support | Native upload | Native upload | File API | Native upload |

AssemblyAI is the best non-Google option with an explicit `disfluencies` flag that doesn't rely on prompt engineering.

## Stage 2: DeepSeek V4 Flash (Post-Processing)

- **Model**: `deepseek-v4-flash`
- **Role**: Add formatting markers only — never correct grammar or word choice
- **Pricing**: $0.14/1M input, $0.28/1M output (cache miss), $0.0028/1M input (cache hit)
- **Cost per transcript**: ~$0.000027 (~50 words)
- **Monthly cost at 50 min**: ~$0.003

### Prompt template

```
You are a formatting assistant for ESL speech transcripts. Your ONLY job is to add formatting markers.

RULES:
1. NEVER change, correct, or improve the text — keep every word exactly as written
2. NEVER fix grammar, word choice, or spelling
3. Never add or remove words
4. Add ... for short pauses where the speaker hesitates
5. Add ...... for longer pauses/silences
6. Add [cough] [laugh] [sigh] [laughs] [coughs] for non-verbal sounds
7. Add [inaudible] for unclear words
8. Keep filler words (um, uh, er, hmm) exactly as written
9. If words are repeated (e.g. "I not I not"), keep the repetition

Input: {raw_assemblyai_transcript}

Return only the formatted transcript with no explanation.
```

### DeepSeek API

- Base URL: `https://api.deepseek.com`
- OpenAI-compatible (same SDK)
- Sign up: `platform.deepseek.com`

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...", base_url="https://api.deepseek.com")
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
)
formatted = response.choices[0].message.content
```

## Total Monthly Cost (50 min / ~10K words)

| Stage | Cost |
|-------|------|
| AssemblyAI (Universal-2, 50 min) | $0.38 |
| DeepSeek V4 Flash (post-process) | ~$0.003 |
| **Total** | **~$0.38** |

## Integration Notes

### Environment variables

| Variable | Source |
|----------|--------|
| `ASSEMBLYAI_API_KEY` | System environment (User scope) |
| `DEEPSEEK_API_KEY` | System environment (User scope) — sign up at platform.deepseek.com |

### AssemblyAI upload to transcript flow

1. `POST /v2/upload` — upload raw audio bytes
2. `POST /v2/transcript` — submit with `disfluencies: True`
3. Poll `GET /v2/transcript/{id}` until `status == "completed"`
4. Extract `text` from response JSON

### DeepSeek formatting flow

1. Send AssemblyAI `text` output to DeepSeek V4 Flash with the formatting prompt
2. Return the formatted transcript

## Known Limitations

- DeepSeek V4 Flash is text-only — no audio input, no vision
- AssemblyAI's `disfluencies` flag preserves filler words (um, uh, er) as words, not as ellipsis markers — ellipsis insertion is the post-processing step's job
- Both services are pay-as-you-go with no monthly minimum

## TTS & Voice Design (Separate Pipeline)

For TTS and voice cloning see `@agents/tts-pipeline` (WIP — not yet implemented).
