# Feature: Compliance Enforcement

## Feature Summary

Four global compliance scripts at `~/.config/kilo/scripts/` plus a Makefile `validate` target and pre-commit hook that enforce Spec Kit rules, Pydantic standards, and testing discipline. Together they form an unbypassable mechanical gate: no commit can proceed unless all checks pass.

## User Scenarios

### User Story 1 — Pre-commit validation (P1)
Every `git commit` triggers `uv run make validate` → ruff lint, pytest, spec_coverage, pydantic_compliance, spec_required, ci_guard. Any failure blocks the commit.

**Why this priority:** Pre-commit hook is the only truly unbypassable gate (Part 2.1 of write-a-spec-guide.md).

### User Story 2 — Spec coverage enforcement (P1)
Every Python module in `scripts/` and `src/` must be documented in at least one spec in `.specify/specs/`. New files without spec entries are flagged.

**Why this priority:** Prevents silent code growth outside the spec-driven development cycle.

### User Story 3 — Pydantic compliance scan (P2)
Scans source code for: json.dump/json.dumps without model_validate, LLM API calls without response_format, empty except: pass blocks, table.upsert() without --upsert flag.

**Why this priority:** Catches the most common compliance violations automatically.

## Technical Approach

Four Python scripts at `~/.config/kilo/scripts/`, each a standalone CLI with `--project-root` argument and deterministic exit codes (0 = pass, 1 = fail):

1. `spec_coverage.py` — AST-free file scan. Reads spec files from `.specify/specs/`, finds Python source in `scripts/` and `src/`, checks case-insensitive filename stem against spec text. Supports `--allow-missing-specs` for bootstrap and `--exclude-file` for permanent exclusions.

2. `pydantic_compliance.py` — AST analysis via `ast.parse()`. Checks for json.dump/dumps calls (by walking function call nodes where method is `json.dump` or `json.dumps`), empty `except:` blocks (handler body is a single `pass`), and `table.upsert()` calls. Supports `--allowlist-file` for pre-existing violators.

3. `spec_required.py` — Git-aware. Runs `git diff` for staged/unstaged/untracked changes, filters to `.py` files, checks each stem against spec content.

4. `ci_guard_check.py` — Artifact existence. For each spec, verifies corresponding plan and tasks exist, tasks have at least one completion marker, and spec text references at least one real source file.

Makefile wraps all four into `validate` target. `.pre-commit-config.yaml` hooks `uv run make validate` as a local hook with `always_run: true`.

## Validation Rules

| Script | Check | Fail condition |
|--------|-------|----------------|
| spec_coverage.py | Module in spec | Not mentioned in any `.specify/specs/*.md` |
| pydantic_compliance.py | json.dumps without model_validate | `json.dump`/`json.dumps` in AST while no `model_validate` in file |
| pydantic_compliance.py | Empty except: pass | AST node where handler body is single `pass` |
| pydantic_compliance.py | table.upsert() | `table.upsert()` without `--upsert` flag context |
| spec_required.py | New file in spec | Changed `.py` file not mentioned in any spec |
| ci_guard_check.py | Plan + tasks exist | `.specify/plans/{stem}.md` or `.specify/tasks/{stem}.md` missing |
| ci_guard_check.py | Task completed | No `[x]` or "DONE" marker in tasks file |
| ci_guard_check.py | Spec-source alignment | No `scripts/` or `src/` file mentioned in spec text |

## Test Coverage

No dedicated test files yet — scripts are validated by manual `--help` and `--project-root` smoke tests.

## Acceptance Criteria

| ID | Criterion | Validation Method |
|----|-----------|-------------------|
| AC1 | script --help prints usage | Exit 0 |
| AC2 | --project-root . on clean project exits 0 | Shell exit code |
| AC3 | Makefile validate passes | `uv run make validate` exit 0 |
| AC4 | Pre-commit hook installed | `.git/hooks/pre-commit` file exists |
| AC5 | Violating commit blocked | `git commit` fails when make validate fails |

## Constraints

- Requires `uv` and `make` on PATH
- GitHub Actions CI is optional (Part 2.6 of write-a-spec-guide.md) — not implemented
- Bootstrap mode (`--allow-missing-specs`) must be removed once Phase 6 is complete
