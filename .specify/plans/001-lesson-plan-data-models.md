# Plan: Lesson Plan Data Models

## Phase 1 — Model types
- Create `src/models.py` with LessonPlan, LessonPlanMeta, Stage, Material BaseModel classes
- Define CEFR_LEVEL, INTERACTION, SHAPE Literal type aliases

## Phase 2 — Field validators
- Add stage_number >= 1 validator
- Add time format regex validator
- Add date format validator (3 patterns)
- Add CEFR level + interaction + shape Literal checks

## Phase 3 — Tests
- 20 tests: 6 Stage, 10 LessonPlan, 4 Material
- Test valid/invalid inputs, aliasing, empty defaults, round-trip
