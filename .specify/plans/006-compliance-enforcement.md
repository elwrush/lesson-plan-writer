# Plan: Compliance Enforcement

## Phase 1 — Global compliance scripts
- spec_coverage.py: module-in-spec check with bootstrap mode
- pydantic_compliance.py: AST-based code scan
- spec_required.py: git-aware changed-file check
- ci_guard_check.py: artifact existence + completion + alignment

## Phase 2 — Makefile validate target
- lint → test → spec-coverage → pydantic-compliance → spec-required → ci-guard

## Phase 3 — Pre-commit hook
- .pre-commit-config.yaml local hook runs uv run make validate
- Hook installed at .git/hooks/pre-commit
