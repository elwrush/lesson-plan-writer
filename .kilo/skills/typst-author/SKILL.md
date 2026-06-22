---
name: typst-author
description: Generate idiomatic Typst (.typ) code, edit and troubleshoot Typst documents and projects, and answer Typst syntax/reference questions. Use when working with .typ files or when the user explicitly asks for Typst document creation, editing, debugging, compilation, formatting, template work, or package usage.
---

# Typst Author

## Purpose

Generate, edit, and debug idiomatic Typst (.typ) code with accurate syntax and up-to-date API knowledge. Handles all Typst tasks: document creation, template work, layout design, table formatting, and compilation troubleshooting. Avoids common traps like `else` without `#`, `json(str)` treating input as file paths, and hash-in-content context mode errors.

**Output:** Typst `.typ` source files or compiled PDF output, depending on the task.

## When to Use

Use this skill when:
- The user explicitly asks to write, edit, or debug Typst (.typ) code
- The user asks Typst syntax or API reference questions
- A document needs quick Typst prototyping

Do NOT use this skill when:
- The Markdown → Pandoc → Typst pipeline can handle the task (use `build-excellent-lesson-plans` or `create-beautiful-slideshows` instead)
- The output is slides or lesson plans — those have dedicated skills

**Trigger:** When the user explicitly asks Typst-related questions or requests Typst code.

## Overview

This skill helps agents generate, edit, and reason about Typst documents. It provides quick‑start examples, detailed workflows, and links to the full Typst documentation (guides, tutorials, reference).

## Minimal document example

```typst
#set document(title: "My Document", author: "Author Name")
#set page(numbering: "1")
#set text(lang: "en")

// Enable paragraph justification and character-level justification
#set par(
  justify: true,
  justification-limits: (
    tracking: (min: -0.012em, max: 0.012em),
    spacing: (min: 75%, max: 120%),
  )
)

#title[My Document]

= Heading 1

This is a paragraph in Typst.

== Heading 2

#lorem(50)
```

## Workflow

### Step 1 — Read relevant documentation

Use local file search to find the relevant syntax in the bundled `docs/` folder. Verify function names, parameters, and syntax against local docs before generating code. See [docs/tutorial/writing-in-typst.md](docs/tutorial/writing-in-typst.md) for the tutorial and [docs/reference/](docs/reference/) for the API reference.

### Step 2 — Generate or modify .typ source

Generate or modify the `.typ` source according to the user's request. Follow the "Minimal document example" pattern for new projects. For existing content, locate the target text and apply changes.

### Step 3 — Run post-edit formatting checks

After each `.typ` file modification, run `typstyle --check <file>`. If it fails, inspect with `typstyle --diff <file>` and decide whether to apply formatting with `typstyle -i <file>`.

### Step 4 — Validate

Validate with `typst compile` after formatting is complete, or use `typst query` for probing uncertain behavior.

### Step 5 — Summarize touched files and outcomes

Summarize the edited files and outcomes for the user. Provide full `.typ` content only when requested.

## Documentation

- **Syntax & foundations**: `docs/reference/syntax.md`
- **Styling & show/set rules**: `docs/reference/styling.md`
- **Scripting & runtime behavior**: `docs/reference/scripting.md`
- **Page setup & tables**: `docs/guides/page-setup.md` and `docs/guides/tables.md`
- **Task-oriented authoring help**: `docs/tutorial/writing-in-typst.md`, `docs/guides/*.md`, and `docs/reference/**/*.md`

## Detailed instructions

1. **PRIORITY: Trust local documentation**. Your internal training data regarding Typst may be outdated or hallucinated. Always verify function names, parameters, and syntax against the local `docs/` folder before generating code.
2. **Read the relevant documentation** using local file search and open tools on the paths above.
3. **Use local docs for syntax and reference questions**. Verify syntax, function names, parameters, and reference behavior from the bundled docs. Run a minimal Typst probe only when runtime or evaluation behavior remains unclear after checking the docs.
4. **Generate or modify the `.typ` source** according to the user's request.
5. **Run the post-edit formatting checks below** for every `.typ` file you created or edited in that pass.
6. **Validate** with `typst compile` after the formatting decision is complete when you created or edited `.typ` files, or when the user explicitly asks for verification (if tool access is allowed).
7. **Summarize touched files and outcomes**. Provide full `.typ` content only when the user requests it or when direct editing is not possible, and optionally include a rendered preview (PDF/HTML).

### Probing uncertain behavior

- Use a probe when the bundled docs do not settle runtime or evaluation behavior.
- Model the case with Typst scripting as described in [docs/reference/scripting.md](docs/reference/scripting.md).
- When a probe is necessary, prefer a fileless probe through stdin instead of creating scratch `.typ` files. Expose the value with `metadata(...) <probe>` and read it with `typst query - "<probe>" --field value --one`. See [docs/reference/introspection/query.md](docs/reference/introspection/query.md) and [docs/reference/introspection/metadata.md](docs/reference/introspection/metadata.md).
- Example: `printf '#metadata(1 + 2) <probe>\n' | typst query - "<probe>" --field value --one`

### Post-edit formatting checks

1. **Check whether `typstyle` is available** with `command -v typstyle`. If it is unavailable, skip the remaining formatting checks.
2. **After each `.typ` file modification, run `typstyle --check <file>`** for the file you just created or edited.
3. **If `typstyle --check` fails, inspect the formatter changes with `typstyle --diff <file>`** before deciding what to do.
4. **Apply formatting with `typstyle -i <file>`** only when the formatter changes are limited to a newly created file or to code you created or edited in the current task.
5. **Stop and ask the user when formatting would change untouched pre-existing code**. If the diff reaches outside your own edits, or if you cannot confidently prove that every formatter change is limited to your edits, ask instead of formatting.

