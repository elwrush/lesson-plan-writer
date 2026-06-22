"""
check_overflow.py — Detect slides with content extending beyond viewport.

Uses Playwright to render each slide in a headless Chromium browser and checks
whether any child element exceeds the slide's bounding box. Catches visual
overflow that design linters and structural validators cannot detect.

Usage:
    python scripts/check_overflow.py --project output/subfolder/slides/

Dependencies:
    pip install playwright
    playwright install chromium

Exit codes:
    0 — all slides fit within viewport
    1 — overflow detected on at least one slide
    2 — tool error (browser unavailable, timeout, etc.)
"""

import argparse
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


def _start_server(directory: Path, port: int) -> HTTPServer:
    """Start a local HTTP server serving the slides directory."""

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, _format, *args):
            pass  # suppress server log output

    server = HTTPServer(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def _find_free_port() -> int:
    """Return a free TCP port on localhost."""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def check_overflow(project_dir: Path) -> list[dict]:
    """Check every slide for overflow. Returns list of overflow issues."""
    from playwright.sync_api import sync_playwright

    index_html = project_dir / "index.html"
    if not index_html.exists():
        print(f"error: index.html not found at {index_html}", file=sys.stderr)
        sys.exit(2)

    port = _find_free_port()
    server = _start_server(project_dir, port)
    url = f"http://127.0.0.1:{port}/index.html"

    results = []

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                no_viewport=False,
            )
            page = context.new_page()

            # Suppress console errors from reveal.js (CDN warnings, etc.)
            page.on("console", lambda msg: None)

            # Navigate and wait for reveal.js to initialize
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
            except Exception as e:
                print(f"error: failed to load {url}: {e}", file=sys.stderr)
                browser.close()
                sys.exit(2)

            # Wait for reveal.js to be ready
            try:
                page.wait_for_function(
                    "typeof Reveal !== 'undefined' && Reveal.isReady()",
                    timeout=15000,
                )
            except Exception:
                print(
                    "error: reveal.js did not initialize within 15s — check for JS errors in console",
                    file=sys.stderr,
                )
                browser.close()
                sys.exit(2)

            # Get total slide count
            total = page.evaluate("Reveal.getTotalSlides()")
            if not total or total < 1:
                print("error: no slides found in presentation", file=sys.stderr)
                browser.close()
                sys.exit(2)

            for i in range(total):
                # Navigate to slide
                page.evaluate(f"Reveal.slide({i})")
                page.wait_for_timeout(400)  # wait for auto-animate + transitions

                # Reveal all fragments on this slide (fragments hide content until revealed)
                page.evaluate("""
                    const slide = Reveal.getCurrentSlide();
                    if (slide) {
                        const fragments = slide.querySelectorAll('.fragment');
                        fragments.forEach(f => f.classList.add('visible'));
                    }
                """)

                # Check overflow in reveal.js logical coordinate system (1280x720).
                # Uses Reveal.getScale() to convert browser pixel coords back to logical coords.
                overflow = page.evaluate(f"""() => {{
                    const scale = Reveal.getScale();
                    const slideEl = Reveal.getSlides()[{i}];
                    if (!slideEl) return null;
                    const slideRect = slideEl.getBoundingClientRect();

                    const issues = [];

                    function checkNode(el) {{
                        if (el === slideEl) return;
                        if (el.tagName === 'SCRIPT') return;
                        if (el.tagName === 'ASIDE' && el.classList.contains('notes')) return;
                        if (el.classList.contains('slide-background')) return;

                        const rect = el.getBoundingClientRect();

                        // Skip zero-size elements
                        if (rect.width === 0 && rect.height === 0) return;

                        // Convert to slide-local logical coordinates
                        const logicalBottom = (rect.bottom - slideRect.top) / scale;
                        const logicalRight = (rect.right - slideRect.left) / scale;

                        if (logicalBottom > 720 + 4) {{  // 4px tolerance
                            issues.push({{
                                tag: el.tagName,
                                id: el.id || '',
                                cls: (el.className && typeof el.className === 'string') ? el.className.slice(0, 60) : '',
                                text: (el.textContent || '').trim().slice(0, 80),
                                dir: 'bottom',
                                px: Math.round(logicalBottom - 720),
                            }});
                        }}
                        if (logicalRight > 1280 + 4) {{
                            issues.push({{
                                tag: el.tagName,
                                id: el.id || '',
                                cls: (el.className && typeof el.className === 'string') ? el.className.slice(0, 60) : '',
                                text: (el.textContent || '').trim().slice(0, 80),
                                dir: 'right',
                                px: Math.round(logicalRight - 1280),
                            }});
                        }}

                        // Recurse into children
                        for (const child of el.children) {{
                            checkNode(child);
                        }}
                    }}

                    for (const child of slideEl.children) {{
                        checkNode(child);
                    }}

                    return issues;
                }}""")

                if overflow:
                    for issue in overflow:
                        tag = issue["tag"]
                        el_id = issue["id"]
                        el_cls = issue["cls"]
                        el_text = issue["text"]
                        direction = issue["dir"]
                        pixels = issue["px"]
                        loc = f"#{el_id}" if el_id else (f".{el_cls}" if el_cls else f"<{tag}>")
                        summary = f"  Slide {i}: {loc} overflows {direction} by {pixels}px"
                        if el_text:
                            summary += f' — "{el_text}"'
                        results.append(summary)

            browser.close()

    finally:
        server.shutdown()

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Detect slides with content overflowing the viewport."
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Path to slides directory containing index.html",
    )

    args = parser.parse_args()
    project_dir = Path(args.project).resolve()

    if not project_dir.is_dir():
        print(f"error: directory not found: {project_dir}", file=sys.stderr)
        sys.exit(2)

    issues = check_overflow(project_dir)

    if issues:
        print(f"\n{'=' * 60}")
        print(f"OVERFLOW DETECTED — {len(issues)} issue(s)")
        print(f"{'=' * 60}")
        for issue in issues:
            print(issue)
        print()
        sys.exit(1)
    else:
        print("OK — all slides fit within viewport.")
        sys.exit(0)


if __name__ == "__main__":
    main()
