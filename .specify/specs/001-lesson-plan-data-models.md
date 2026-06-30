# Feature: Lesson Plan Data Models

## Feature Summary

Pydantic data models for lesson plan validation. Defines `LessonPlan`, `LessonPlanMeta`, `Stage`, and `Material` models that replace three manually maintained `REQUIRED_FIELDS` lists currently duplicated across `build_lesson_pdf.py`, `json_to_markdown.py`, and `json_to_pdf.py`. Uses `field_validator` decorators for date format, CEFR level, interaction pattern, and time format enforcement.

## User Scenarios

### User Story 1 — Validate incoming JSON (P1)
Any script that reads a lesson plan JSON can use `LessonPlan.model_validate(data)` instead of manual field-by-field checks with `if field not in data`. The Pydantic BaseModel guarantees all required fields present and correctly typed.

**Why this priority:** Three scripts independently validate the same structure. Centralizing eliminates drift.

### User Story 2 — Domain constraints enforced (P1)
Field validators reject: dates not matching dd/mm/yy/ddmmyy/d Month YYYY, CEFR levels outside A1-C2, stage numbers < 1, times not matching "N min." format, interaction patterns not in the standard set.

**Why this priority:** These constraints are currently implicit or enforced differently per script.

## Technical Approach

Four Pydantic v2 models at `src/models.py`:
- `Material` (name, type, optional page)
- `Stage` (stage_number, stage, stage_aim, procedure, time, interaction) with `field_validator` for stage_number >= 1, time regex `^\d+(?:-\d+)?\s*min\.?$`, interaction Literal set
- `LessonPlanMeta` (shape, shape_name, cefr_level, class_name aliased from `class`, stages) with CEFR Literal A1-C2
- `LessonPlan` (teacher, duration, date, topic, materials, lesson_plan) with date validator for 3 patterns

`class` field is a Python reserved word — uses `Field(alias="class")` to accept JSON key `"class"` while exposing `.class_name` in Python.

## Validation Rules

| Model | Field | Rule |
|-------|-------|------|
| Stage | stage_number | int, >= 1 |
| Stage | time | str matching `N min.` or `N-M min.` |
| Stage | interaction | Literal: T-Ss, Ss-Ss, S-S, S-Ss, T-S, Group, Individual |
| LessonPlanMeta | cefr_level | Literal: A1, A2, B1, B2, C1, C2 |
| LessonPlanMeta | shape | Literal: ESA, PPP, TBL, Test-Teach-Test, Guided Discovery |
| LessonPlanMeta | class_name | str (aliased from `class` in JSON) |
| LessonPlan | date | str matching dd/mm/yy, ddmmyy, or d Month YYYY |
| LessonPlan | materials | default empty list if missing |

## Test Coverage

`tests/test_models.py`: 20 tests across 3 test classes — TestStage (6), TestLessonPlan (10), TestMaterial (4). Covers valid/invalid inputs, field aliasing, empty defaults, JSON round-trip, and edge cases (empty stages, missing materials, negative stage numbers, invalid date/CEFR/shape/interaction formats).

## Acceptance Criteria

| ID | Criterion | Validation Method |
|----|-----------|-------------------|
| AC1 | LessonPlan.model_validate(valid_json) returns populated object | pytest assertion |
| AC2 | Invalid date raises ValidationError | pytest.raises(ValidationError) |
| AC3 | Invalid CEFR level raises ValidationError | pytest.raises(ValidationError) |
| AC4 | class field alias round-trips correctly | model_dump(by_alias=True) has 'class' key |
| AC5 | Empty materials default to [] | model_validate without materials key |
| AC6 | Stage with stage_number=0 raises ValidationError | pytest.raises(ValidationError) |

## Constraints

- Pydantic v2 only (uses BaseModel, not the removed v1 API)
- Python >= 3.12 for `from typing import Literal` with `\|` syntax
- No external API calls — pure data validation
