"""
Encoding checker: scan project files for UTF-8 validity.
Auto-fixes files that were incorrectly saved as cp1252.
Part of the /lint command workflow.
"""

import os
import sys

# Force UTF-8 for all I/O in this script
sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# File extensions to check
EXTENSIONS = {
    ".md",
    ".html",
    ".py",
    ".json",
    ".css",
    ".js",
    ".typ",
    ".txt",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
}

# Directories to skip
SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".image-cache", ".local", ".kilo", "venv"}


def check_and_fix(fix: bool = False) -> tuple:
    """Walk project files and return list of issues found/fixed."""
    issues = []
    fixes = []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip unwanted dirs
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in EXTENSIONS:
                continue
            fpath = os.path.join(root, fname)

            # Try reading as UTF-8
            try:
                with open(fpath, encoding="utf-8") as f:
                    f.read()
                # No issue
            except UnicodeDecodeError:
                # Try cp1252 -> convert to UTF-8
                try:
                    with open(fpath, encoding="cp1252") as f:
                        content = f.read()
                    # File is cp1252-encoded text, not UTF-8
                    issues.append(fpath)
                    if fix:
                        with open(fpath, "w", encoding="utf-8") as f:
                            f.write(content)
                        fixes.append(fpath)
                except Exception:
                    issues.append(f"{fpath} (encoding unknown, not cp1252)")

    return issues, fixes


def main():
    issues, fixes = check_and_fix(fix=False)

    if not issues:
        print("✓ All text files are valid UTF-8.")
        return 0

    print(f"\nFound {len(issues)} file(s) with encoding issues:")
    for f in issues:
        print(f"  {f}")

    print("\nRun with --fix to auto-convert cp1252 files to UTF-8:")
    print("  python scripts/check_encoding.py --fix")
    return 1


if __name__ == "__main__":
    fix_mode = "--fix" in sys.argv
    if fix_mode:
        issues, fixes = check_and_fix(fix=True)
        if not issues:
            print("✓ All text files are valid UTF-8.")
        else:
            print(f"Fixed {len(fixes)} file(s):")
            for f in fixes:
                print(f"  {f}")
            if len(fixes) < len(issues):
                print(f"Could not fix {len(issues) - len(fixes)} file(s) (unknown encoding).")
    else:
        sys.exit(main())
