#!/usr/bin/env python3
"""
serve_slides.py — Start HTTP server and open browser for reveal.js slides.

Usage:
    python scripts/serve_slides.py output/{subfolder}/slides/
    python scripts/serve_slides.py                           # serves from .
    python scripts/serve_slides.py --port 8080 output/{subfolder}/slides/

Opens the browser automatically. Keeps running until Ctrl+C.
"""

import argparse
import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Serve reveal.js slides and open browser")
    parser.add_argument(
        "directory", nargs="?", default=".", help="Slides directory (default: current dir)"
    )
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port number (default: 8000)")
    parser.add_argument(
        "--no-browser", action="store_true", help="Do not open browser automatically"
    )
    args = parser.parse_args()

    slides_dir = Path(args.directory).resolve()
    if not slides_dir.exists():
        print(f"Error: directory not found: {slides_dir}")
        sys.exit(1)

    # Change to the slides directory
    os.chdir(slides_dir)
    print(f"Serving: {slides_dir}")
    print(f"URL:     http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")

    # Open browser unless --no-browser
    if not args.no_browser:
        webbrowser.open(f"http://localhost:{args.port}/")

    # Start server
    server = HTTPServer(("", args.port), SimpleHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
