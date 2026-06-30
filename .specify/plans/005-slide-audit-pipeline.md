# Plan: Slide Audit Pipeline

## Phase 1 — Plan data extraction
- Load lesson plan JSON
- Extract stage info (number, name, exercise/page references) from procedure text

## Phase 2 — Slide data extraction
- Load built HTML
- Split by SLIDE comments
- Extract exercise/page references from visible content

## Phase 3 — Cross-reference checks
- Stage coverage: each plan stage has matching slide
- Exercise consistency: bidirectional check
- Page consistency: plan pages appear on slides
- Content quality: no banned text patterns
