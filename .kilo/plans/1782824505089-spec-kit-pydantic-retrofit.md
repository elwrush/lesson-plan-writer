# Spec Kit + Pydantic Retrofit — Lesson Plan Writer 3

## Goals

1. Mechanical enforcement of spec-first development via pre-commit hook (`make validate`)
2. Central Pydantic model (`src/models.py`) replacing 3× scattered `REQUIRED_FIELDS` validation lists
3. 6 specs covering the data-flow pipeline (models, PDF, slides converter, validation, audit, compliance)
4. Global compliance scripts reusable across all projects
5. Spec Kit initialization with fleet-orchestrator, ci-guard, and agent-context extensions

---

## Design Decisions (Resolved)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data model | `src/models.py` — `LessonPlan`, `Stage`, `Material` Pydantic models with `field_validator` decorators | 3 scripts duplicate the same validation; one source of truth |
| Compliance script location | Global: `~/.config/kilo/scripts/` | Reusable across all projects; already wired in global `kilo.jsonc` |
| Dependency scope | `uv` for enforcement-critical packages only (pydantic, pytest, ruff) | Operational scripts (`pixabay_download.py`, `check_vocab_levels.py`) run against system Python as-is |
| Spec backfill scope | 6 specs for data-flow pipeline + models | Leaf utilities (`pixabay_download.py`, `serve_slides.py`, etc.) excluded |
| Constitution | 8 merged articles: Test-First, Pydantic-Required, Blueprint Gate, Full-Audit, Skill Re-load, Hallucination Guard, No Shared Lua Edits, Library-First | Combines spec-kit defaults with project AGENTS.md Execution Gates |
| `field_validator` decorators | Encode date (`ddmmyy`), CEFR (`A1`-`C2`), interaction (`T-Ss`, `Ss-Ss`), time (`N min.`) | Currently validated implicitly across 3 scripts — make explicit |
| Bootstrap circular dependency | `spec_coverage.py` ships with `--allow-missing-specs` flag (warns, exit 0) | Compliance scripts check for specs, but specs don't exist yet. Flag removed after Phase 6. |

---

## Conscious Deviations from `write-a-spec-guide.md`

| Guide specifies | Our plan uses | Why |
|-----------------|---------------|-----|
| Compliance scripts in project `scripts/` | Global at `~/.config/kilo/scripts/` | Reusable across projects; Makefile references absolute path |
| `uv run ruff check src/ tests/ scripts/` | `uv run ruff check src/ tests/ scripts/` (same, but `src/` is new) | No prior `src/` directory existed |
| GitHub Actions CI (Part 2.6) | Not included | Optional second mechanical gate; project doesn't use GitHub Actions |

---

## Phase-by-Phase Implementation Plan

### Phase 0: Constitution

**File:** `.specify/memory/constitution.md`

**8 articles:**

1. **Test-First (Red/Green)** — No implementation code before corresponding test. Write test, confirm FAIL, then implement. Per `/mnt/c/PROJECTS/COMMON/red-green.md`.
2. **Pydantic-Required** — Every JSON write passes through `Model.model_validate()`. Every LLM JSON call uses `response_format={"type": "json_object"}`. No raw dicts between step functions.
3. **Blueprint Approval Gate** — Slide blueprints must be reviewed and explicitly approved before any `slides.md` is written.
4. **Full-Audit Rule** — When the user reports one problem, audit the entire `slides.md` against SKILL.md and blueprint. Fix all deviations in one pass.
5. **Skill Re-load Rule** — After any rejection or failure, re-load the relevant SKILL.md before making the next edit.
6. **Hallucination Guard** — Every stat/fact on answer slides must be verified against source transcription. No unverified numbers, dates, or locations.
7. **No Shared Lua Edits** — Shared infrastructure Lua files (`reading-feedback.lua`, `shield-block.lua`, etc.) are locked. Create standalone filters; ask user before modifying shared ones.
8. **Library-First** — Reusable modules (`src/models.py`) over ad-hoc validation. Each script imports from shared source, not copying validation lists.

---

### Phase 1: Global Compliance Scripts

Write 4 scripts at `~/.config/kilo/scripts/`. Each script returns exit 0 on pass, non-zero on failure. Accept `--project-root` argument.

