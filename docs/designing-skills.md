# Designing Agent Skills — Progressive Disclosure Pattern

This document explains how to structure skills for agent consumption using the **progressive disclosure** pattern. The target reader is an agent tasked with writing a new skill or refactoring an existing one.

## The Pattern: Three-Tier Loading

A skill is not a document. It is a **procedural brain** that guides the agent through a task step by step. The brain should be lean — reference material belongs in supplementary files that the agent fetches on demand.

```
Tier 1: Advertise (~100 tokens)
  name + description in frontmatter.
  Agent sees this at session start for EVERY skill.
  Make it discoverable — specific, not generic.

Tier 2: Load (SKILL.md, <500 lines recommended)
  Full skill body loaded when the skill is triggered.
  Contains ONLY procedural workflow steps.
  This is the "brain" — the agent follows this moment by moment.

Tier 3: Read references/ files (on demand)
  Design rules, language constraints, debugging guides.
  Agent reads these ONLY when a specific subtask requires them.
  Never loaded into context unless explicitly needed.

Tier 4: Run scripts/ (executed, not read)
  Python/bash CLIs for deterministic operations.
  Agent runs them without loading source into context.
```

**Source:** This pattern is documented by Microsoft Agent Framework, Anthropic, mgechev/skills-best-practices, SwirlAI, and MindStudio. It is the industry-standard approach for agent skill design.

## The Extended TOC Technique

When you must refer to material that belongs in a `references/` file, use the **Extended TOC** pattern (Addy Osmani):

```
## Section Name

2-line summary of what the section covers.

- Critical point 1 (must remember)
- Critical point 2 (must remember)

See `references/filename.md` for the complete reference.
Consult this file when [specific trigger condition].
```

The TOC gives the agent a map at Tier 2. The agent fetches details from Tier 3 only when the trigger condition is met. Without the trigger condition, the agent must guess when to read the reference, which leads to either unnecessary reads (context bloat) or missed reads (quality loss).

## Decision Rules: Inline vs Reference

Keep inline in SKILL.md if the agent needs it **every session** during the task:

| Keep inline | Move to references/ |
|---|---|
| Procedural workflow steps (Step 0, Step 1, Step 2...) | Reference tables (color values, fragment classes) |
| Configuration instructions (copy template, run script) | Design rules that duplicate documentation |
| Format specifications (annotation formats, code snippets) | Language/style constraints (vocabulary ceilings) |
| Verification checklists the agent runs after every build | Debug guides (plugin failure, layout breaks) |
| Decision gates ("if you cannot fill this in, redesign") | Rarely-used adaptations (B2 rules, edge cases) |

The litmus test: **If the agent would need to read this section on every invocation to complete the task, keep it inline. If the agent reads it only when something specific happens (a rule check fails, a layout breaks, a rare language level is needed), move it to references/.**

## How It Was Applied Here

The `lesson-plan-to-reveal` skill at `.kilo/skills/lesson-plan-to-reveal/SKILL.md` is the canonical example:

| Section | Decision | Rationale |
|---------|----------|-----------|
| Workflow Steps 0-6 (500 lines) | **Inline** | Agent follows these every build session. |
| Annotation format (4-line comment block) | **Inline** | Agent writes this on every slide. |
| Design Blueprint format (6 tables) | **Inline** | Agent creates a blueprint before every build. |
| Fragment Policy (10 lines) | **Inline** (minimal) | Agent needs fragment class names at generation time. |
| Key Design Rules (70 lines → 6-line TOC) | **Moved to references/key-design-rules.md** | 15+ standalone rules. Agent needs 2-3 per session. |
| Authorial Voice (53 lines → 5-line TOC) | **Moved to references/authorial-voice.md** | Static reference table. Consult during Design Blueprint. |
| Common Pitfalls (57 lines → 4-line TOC) | **Moved to references/common-pitfalls.md** | Debug-only. Read when verification fails. |

The result: SKILL.md dropped from 860 lines to 540 lines. The agent loads 320 fewer lines of reference material into context on every activation but still has access to everything it needs via Tier-3 reads.

## The TOC Trigger Condition

Every TOC must specify WHEN the agent should read the reference file:

| Reference file | Trigger condition |
|---|---|
| `references/key-design-rules.md` | "When you encounter an unfamiliar slide type or when a rule check fails." |
| `references/authorial-voice.md` | "During the Design Blueprint phase to check language against the B1 word list." |
| `references/common-pitfalls.md` | "When verification fails, answer-list layout breaks, or slides appear blank/empty in browser." |

Without a trigger condition, the agent must either load the reference proactively (bloating context) or discover it reactively after failure (wasting a cycle). The trigger condition eliminates both failure modes.

## File Structure Convention

```
skill-name/
├── SKILL.md                    # Procedural brain (<500 lines recommended)
├── references/                 # Supplementary files (Level 3, read on demand)
│   ├── design-rules.md
│   ├── language-guide.md
│   └── troubleshooting.md
└── scripts/                    # Executable CLIs (Level 4, run without reading)
    ├── validate.py
    └── generate.py
```

## Measuring Success

| Metric | Good | Needs work |
|--------|------|------------|
| SKILL.md line count | <500 lines | >800 lines |
| Reference files | Present with TOC triggers | None — everything inline |
| First section loaded | Agent can start working immediately | Agent must read 200 lines of reference before first action |
| Context quality | Every line is procedural — the agent acts on it | Lines are descriptive — the agent reads but doesn't act |
