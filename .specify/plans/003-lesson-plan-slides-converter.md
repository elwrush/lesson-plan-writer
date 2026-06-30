# Plan: Lesson Plan Slides Converter

## Phase 1 — Input validation
- REQUIRED_FIELDS / REQUIRED_LESSON_PLAN_FIELDS / REQUIRED_STAGE_FIELDS list checks
- (Eventually replace with LessonPlan.model_validate())

## Phase 2 — Slide generation
- Per-stage iteration generates slide headings + speaker notes + body
- Differentiation tiers: Standard/Advanced/Elite with FA icons

## Phase 3 — Output
- Writes slides.md with Pandoc Markdown syntax
- Fenced divs for title rows, shields, challenge tiers
