import base64
import json
import os
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API_KEY = os.environ.get("INWORLD_API_KEY")
if not API_KEY:
    print("ERROR: INWORLD_API_KEY environment variable not set")
    sys.exit(1)


def load_voice_id():
    script_dir = Path(__file__).parent.resolve()
    config_path = script_dir.parent / "config" / "tts_vocab_voice.json"
    if not config_path.exists():
        print(f"ERROR: Voice config not found at {config_path}")
        print("Run scripts/design_tts_voice.py first.")
        sys.exit(1)
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)["voice_id"]


def generate_word_audio(word: str, voice_id: str, output_dir: Path) -> Path:
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

    filename = f"vocab-{word.lower().replace(' ', '-')}.mp3"
    out_path = output_dir / filename
    with open(out_path, "wb") as f:
        f.write(audio_bytes)
    print(f"  Generated: {filename} ({len(audio_bytes)} bytes)")
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate TTS audio clips for vocabulary words")
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
