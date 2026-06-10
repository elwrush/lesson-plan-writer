# Command: get-YouTube-transcript

## Usage
`/get-youtube-transcript VIDEO_ID [--output FILE] [--segment START-END]`

## What it does
Fetches a timestamped transcript from a YouTube video using the `youtube-transcript-api` Python library. Outputs lines in `[MM:SS] text` format.

## Arguments
- `VIDEO_ID` — Required. The YouTube video ID (e.g., `qkX5CPXzjxs`), NOT the full URL
- `--output`, `-o` — Optional file path to save the transcript. Default: stdout
- `--segment`, `-s` — Optional time range in seconds: `START-END` (e.g., `0-150`)
- `--lang`, `-l` — Language code (default: `en`)

## Examples
```powershell
python scripts/get_youtube_transcript.py qkX5CPXzjxs
python scripts/get_youtube_transcript.py qkX5CPXzjxs --output transcript_timed.txt
python scripts/get_youtube_transcript.py qkX5CPXzjxs --segment 0-150
```

## Script
`scripts/get_youtube_transcript.py`

## Dependencies
- `youtube-transcript-api` (installed globally via pip)
