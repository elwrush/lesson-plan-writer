# Command: Build Excellent Lesson Plan

## Usage
`/build-excellent-lesson-plan <path/to/lesson.md>`

## What it does
1. Loads the `build-excellent-lesson-plans` skill
2. Reads the Markdown lesson plan file
3. Validates YAML frontmatter and stage structure
4. Runs Pandoc to convert Markdown → Typst via `templates/lesson-plan.typ`
5. Compiles with `typst` to PDF
6. Validates the output PDF content

## Output
PDF saved to `PDF/{subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`

## Example
```
/build-excellent-lesson-plan output/M3-LISTENING-GENDER-ROLES/gender-stereotypes.md
```
