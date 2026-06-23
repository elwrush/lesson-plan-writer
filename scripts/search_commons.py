#!/usr/bin/env python3
"""
search_commons.py — Search and download images from Wikimedia Commons.

Usage:
    python search_commons.py --query "teenagers smartphone" --count 3 --output slides/assets/ --aspect landscape

Parameters:
    --query      Search term (required)
    --count      Number of images to download (default: 3, max: 10)
    --output     Output directory (default: .)
    --min-width  Minimum image width in pixels (default: 800)
    --aspect     Aspect ratio preference: landscape (default), portrait, any

Output: JSON with downloaded files, attribution, and source URLs.
"""

import json
import sys
import time
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

API_URL = "https://commons.wikimedia.org/w/api.php"
HEADERS = {
    "User-Agent": "LessonPlanWriter3/1.0 (https://github.com/elwrush/lesson-plan-writer-3) requests/2.32"
}
ASPECT_CONFIG = {
    "landscape": {"target": 1.78, "min_ratio": 1.3, "max_ratio": 2.5},
    "portrait": {"target": 0.75, "min_ratio": 0.3, "max_ratio": 0.9},
    "any": {"target": None, "min_ratio": 0.0, "max_ratio": 100.0},
}


def api_get(params, retries=3):
    """Make an API request with retry and backoff on 429."""
    for attempt in range(retries):
        r = requests.get(API_URL, params=params, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 429:
            retry_after = int(r.headers.get("Retry-After", 5))
            print(f"  Rate limited. Waiting {retry_after}s...", file=sys.stderr)
            time.sleep(retry_after)
            continue
        else:
            r.raise_for_status()
    raise RuntimeError(f"API request failed after {retries} retries (last status: {r.status_code})")


def search_images(query, count=3, min_width=800, aspect="landscape"):
    """Search Commons for images matching query. Returns list of matching image dicts."""
    cfg = ASPECT_CONFIG.get(aspect, ASPECT_CONFIG["landscape"])

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srnamespace": 6,
        "srsearch": query,
        "srlimit": count * 5,
    }
    data = api_get(params)
    results = data.get("query", {}).get("search", [])
    if not results:
        return []

    hits = []
    for hit in results:
        title = hit["title"]
        if any(
            title.lower().endswith(ext)
            for ext in (".ogg", ".ogv", ".pdf", ".svg", ".webm", ".mp3", ".wav")
        ):
            continue

        params2 = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|dimensions|mime",
        }
        data2 = api_get(params2)
        for page_id, page in data2.get("query", {}).get("pages", {}).items():
            info = page.get("imageinfo", [{}])[0]
            mime = info.get("mime", "")
            if mime not in ("image/jpeg", "image/png", "image/webp"):
                continue
            if info.get("width", 0) < min_width:
                continue
            w = info.get("width", 1)
            h = info.get("height", 1)
            ratio = w / h
            if ratio < cfg["min_ratio"] or ratio > cfg["max_ratio"]:
                continue

            author = "Unknown"
            try:
                author = info.get("extmetadata", {}).get("Artist", {}).get("value", "Unknown")
            except Exception:
                pass
            license_name = "Unknown"
            try:
                license_name = (
                    info.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "Unknown")
                )
            except Exception:
                pass

            hits.append(
                {
                    "title": page["title"],
                    "url": info["url"],
                    "thumb_url": info.get("thumburl", info["url"]),
                    "width": w,
                    "height": h,
                    "ratio": round(ratio, 2),
                    "author": author,
                    "license": license_name,
                    "source_url": f"https://commons.wikimedia.org/wiki/{page['title'].replace(' ', '_')}",
                }
            )
            break

        time.sleep(0.5)  # Be polite between API calls

    if cfg["target"] is not None:
        hits.sort(key=lambda h: abs(h["ratio"] - cfg["target"]))
    else:
        hits.sort(key=lambda h: h["ratio"], reverse=True)

    return hits[:count]


def download_and_compress(url, output_path):
    """Download an image, compress it, and save to output_path."""
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    img = Image.open(BytesIO(r.content))
    img.thumbnail((1920, 1920), Image.LANCZOS)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output_path, "JPEG", quality=80, optimize=True)
    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Search and download images from Wikimedia Commons"
    )
    parser.add_argument("--query", required=True, help="Search term")
    parser.add_argument(
        "--count", type=int, default=3, help="Number of images (default: 3, max: 10)"
    )
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--min-width", type=int, default=800, help="Minimum image width")
    parser.add_argument(
        "--aspect",
        choices=["landscape", "portrait", "any"],
        default="landscape",
        help="Aspect ratio preference",
    )
    args = parser.parse_args()
    args.count = min(args.count, 10)

    hits = search_images(args.query, args.count, args.min_width, args.aspect)
    result = {"files": [], "errors": []}

    for i, hit in enumerate(hits):
        filename = f"commons_{i + 1}.jpg"
        out_path = Path(args.output) / filename
        try:
            download_and_compress(hit["url"], out_path)
            result["files"].append(
                {
                    "path": str(out_path),
                    "filename": filename,
                    "width": hit["width"],
                    "height": hit["height"],
                    "ratio": hit["ratio"],
                    "attribution": f"{hit['author']} ({hit['license']})",
                    "source_url": hit["source_url"],
                }
            )
            print(f"  Downloaded: {filename} ({hit['width']}x{hit['height']})", file=sys.stderr)
        except Exception as e:
            result["errors"].append({"url": hit["url"], "error": str(e)})
            print(f"  Failed: {filename} - {e}", file=sys.stderr)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
