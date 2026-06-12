"""
typst_check.py — Validate Typst syntax via typst compile without producing output.

Usage:
    python scripts/typst_check.py <file.typ>              # validate a file
    python scripts/typst_check.py <file.typ> --json       # JSON output for agent consumption
    python scripts/typst_check.py -                       # read Typst from stdin
    echo "#table(...)" | python scripts/typst_check.py -  # pipe Typst to validate

The script compiles the Typst source to a temporary PDF, captures errors,
and reports success/failure. The temp PDF is deleted after validation.

Exit codes:
    0 — compilation succeeded (valid Typst)
    1 — compilation failed (syntax/layout errors)
    2 — input error (file not found, stdin empty, typst CLI missing)
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Roboto font directory (optional — Typst uses fallback fonts if missing)
ROBOTO_FONT_DIR = Path(
    os.path.expandvars(r"%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto")
)


def _has_font_path() -> bool:
    """Check if the Roboto font directory exists."""
    return ROBOTO_FONT_DIR.exists()


def _minimal_wrapper(source: str) -> str:
    """Wrap a bare snippet in minimal Typst boilerplate so it compiles standalone.

    If the source already starts with a known document-level directive
    (#set, #import, #show, = heading, etc.), return it unchanged.
    Otherwise wrap it in #set page + #set text so inline content renders.
    """
    stripped = source.strip()
    if not stripped:
        return source

    # If it already looks like a complete document, don't wrap
    doc_starters = ("#set", "#import", "#show", "#let", "=", "//", "/*", "#[")
    for starter in doc_starters:
        if stripped.startswith(starter):
            return source

    # Wrap bare content (e.g. "#table(...)" or plain text) in a minimal document
    return (
        "#set page(width: auto, height: auto, margin: 0.5in)\n"
        '#set text(size: 10pt, font: "Roboto", fallback: true)\n' + source
    )


def validate(source: str, use_fonts: bool = True) -> dict:
    """Compile Typst source to a temp PDF and return structured result.

    Args:
        source: Typst source code
        use_fonts: If True and ROBOTO_FONT_DIR exists, pass --font-path

    Returns:
        dict with keys: success (bool), exit_code (int), stdout, stderr
    """
    # Wrap bare content in minimal document
    wrapped = _minimal_wrapper(source)

    # Write to temp file
    typ_path = None
    pdf_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".typ", encoding="utf-8", delete=False
        ) as f:
            f.write(wrapped)
            typ_path = f.name

        pdf_fd, pdf_path = tempfile.mkstemp(suffix=".pdf")
        os.close(pdf_fd)

        cmd = ["typst", "compile", typ_path, pdf_path]

        if use_fonts and _has_font_path():
            cmd.extend(["--font-path", str(ROBOTO_FONT_DIR)])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )

        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "Compilation timed out after 60 seconds.",
        }
    except FileNotFoundError:
        return {
            "success": False,
            "exit_code": -2,
            "stdout": "",
            "stderr": (
                "typst CLI not found. Install from https://github.com/typst/typst "
                "or ensure typst is in PATH."
            ),
        }
    finally:
        # Clean up temp files
        if typ_path:
            try:
                os.unlink(typ_path)
            except OSError:
                pass
        if pdf_path:
            try:
                os.unlink(pdf_path)
            except OSError:
                pass


def _extract_errors(stderr: str) -> list[dict]:
    """Parse typst compile stderr into structured error objects.

    Typst error format:
        error: expected content, found array
          ┌─ :3:5
          │
        3 │   []
          │    ^^

    Returns list of dicts with: line, column, message, context
    """
    errors = []
    if not stderr:
        return errors

    lines = stderr.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        # Match error/warning line
        if line.startswith("error:") or line.startswith("warning:"):
            severity = "error" if line.startswith("error:") else "warning"
            message = line.split(":", 1)[1].strip() if ":" in line else line

            # Look ahead for line/column location
            location = None
            context_lines = []
            j = i + 1
            while j < len(lines) and j < i + 10:
                next_line = lines[j]
                if "─┐" in next_line or "─┘" in next_line:
                    break
                if "─┬" in next_line or "─┴" in next_line:
                    break
                if "──" in next_line:
                    # Location line: "  ┌─ :3:5"
                    # or "  ┌─ <path>:3:5"
                    import re

                    m = re.search(r"[:](\\d+):(\\d+)", next_line)
                    if m:
                        location = {"line": int(m.group(1)), "column": int(m.group(2))}
                elif next_line.strip().startswith("│"):
                    # Context line
                    ctx = next_line.strip()
                    # Remove the │ prefix
                    if ctx.startswith("│"):
                        ctx = ctx[1:].strip()
                    if ctx:
                        context_lines.append(ctx)
                j += 1

            errors.append(
                {
                    "severity": severity,
                    "message": message,
                    "line": location["line"] if location else None,
                    "column": location["column"] if location else None,
                    "context": context_lines,
                }
            )
            i = j
        else:
            i += 1

    return errors


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate Typst syntax via typst compile.")
    parser.add_argument(
        "input",
        nargs="?",
        help="Path to .typ file, or '-' to read from stdin",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON (default for agent consumption)",
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Output human-readable text (overrides --json)",
    )
    parser.add_argument(
        "--no-fonts",
        action="store_true",
        help="Do not pass --font-path to typst (use system fallback fonts)",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Do not wrap bare content in minimal document boilerplate",
    )

    args = parser.parse_args()

    # Read source
    if args.input is None or args.input == "-":
        source = sys.stdin.read()
        if not source.strip():
            print("error: no Typst source provided via stdin", file=sys.stderr)
            sys.exit(2)
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"error: file not found: {args.input}", file=sys.stderr)
            sys.exit(2)
        source = input_path.read_text(encoding="utf-8")

    # Validate
    result = validate(source, use_fonts=not args.no_fonts)

    # Parse structured errors
    if not result["success"]:
        result["errors"] = _extract_errors(result["stderr"])
    else:
        result["errors"] = []

    # Output
    if args.text:
        _print_text(result)
    else:
        # Default: JSON output
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")

    sys.exit(0 if result["success"] else 1)


def _print_text(result: dict):
    """Human-readable output."""
    if result["success"]:
        print("OK — Typst compilation succeeded.")
        return

    print(f"FAILED (exit code {result['exit_code']})")
    if result["stderr"]:
        print(result["stderr"])

    errors = result.get("errors", [])
    if errors:
        print(f"\n{len(errors)} error(s) parsed:")
        for i, err in enumerate(errors, 1):
            line_info = f"line {err['line']}" if err.get("line") else "unknown line"
            print(f"  {i}. [{err['severity']}] {line_info}: {err['message']}")


if __name__ == "__main__":
    main()
