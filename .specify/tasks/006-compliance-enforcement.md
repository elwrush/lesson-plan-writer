## Backlog

- [x] spec_coverage.py: module-in-spec check with bootstrap --allow-missing-specs
- [x] pydantic_compliance.py: AST-based scan (json.dumps, empty except, upsert)
- [x] spec_required.py: git-aware changed-file-in-spec check
- [x] ci_guard_check.py: artifact existence + completion + alignment
- [x] Makefile validate target (lint → test → spec-coverage → pydantic-compliance → spec-required → ci-guard)
- [x] .pre-commit-config.yaml local hook (uv run make validate)
- [x] Pre-commit hook installed (.git/hooks/pre-commit)
