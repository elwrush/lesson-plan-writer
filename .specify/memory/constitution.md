# Constitution — Lesson Plan Writer 3

These articles are immutable principles that govern how specs become code in this project. Violations must be flagged by spec-coverage, pydantic-compliance, or ci-guard checks.

## Article I — Test-First (Red/Green)

No implementation code before corresponding test. Write test, confirm FAIL (red), then implement (green). Per `/mnt/c/PROJECTS/COMMON/red-green.md`. Every feature module must have a corresponding test file in `tests/`.

## Article II — Pydantic-Required

Every JSON write must pass through `Model.model_validate()` first. Every LLM call expecting JSON must use `response_format={"type": "json_object"}`. No raw dicts between step functions. Default to `table.insert()`, not `table.upsert()`.

## Article III — Blueprint Approval Gate

Slide blueprints must be reviewed and explicitly approved by the user before any `slides.md` is written. No exceptions. The blueprint is the design document; `slides.md` is a mechanical translation.

## Article IV — Full-Audit Rule

When the user reports one problem, immediately audit the entire `slides.md` against the relevant SKILL.md and blueprint. Find and list ALL deviations. Fix them in one pass. Do not fix the single issue in isolation.

## Article V — Skill Re-load Rule

After any rejection or failure, re-load the relevant SKILL.md to refresh pedagogical principles before making the next edit. The patterns are documented there — reading them eliminates guesswork.

## Article VI — Hallucination Guard

After writing any answer slide, verify every stat and fact against the source transcription. If the source doesn't contain a specific number, date, or location, do not include it. No unverified content on answer slides.

## Article VII — No Shared Lua Edits

Never modify shared infrastructure Lua files (`reading-feedback.lua`, `shield-block.lua`, `box-keywords.lua`, `audio-autoplay.lua`, `youtube-embed.lua`, `slide-helper.lua`). Create new standalone filters with unique names. Ask the user before modifying any shared filter.

## Article VIII — Library-First

Reusable modules (`src/models.py`) over ad-hoc duplicate validation. Each script imports from the shared source rather than copying validation lists. No two scripts should independently define the same field constraints.
