import json
import os
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API_KEY = os.environ.get("INWORLD_API_KEY")
if not API_KEY:
    print("ERROR: INWORLD_API_KEY environment variable not set")
    sys.exit(1)

AUTH_HEADER = f"Basic {API_KEY}"

design_prompt = (
    "An articulate, professionally-trained female voice with an educated "
    "New York accent, mid-thirties. Warm and sunny tone; lively, natural "
    "pacing; perfect syllable stress and sound articulation. "
    "Perfect broadcast quality audio."
)

preview_text = "Can you recognize faces that you have only seen once? Let us find out."

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

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "..", "config", "tts_vocab_voice.json")
config_path = os.path.normpath(config_path)
os.makedirs(os.path.dirname(config_path), exist_ok=True)
config = {"voice_id": voice_id, "description": design_prompt}
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
print(f"  Saved to {config_path}")
print("Done - voice is ready for vocabulary TTS generation.")
