.PHONY: validate lint test spec-coverage pydantic-compliance spec-required ci-guard

GLOBAL_SCRIPTS := $(HOME)/.config/kilo/scripts

validate: lint test spec-coverage pydantic-compliance spec-required ci-guard
	@echo "Full validation passed."

lint:
	uv run ruff check src/ tests/ scripts/

test:
	uv run pytest tests/ -q --ignore=tests/test_pandoc_and_lua_registry.py --ignore=tests/test_slide_structure.py

spec-coverage:
	uv run python $(GLOBAL_SCRIPTS)/spec_coverage.py --project-root . --exclude-file .specify/config/spec-coverage-exclude.txt

pydantic-compliance:
	uv run python $(GLOBAL_SCRIPTS)/pydantic_compliance.py --project-root . --allowlist-file .specify/config/pydantic-allowlist.txt

spec-required:
	uv run python $(GLOBAL_SCRIPTS)/spec_required.py --project-root . --bootstrap

ci-guard:
	uv run python $(GLOBAL_SCRIPTS)/ci_guard_check.py --project-root .
