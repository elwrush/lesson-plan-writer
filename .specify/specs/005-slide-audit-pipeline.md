# Feature: Slide Audit Pipeline

## Feature Summary

Cross-reference slide content against the lesson plan JSON. `audit_slides.py` compares the generated slides HTML with the source lesson plan JSON to verify: every stage has at least one matching slide, every exercise reference in the plan appears in the slides, every page reference from the plan is present in slides, and no banned text patterns (like "Source: First Steps", "Teacher:", "Duration:") appear on slides.

## User Scenarios

### User Story 1 — Verify stage coverage (P1)
Each stage in the lesson plan should have at least one slide. The audit checks stage names against slide titles using fuzzy matching. Missing stages are flagged as failures.

**Why this priority:** A stage without a slide means students miss that activity.

### User Story 2 — Exercise consistency (P2)
Every exercise reference (e.g., "Practice 1A") from the lesson plan should appear in at least one slide's title or body. Conversely, exercises on slides not in the lesson plan are flagged (unless they're bespoke tests).

**Why this priority:** Exercise drift between plan and slides is a common agent error.

## Technical Approach

`audit_slides.py` loads the lesson plan JSON and extracts stage info (number, name, procedure text). It then parses the built HTML file, splitting by `<!-- SLIDE N: -->` comments. Exercise/page references are extracted via regex from both sources. Stage coverage uses keyword-matching (stage name words in slide title). Exercise consistency uses set comparison. Page references use substring matching. Content quality checks scan for banned text patterns.

Four audit checks:
1. Stage coverage (plan stages → matching slides)
2. Exercise consistency (plan exercises → slide references, bidirectional)
3. Page reference consistency (plan pages → slide references)
4. Content quality (no banned text patterns)

## Validation Rules

| Check | Rule |
|-------|------|
| Stage coverage | Every stage in plan has >= 1 matching slide |
| Exercise consistency | Plan exercises appear on slides; slide exercises appear in plan (or are bespoke) |
| Page consistency | Plan page numbers appear in slides |
| Content quality | No "Source: First Steps", "Teacher:", "Duration:" visible |

## Test Coverage

`tests/test_slide_structure.py`: Indirectly tested via pedagogical intent and filter output tests. `audit_slides.py` itself is CLI-driven.

## Acceptance Criteria

| ID | Criterion | Validation Method |
|----|-----------|-------------------|
| AC1 | Matching plan+slides reports minimal issues | Manual CLI run |
| AC2 | Stage missing from slides flagged | Fuzzy matching produces hit |
| AC3 | Banned text on slides detected | Pattern match |

## Constraints

- Requires both lesson plan JSON AND built slides HTML (not slides.md)
- Fuzzy matching may produce false negatives on very different stage/slide naming
- Unicode-safe printing required for Windows console (safe_print wrapper)
