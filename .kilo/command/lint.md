---
description: Run ruff linting and formatting on the project. Check for code quality issues, auto-fix where possible, and format Python files.
---
# Command: Lint

## Usage
Invoke this command to run ruff linting and formatting on the project.

## What it does

1. **Check + fix** — `python -m ruff check --fix .` — finds lint violations and auto-fixes them
2. **Format** — `python -m ruff format .` — formats all Python files per ruff's style

## When to use

Run this before committing changes (replaces the pre-commit hook that was previously used). No background process, no git lock contention — just manual on-demand linting.

## Commands

```powershell
python -m ruff check --fix .
python -m ruff format .
```

Or run both in sequence:

```powershell
python -m ruff check --fix . ; python -m ruff format .
```

## Also available

To run pre-commit on all files without committing:

```powershell
python -m pre_commit run --all-files
```

Run all tests:

```powershell
python -m pytest tests/ -v
```