#### 1.1 `spec_coverage.py`
- **Checks:** Every Python module in `scripts/` and `src/` is documented in at least one spec at `.specify/specs/`
- **Matching logic:** Case-insensitive filename stem match against spec content. Also check parent directory name (e.g., `scripts/build_lesson_pdf.py` matches specs mentioning `build_lesson_pdf` or `build-lesson-pdf`)
- **Bootstrap:** `--allow-missing-specs` flag warns but returns exit 0. Used until all 6 specs are written.
- **Config:** Read `.specify/config/audit-scope.json` for file patterns to include/exclude. Default: `scripts/**/*.py`, `src/**/*.py`.

#### 1.2 `pydantic_compliance.py`
- **Checks:**
  - Any `json.dump()`/`json.dumps()` call NOT followed by `model_validate()` in the same file → ERROR
  - Any `requests.post()`/LLM API call without `response_format` in the payload → ERROR
  - Empty `except:` or `except Exception: pass` blocks → ERROR (Part 4.3 enforcement)
  - `table.upsert()` without explicit `--upsert` flag in command → ERROR (if applicable)
- **Skip:** Files in `.specify/config/pydantic-allowlist.json`. Leaf utility scripts (Pixabay, Tavily, serve) are allowlisted.
- **Exit:** 0 if clean, 1 if violations found.

#### 1.3 `spec_required.py`
- **Checks:** New or modified source files (since last spec update) have a corresponding entry in `.specify/specs/`
- **Matching:** Filename stem (case-insensitive) must appear in at least one spec file
- **Git integration:** `git diff --name-only HEAD` to find modified files. `git log --diff-filter=A --name-only` for new files.
- **Exit:** 0 if all files covered, 1 if orphan files found.

#### 1.4 `ci_guard_check.py`
- **Checks:** (Part of `make validate` chain)
  - Artifact existence: For each spec in `.specify/specs/`, corresponding plan exists in `.specify/plans/` and tasks in `.specify/tasks/`
  - Task completion: At least one task marked `[x]` (DONE) or 100% completion verified
  - Spec-code alignment: At least one source module matches each spec (fuzzy filename match)
- **Exit:** 0 if all checks pass, 1 if violations.

---

### Phase 2: Project Dependency Setup

**Files modified:** `pyproject.toml` (add `[project]` and `[dependency-groups]`)

Add to existing `pyproject.toml`:

```toml
[project]
name = "lesson-plan-writer"
version = "3.0.0"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "ruff>=0.11",
]
```

Add `src/` to pyright includes:

```toml
[tool.pyright]
include = ["src", "scripts", "tests", "*.py"]
```

**Action:** Run `uv sync` to generate `uv.lock`.

---

### Phase 3: Spec Kit Initialization + Extensions

**Commands (in order):**

```bash
# 3.1 Initialize
specify init --here --integration kilocode --force

# 3.2 Install extensions
specify extension add fleet-orchestrator
specify extension add ci-guard
specify extension add agent-context

# 3.3 Verify
specify extension list
specify integration status
```

**Expected output:**
- `.specify/` directory created with `memory/`, `specs/`, `plans/`, `tasks/`, `templates/`, `workflows/`
- `.kilocode/workflows/` created with SDD workflow files
- `.kilocode/rules/specify-rules.md` created for agent context

**Pitfall guard (Part 7):** If `specify init` was previously run with wrong integration (`opencode`/`copilot`), run `specify integration switch kilocode` first.

---

### Phase 4: Pydantic Models + Tests

#### 4.1 Create `src/__init__.py`

```python
# src/__init__.py
```

#### 4.2 Create `src/models.py`

**Models:**

