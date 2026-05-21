---
description: Run ruff linting and formatting on the project. Check for code quality issues, auto-fix where possible, and format Python files.
---
# Command: Lint

## Usage
Invoke this command to run ruff linting and formatting on the project.

## What it does

1. **Encoding check** — `python scripts/check_encoding.py` — verifies all text files are valid UTF-8. Run with `--fix` to auto-convert cp1252-encoded files
2. **Check + fix** — `python -m ruff check --fix .` — finds lint violations and auto-fixes them
3. **Format** — `python -m ruff format .` — formats all Python files per ruff's style

## When to use

Run this before committing changes (replaces the pre-commit hook that was previously used). No background process, no git lock contention — just manual on-demand linting.

## Commands

```powershell
# Check encoding first
python scripts/check_encoding.py ; if ($?) { python -m ruff check --fix . }

# Format (separate step, safe to always run)
python -m ruff format .
```

Or run all three in sequence:

```powershell
python scripts/check_encoding.py ; if ($?) { python -m ruff check --fix . ; python -m ruff format . }

## Also available

To run pre-commit on all files without committing:

```powershell
python -m pre_commit run --all-files
```

Run all tests:

```powershell
python -m pytest tests/ -v
```