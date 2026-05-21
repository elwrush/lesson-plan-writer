---
description: Run ruff linting and formatting on the project. Check for code quality issues, auto-fix where possible, and format Python files.
---
# Command: Lint

## Usage
Invoke this command to run ruff linting and formatting on the project.

## What it does

1. **Encoding check** — `python scripts/check_encoding.py` — verifies all text files are valid UTF-8. Run with `--fix` to auto-convert cp1252-encoded files
2. **Unicode check/cross scan** — `python scripts/check_unicode_symbols.py` — scans all HTML files for raw Unicode check (U+2713) and cross (U+2717) characters. These must be replaced with Font Awesome icons `<i class="fa-solid fa-check">` and `<i class="fa-solid fa-times">`. Run with `--fix` to auto-replace.
3. **Pedagogical intent check** — `python scripts/check_pedagogical_intent.py --project <slides-dir>` — verifies every non-exempt slide has mandatory `<!-- PEDAGOGICAL INTENT: -->` and `<!-- WHY THIS FEATURE: -->` annotations. New builds should pass; existing slides may fail until annotated.
4. **Check + fix** — `python -m ruff check --fix .` — finds lint violations and auto-fixes them
5. **Format** — `python -m ruff format .` — formats all Python files per ruff's style

## When to use

Run this before committing changes (replaces the pre-commit hook that was previously used). No background process, no git lock contention — just manual on-demand linting.

## Commands

```powershell
# Check encoding first
python scripts/check_encoding.py ; if ($?) { python -m ruff check --fix . }

# Unicode check/cross scan (prevents raw Unicode check/cross in HTML files)
python scripts/check_unicode_symbols.py

# Fix any found (safe to always run — no-op if clean)
python scripts/check_unicode_symbols.py --fix

# Pedagogical intent check
python scripts/check_pedagogical_intent.py --project "output/{subfolder}/slides/"

# Format (separate step, safe to always run)
python -m ruff format .
```

Or run all five in sequence:

```powershell
python scripts/check_encoding.py ; if ($?) { python scripts/check_unicode_symbols.py --fix ; python scripts/check_pedagogical_intent.py ; if ($?) { python -m ruff check --fix . ; python -m ruff format . } }

## Also available

To run pre-commit on all files without committing:

```powershell
python -m pre_commit run --all-files
```

Run all tests:

```powershell
python -m pytest tests/ -v
```