```python
from pydantic import BaseModel, field_validator
from typing import Literal

CEFR_LEVELS = Literal["A1", "A2", "B1", "B2", "C1", "C2"]
INTERACTION_PATTERNS = Literal["T-Ss", "Ss-Ss", "S-S", "S-Ss", "T-S", "Group", "Individual"]
SHAPES = Literal["ESA", "PPP", "TBL", "Test-Teach-Test", "Guided Discovery"]

class Material(BaseModel):
    name: str
    type: str  # "coursebook", "handout", "audio", "video", "slides"
    page: str | None = None

class Stage(BaseModel):
    stage_number: int
    stage: str
    stage_aim: str
    procedure: str
    time: str  # "N min."
    interaction: INTERACTION_PATTERNS

    @field_validator("stage_number")
    @classmethod
    def positive_stage(cls, v: int) -> int:
        if v < 1:
            raise ValueError(f"Stage number must be >= 1, got {v}")
        return v

    @field_validator("time")
    @classmethod
    def time_format(cls, v: str) -> str:
        import re
        if not re.match(r"^\d+(?:-\d+)?\s*min\.?$", v, re.IGNORECASE):
            raise ValueError(f"Time must match 'N min.' format, got '{v}'")
        return v

class LessonPlan(BaseModel):
    teacher: str
    duration: str
    date: str  # "DDMMYY" or "DD/MM/YY" or "D Month YYYY"
    topic: str
    materials: list[Material]
    shape: SHAPES
    shape_name: str
    cefr_level: CEFR_LEVELS
    class_name: str  # "class" is reserved — use class_name
    stages: list[Stage]

    @field_validator("date")
    @classmethod
    def date_format(cls, v: str) -> str:
        import re
        # Accept dd/mm/yy, d Month YYYY, or ddmmyy
        patterns = [
            r"^\d{1,2}/\d{1,2}/\d{2,4}$",
            r"^\d{1,2}\s+\w+\s+\d{4}$",
            r"^\d{6}$",
        ]
        if not any(re.match(p, v) for p in patterns):
            raise ValueError(f"Date '{v}' must match dd/mm/yy, d Month YYYY, or ddmmyy")
        return v

    @field_validator("class_name")
    @classmethod
    def non_empty_class(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("class_name must not be empty")
        return v
```

#### 4.3 Create `tests/test_models.py` (Red/Green)

**Test cases:**

1. Valid `Stage` parses correctly
2. Invalid `stage_number` (0, negative) raises `ValidationError`
3. Invalid `time` format ("5 minutes", "5") raises `ValidationError`
4. Valid `LessonPlan` with all fields parses correctly
5. Missing required field raises `ValidationError`
6. Invalid `date` format raises `ValidationError`
7. Invalid `cefr_level` raises `ValidationError`
8. Invalid `interaction` pattern raises `ValidationError`
9. Empty `stages` list is valid (allow empty lesson plans)
10. Model serializes to JSON via `model_dump()` and round-trips

**Procedure:**
1. Write tests first → run `uv run pytest tests/test_models.py -q` → confirm FAIL (no `src/models.py` yet)
2. Write `src/models.py` → run tests → confirm GREEN

---

### Phase 5: Makefile + Pre-commit

#### 5.1 Create `Makefile`

```makefile
.PHONY: validate lint test spec-coverage pydantic-compliance spec-required ci-guard

GLOBAL_SCRIPTS := $(HOME)/.config/kilo/scripts

validate: lint test spec-coverage pydantic-compliance spec-required ci-guard
	@echo "Full validation passed."

lint:
	uv run ruff check src/ tests/ scripts/

test:
	uv run pytest tests/ -q

spec-coverage:
	uv run python $(GLOBAL_SCRIPTS)/spec_coverage.py --project-root . --allow-missing-specs

pydantic-compliance:
	uv run python $(GLOBAL_SCRIPTS)/pydantic_compliance.py --project-root .

spec-required:
	uv run python $(GLOBAL_SCRIPTS)/spec_required.py --project-root .

ci-guard:
	uv run python $(GLOBAL_SCRIPTS)/ci_guard_check.py --project-root .
```

**Key:** `spec-coverage` uses `--allow-missing-specs` during bootstrap. Remove this flag after Phase 6.

#### 5.2 Update `.pre-commit-config.yaml`

Replace current minimal config:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate
        name: Full validation suite
        description: ruff → pytest → spec_coverage → pydantic_compliance → spec_required → ci_guard
        entry: uv run make validate
        language: system
        pass_filenames: false
        always_run: true
```

#### 5.3 Install pre-commit hook

```bash
uv run pre-commit install
```

**Pitfall guard (Part 7):** Verify hook file exists at `.git/hooks/pre-commit` after install.

---

### Phase 6: Spec Backfill (via Fleet Orchestrator)

For each of the 6 specs, run the full SDD cycle. Order matters — models first, then consumers.

#### Spec template (Part 9 integration)

Every spec file at `.specify/specs/###-feature-name.md` follows this structure:

