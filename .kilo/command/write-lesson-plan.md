---
description: Interactively gathers teacher requirements and generates a lesson plan in JSON format. Asks one question per turn using chat or the question tool. Outputs to output/{input_subfolder}/{mmddyy}-{topic}-lesson-plan.json.
---

# Command: Write Lesson Plan

## Usage
`/write-lesson-plan`

No arguments needed. All input is gathered interactively.

## What it does
1. Loads the `write-lesson-plan` skill (full 13-step interactive workflow)
2. Prompts the teacher through shape selection, teacher name, duration, CEFR level, topic, class, materials, input folder, answer key, and transcript
3. Reads input folder contents to auto-detect materials references, answer keys, and transcripts
4. Generates a structured JSON lesson plan using the selected shape template
5. Outputs to `output/{input_subfolder}/{mmddyy}-{topic}-lesson-plan.json`

## Workflow

### Step 1: Load the skill
`skill write-lesson-plan`

This loads all 13 steps of the interactive workflow, including shape templates, question tool configuration, input folder scanning rules, and JSON schema requirements.

### Step 2: Follow the skill's interactive workflow
The skill asks exactly one question per turn. Follow its sequence:

1. **Greeting** — welcome message
2. **Shape** (question tool) — A–G with descriptions. Read the selected shape template from `knowledge-base/lesson plan shapes/json/shape-{letter}.json`
3. **Teacher name** (chat) — free text
4. **Duration** (chat) — minutes (integer)
5. **CEFR level** (question tool) — A1–C2
6. **Topic** (chat) — free text
7. **Class** (chat) — free text
8. **Materials type** (chat) — free text
9. **Input subfolder** (chat) — folder name under `inputs/`. Read folder contents, scan for materials reference, answer keys, and transcripts
10. **Resolve remaining items** (chat) — only for items not auto-detected in step 9
11. **Special requests** (chat) — ask if user has any additional requirements
12. **Generate JSON** — assemble and write the file
13. **Confirm** — report output path

### Step 3: Generate the output file
```
output/{input_subfolder}/{mmddyy}-{topic}-lesson-plan.json
```

### Step 4: Report
Inform the user where the lesson plan was saved. Suggest next steps:
- `/create-pdf-lesson-file <path>` to generate a PDF
- `/lesson-plan-to-reveal <path>` to generate a slideshow

## Input Scanning Rules
- Always read the input folder contents BEFORE asking about materials, answer keys, or transcripts
- Scan markdown files for "Answer:", "**Answer:**", "Answers:" patterns → auto-detect answer key
- Scan for "Transcript", "Audio transcript" patterns → auto-detect transcript
- Only ask user about items NOT found in the input folder
- If no audio/video files exist, skip transcript question entirely (set to "none")

## Edge cases
- **User cancels mid-flow**: No partial file is written
- **Shape JSON not found**: "Error: Shape template not found at knowledge-base/lesson plan shapes/json/shape-{letter}.json"
- **Invalid input folder**: Create it with a warning: "Created inputs/{subfolder}/ — it was empty"
- **User types custom answer in question tool**: Accept literally, do NOT remap to predefined options
- **Empty topic name**: "Topic cannot be empty — please provide a lesson topic"
- **Non-numeric duration**: "Duration must be a number in minutes"
