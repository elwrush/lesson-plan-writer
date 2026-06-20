"""
Fetch a timestamped transcript from a YouTube video.

Usage:
    python scripts/get_youtube_transcript.py VIDEO_ID [--output FILE] [--segment START-END]

Examples:
    python scripts/get_youtube_transcript.py qkX5CPXzjxs
    python scripts/get_youtube_transcript.py qkX5CPXzjxs --output transcript_timed.txt
    python scripts/get_youtube_transcript.py qkX5CPXzjxs --segment 0-150
"""

import argparse
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("ERROR: Install youtube-transcript-api: pip install youtube-transcript-api")
    sys.exit(1)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT-style timestamp: MM:SS or H:MM:SS."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def format_output(transcript: list) -> str:
    """Format snippet objects as timestamped lines."""
    lines = []
    for snippet in transcript:
        ts = format_timestamp(snippet.start)
        format_timestamp(snippet.duration)
        text = snippet.text.strip()
        lines.append(f"[{ts}] {text}")
    return "\n".join(lines)


def filter_by_segment(transcript: list, start_sec: float, end_sec: float) -> list:
    """Filter transcript entries between start and end timestamps."""
    return [s for s in transcript if s.start >= start_sec and s.start + s.duration <= end_sec]


def main():
    parser = argparse.ArgumentParser(description="Fetch timestamped YouTube transcript")
    parser.add_argument("video_id", help="YouTube video ID (e.g., qkX5CPXzjxs)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--segment", "-s", help="Time range: START-END in seconds (e.g., 0-150)")
    parser.add_argument("--lang", "-l", default="en", help="Language code (default: en)")

    args = parser.parse_args()

    try:
        api = YouTubeTranscriptApi()
        fetched = api.fetch(args.video_id, languages=[args.lang])
        transcript = fetched.snippets
    except Exception as e:
        print(f"ERROR fetching transcript: {e}", file=sys.stderr)
        sys.exit(1)

    if args.segment:
        try:
            parts = args.segment.split("-")
            start_s = float(parts[0])
            end_s = float(parts[1])
            transcript = filter_by_segment(transcript, start_s, end_s)
        except (ValueError, IndexError):
            print("ERROR: --segment must be in format START-END (e.g., 0-150)", file=sys.stderr)
            sys.exit(1)

    output = format_output(transcript)

    if args.output:
        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Transcript written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