## Quick syntax reference

### Critical distinctions

- **Arrays**: `(item1, item2)` (parentheses). See [docs/reference/foundations/array.md](docs/reference/foundations/array.md).
- **Dictionaries**: `(key: value, key2: value2)` (parentheses with colons). See [docs/reference/foundations/dictionary.md](docs/reference/foundations/dictionary.md).
- **Content blocks**: `[markup content]` (square brackets). See [docs/reference/foundations/content.md](docs/reference/foundations/content.md).
- **NO tuples**: Typst only has arrays.

### Hash usage (markup vs code)

- Use `#` to start a code expression inside markup or content blocks; it disambiguates code from text. This is required for content-producing function calls and field access in markup: `#figure[...]`, `#image("file.png")`, `text(...)[#numbering(...)]`.
- Do not use `#` inside code contexts (argument lists, code blocks, show-rule bodies). Example: `#figure(image("file.png"))` (no `#` before `image`).
- Reference: [docs/reference/scripting.md](docs/reference/scripting.md), [docs/tutorial/writing-in-typst.md](docs/tutorial/writing-in-typst.md)

```typst
// Incorrect (missing # inside content block)
text(...)[(numbering(...))]

// Correct
text(...)[(#numbering(...))]
```

### Styling rules: set vs show

- `set`: Set rule to configure optional parameters on element functions (style defaults scoped to the current block or file).
- `show`: Show rule to target selected elements and apply a set rule or transform/replace the element output.
- Use `set` for common styling; use `show` for selective or structural changes (e.g., `heading.where(level: 1)`, labels, text, regex).

```typst
// Set rule: configure optional parameters for an element type
#set heading(numbering: "I.")
#set text(font: "New Computer Modern")

// Show-set rule: apply a set rule only to selected elements
#show heading: set text(navy)

// Show transform rule: replace/reshape element output
#show heading: it => block[#emph(it.body)]
```

## Common mistakes to avoid

- Calling things "tuples" (Typst only has arrays).
- Using `[]` for arrays (use `()` instead).
- Accessing array elements with `arr[0]` (use `arr.at(0)`).
- Omitting `#` in markup/content blocks (e.g., `text(...)[numbering(...)]` should be `text(...)[#numbering(...)]`).
- Using `#` inside code contexts (e.g., `figure(#image("x.png"))` in an argument list).
- Mixing up content blocks `[]` with code blocks `{}`.
- Forgetting to include the namespace when accessing imported variables/functions (e.g., use `color.hsl` instead of just `hsl`).
- Using LaTeX syntax (do **NOT** use `\begin{...}`, `\section`, or other LaTeX commands).
- Hallucinating environments (e.g., `tabular` does not exist; use `table`).


## Reference

Bundled documentation in `.kilo/skills/typst-author/docs/`:

- `docs/tutorial/writing-in-typst.md` — Getting started tutorial
- `docs/reference/syntax.md` — Complete syntax reference
- `docs/reference/styling.md` — Show/set rules and custom themes
- `docs/reference/scripting.md` — Scripting and runtime behavior
- `docs/guides/page-setup.md` — Page layout and margins
- `docs/guides/tables.md` — Table creation and formatting
- `docs/reference/foundations/array.md` — Array syntax
- `docs/reference/foundations/dictionary.md` — Dictionary syntax
- `docs/reference/foundations/content.md` — Content block syntax
- `docs/reference/foundations/module.md` — Multi-file project organization
- `docs/reference/introspection/query.md` — Query API for probes
- `docs/reference/introspection/metadata.md` — Metadata API for probes

## Scripts

This skill does not ship standalone scripts. It uses `typst compile` and `typst query` for validation, and `typstyle` for formatting. The workflow is implemented directly in the skill steps.


## Advanced features

- **Custom themes**: See [docs/reference/styling.md](docs/reference/styling.md) for theme creation.
- **Scripting**: Use Typst's scripting capabilities ([docs/reference/scripting.md](docs/reference/scripting.md)) for automatic generation.
- **Math and visualisation**: Reference [docs/reference/math/](docs/reference/math/) and [docs/reference/visualize/](docs/reference/visualize/) for formulas and diagrams.

### For large projects

When working on large projects, consider organizing the project across multiple files.

- Use `#include "file.typ"` to split into multiple files
- Relevant documentation: [docs/reference/foundations/module.md](docs/reference/foundations/module.md)
## Examples

### Example 1: Debug a compile error

**Request:** "Why is my table not rendering in Typst?"

**Action taken:** Check the error output, identify missing `#table()` context, fix by adding column definitions.

### Example 2: Quick document prototype

**Request:** "Write a simple invoice template in Typst"

**Action taken:** Produce standalone .typ file with grid layout, table, and basic formatting.



## Error Handling

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| "unknown font family" warnings | Font not installed or font path not set | Remove the font specification to use system defaults; warnings are non-fatal |
| "package not found" | Typo in package name or version | Verify exact package name and version on Typst Universe; check `@preview/package:version` syntax |
| "expected content, found ..." | Using code where markup is expected | Wrap in `#{ }` or use proper syntax |
| "expected expression, found ..." | Missing `#` in markup/content blocks | Add `#` (or `#(...)`) before code expressions inside `[...]` |
| "unknown variable" | Spelling error or missing import | Check variable spelling and ensure imports are correct |
| Array/dictionary errors | Wrong delimiter used | Use `()` for both arrays and dictionaries; dictionaries need `key: value` syntax; singleton arrays are `(elem,)`