```
# Feature: <Name>

## Feature Summary
One paragraph: what it does, who uses it, what problem it solves.

## User Scenarios
### User Story 1 — <Title> (P1)
<description>
**Why this priority:** <justification>

## Technical Approach
What modules/files change, what libraries are added, architecture patterns.

## Validation Rules
| Model | Field | Rule |
|-------|-------|------|
| <Model> | <field> | <constraint> |

## Test Coverage
What each test file covers, verification method.

## Acceptance Criteria
| ID | Criterion | Validation Method |
|----|-----------|-------------------|
| AC1 | <criterion> | Pydantic model_validate() / pytest |

## Constraints
Tech stack, format rules, integration points, dependencies, guardrails.
```

#### 6.1 `lesson-plan-data-models`
- **Covers:** `src/models.py` — LessonPlan, Stage, Material, field_validators
- **P1 Stories:** LessonPlan model validates JSON input; Stage model enforces field constraints
- **Validation Rules:** Every field + `field_validator` from Phase 4 model
- **Tests:** `tests/test_models.py`

#### 6.2 `lesson-plan-pdf-pipeline`
- **Covers:** `build_lesson_pdf.py` — Markdown→Pandoc→Typst→PDF three-layer pipeline
- **P1 Stories:** Build PDF from lesson.md; template hash verification; font resolution
- **Validation Rules:** REQUIRED_META keys, template lock hash, pandoc exit code
- **Tests:** `tests/test_build_lesson_pdf.py`

#### 6.3 `lesson-plan-slides-converter`
- **Covers:** `json_to_markdown.py` — lesson plan JSON → slides.md
- **P1 Stories:** Convert lesson JSON to valid Pandoc Markdown; preserve speaker notes; handle image assets
- **Validation Rules:** Slide structure (heading + notes + body), fenced div balance
- **Tests:** `tests/test_json_to_markdown.py`

#### 6.4 `slide-validation-gate`
- **Covers:** `validate_slides.py` — pre-build validation checks
- **P1 Stories:** Catch missing speaker notes; detect raw HTML; verify file references; enforce CSS hash-lock
- **Validation Rules:** Per check: speaker notes, raw HTML, fenced div balance, missing files, YouTube IDs, inline CSS, unauthorized assets, CSS hash
- **Tests:** `tests/test_validate_slides.py`

#### 6.5 `slide-audit-pipeline`
- **Covers:** `audit_slides.py` — cross-reference lesson plan JSON vs slides index.html
- **P1 Stories:** Verify stage coverage; check exercise consistency; validate page references; detect banned text patterns
- **Validation Rules:** Stage name matching, exercise reference extraction, page number extraction, banned text patterns
- **Tests:** `tests/test_slide_structure.py`

#### 6.6 `compliance-enforcement`
- **Covers:** 4 global scripts — spec_coverage, pydantic_compliance, spec_required, ci_guard
- **P1 Stories:** Pre-commit hook blocks unvalidated commits; spec_coverage detects undocumented modules; pydantic_compliance catches raw dict writes
- **Validation Rules:** Exit codes, report format, bootstrap mode, allowlist support
- **Tests:** `tests/test_compliance_scripts.py`

**Procedure for each:**
```
/speckit.fleet.run  (describe the spec from the table above)
  → specify → [review gate: approve/reject] → plan → [review gate: approve/reject] → tasks → implement → converge
```

**Pitfall guard (Part 7):** After implement, run converge. If gaps found, loop implement→converge until 100%. CI Guard module detection requires case-insensitive filename matching — verify both module stem AND parent directory name.

---

### Phase 7: Refactor Scripts to Use Pydantic

#### 7.1 `build_lesson_pdf.py`
- **Before:** Manual `REQUIRED_META` list with `for key in REQUIRED_META: assert key in meta`
- **After:** `from src.models import LessonPlan` → `LessonPlan.model_validate(meta)`
- **Risk:** `build_lesson_pdf.py` reads YAML frontmatter via Pandoc, not raw JSON. The mapping may need a conversion step (e.g., `class` → `class_name`). Verify with existing test suite.

