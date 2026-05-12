# Code Quality Setup — Ruff + pre-commit

Copy this file into a new Python project and follow the instructions to set up automated linting and formatting.

## Overview

Three components work together:

| Component | Purpose |
|-----------|---------|
| `ruff` (global CLI) | Linter + formatter for Python |
| `pyproject.toml` | Project-level Ruff configuration |
| `pre-commit` (global CLI) | Git hook manager |
| `.pre-commit-config.yaml` | Hook definition — runs `ruff` before every `git commit` |

## Step 1: Verify global tools

```bash
python -m ruff --version
python -m pre_commit --version
```

If either fails, install:
```bash
python -m pip install ruff pre-commit
```

## Step 2: Create `pyproject.toml`

Paste this at the project root:

```toml
[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.ruff.lint.per-file-ignores]
# Add per-file ignores here if needed

[tool.ruff.format]
quote-style = "double"
```

**Rule reference:**
- `E` = pycodestyle errors
- `F` = pyflakes (logic errors)
- `I` = isort (import sorting)
- `N` = pep8-naming
- `W` = pycodestyle warnings
- `UP` = pyupgrade (modern Python idioms)

## Step 3: Create `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Step 4: Update `.gitignore`

Add this line if not already present:
```
.ruff_cache/
```

## Step 5: Install the git hook

```bash
python -m pre_commit install
```

This creates `.git/hooks/pre-commit`. On every `git commit`, Ruff checks staged `.py` files and auto-fixes them.

## Step 6: Verify

```bash
# Lint check — should pass
python -m ruff check .

# Format check — should show no changes needed
python -m ruff format . --check

# Dry-run the pre-commit hook on all files
python -m pre_commit run --all-files
```

## Usage

- **Manual lint + fix:** `python -m ruff check --fix .`
- **Format:** `python -m ruff format .`
- **Watch mode:** `python -m ruff check --watch .` (polls for file changes)
- **Run tests:** `python -m pytest tests/ -v`