#### 7.2 `json_to_markdown.py`
- **Before:** Manual `REQUIRED_FIELDS`, `REQUIRED_LESSON_PLAN_FIELDS`, `REQUIRED_STAGE_FIELDS` lists
- **After:** `LessonPlan.model_validate(data)` at entry point
- **Risk:** Medium — this script consumes JSON directly. Field names must match exactly or use `model_validate` with `from_attributes=True`.

#### 7.3 `json_to_pdf.py`
- **Same as 7.2** — replace manual validation with `LessonPlan.model_validate()`

#### 7.4 Silent exception audit (Part 4.3 integration)
- Scan all 28 scripts for empty `except:` blocks
- Replace each with `except Exception as exc: print(f"WARNING: {exc}", file=sys.stderr)`
- Add to Phase 7 checklist

#### 7.5 Update `pyright` config
- Add `src/` to includes: `include = ["src", "scripts", "tests", "*.py"]`
- Verify no new type errors with `uv run pyright src/`

---

### Phase 8: Full Validation

```bash
# 8.1 Remove bootstrap flag from Makefile
# Edit Makefile: change --allow-missing-specs to (nothing)

# 8.2 Run full validation
uv run make validate

# 8.3 Spec compliance check
uv run python ~/.config/kilo/scripts/ci_guard_check.py --project-root .

# 8.4 Drift detection
# (via slash command in agent)
/speckit.ci-guard.drift

# 8.5 Final verdict
/verify
```

**Expected:** All checks pass. Exit code 0. Agent can commit with confidence.

---

## Validation Checkpoints

After each phase, verify:

| Phase | Checkpoint |
|-------|-----------|
| 0 | `.specify/memory/constitution.md` exists, 8 articles present |
| 1 | 4 scripts at `~/.config/kilo/scripts/` each accept `--project-root` and `--help` |
| 2 | `uv run python -c "import pydantic"` succeeds; `uv.lock` exists |
| 3 | `specify extension list` shows fleet-orchestrator, ci-guard, agent-context |
| 4 | `uv run pytest tests/test_models.py -q` → 10 tests GREEN |
| 5 | `make validate` runs (may soft-warn on coverage); `.git/hooks/pre-commit` exists |
| 6 | 6 spec files, 6 plan files, 6 task files; all tasks marked DONE |
| 7 | `uv run pytest tests/ -q` → all existing tests still pass; no new pyright errors |
| 8 | `uv run make validate` exit 0; `ci-guard.drift` reports no drift |

---

## Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| `json_to_markdown.py` field name mismatch with Pydantic model | Medium | Map fields in conversion layer; run existing test suite after refactor |
| `spec_coverage.py` flags all 28 scripts as undocumented | High (by design) | Bootstrap `--allow-missing-specs` flag; only check 6 specced scripts |
| Spec Kit init creates `.kilocode/` that conflicts with `.kilo/` | Low | Verified: separate namespaces; no overlap |
| Pre-commit hook blocks all commits during bootstrap | High (by design) | Hook not installed until Phase 5; `--allow-missing-specs` active until Phase 8 |
| `build_lesson_pdf.py` YAML frontmatter keys differ from Pydantic field names | Medium | `class` → `class_name` mapping; verify with existing tests |
| Lua filter quality gates conflict with spec kit enforcement | Low | Phase 7 touches only Python scripts; Lua filters untouched |

---

## Files Summary

| Phase | New | Modified |
|-------|-----|----------|
| 0 | 1 (constitution.md) | 0 |
| 1 | 4 (global scripts) | 0 |
| 2 | 1 (uv.lock) | 1 (pyproject.toml) |
| 3 | ~15 (.specify/ + .kilocode/) | 0 |
| 4 | 2 (src/__init__.py, src/models.py) | 1 (pyproject.toml pyright includes) |
| 5 | 2 (Makefile, .pre-commit-config.yaml) | 0 |
| 6 | 18 (.specify/specs/×6, plans/×6, tasks/×6) | 1 (Makefile remove bootstrap flag) |
| 7 | 0 | 3 (build_lesson_pdf.py, json_to_markdown.py, json_to_pdf.py) |
| 8 | 0 | 0 |
| **Total** | **~43** | **~6** |
