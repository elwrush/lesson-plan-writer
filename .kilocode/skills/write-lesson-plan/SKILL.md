---
name: write-lesson-plan
description: Interactively gathers teacher requirements and generates a lesson plan in JSON format. Use when a teacher asks to create a lesson plan.
---

# Skill: Write Lesson Plan

## Purpose
Interactively gather teacher requirements and generate a structured lesson plan in JSON format for later PDF generation via Quarto.

## Workflow

Two input methods depending on the field type:

| Field type | How to ask | Tool |
|---|---|---|
| **Selectable** (shape, CEFR level, materials type) | Use `question` tool with predefined options — user clicks to pick | `question` call with `options` array |
| **Free text** (teacher, duration, topic, class, subfolder, materials reference, answer key path, transcript path) | Ask directly in the chat message — user types in the normal message input, NOT in a `question` tool form | Plain text message, wait for user reply |

**Rules:**
- One field at a time. Ask, wait for reply, then move to the next.
- For selectable fields: use `question` tool with well-defined `options`, each with `label` + `description`.
- For free-text fields: do NOT use `question` tool. Just write the question in your response text. The user will reply in the chat input.
- After each answer, do a brief visible action (read a file, confirm receipt) before the next question, so the user sees progress.

### Step 1: Greet the User
```
Welcome to the Lesson Plan Writer!
I'll help you create a structured lesson plan.
```

### Step 2: Ask About the Shape (selectable)
Display the available lesson plan shapes in your message text:

| Shape | Name |
|-------|------|
| A | Text-based Presentation of Language |
| B | Language Practice |
| C | Test-Teach-Test |
| D | Situational Presentation (PPP) |
| E | Receptive Skills (Traditional) |
| F | Productive Skills (Traditional) |
| G | Task-Based Learning/TBT |

Use `question` tool with options A–G. After the user answers, read the corresponding shape template file from `knowledge-base/lesson plan shapes/json/shape-{letter}.json` and report back: "Loaded Shape {letter} — {shape name}."

### Step 3: Collect Free-Text Basic Info (one per chat message)
Ask each by writing the question directly in your response text. Do NOT use `question` tool for these:
1. **Teacher name** — "What's the teacher name?"
2. **Lesson length** — "Lesson length in minutes?"
3. **Topic** — "What's the lesson topic?"
4. **Class** — "What's the class name or identifier?"

### Step 4: CEFR Level (selectable)
Use `question` tool with predefined options: A1, A2, B1, B2, C1, C2.

### Step 5: Materials Type (selectable)
Use `question` tool with options: Bespoke, Existing.

### Step 6: Input Subfolder (free text)
Ask in chat: "What's the input subfolder name? (under inputs/)" — do NOT use `question` tool.

After receiving the name, check if the folder exists under `inputs\`. If not, create it. Scan its contents:
- List all files
- Read files for materials reference (book name, unit, page numbers)
- Read files for answer keys (look for "Answer", "Answers:", "**Answer:**" patterns, or files with "answer"/"key" in name)
- Read files for transcripts (look for "Transcript", "Audio transcript", or files with "transcript" in name)

### Step 7: Resolve Remaining Items (free text, chat only)

### Step 8: Generate and Write Lesson Plan

#### Output Path
```
C:\PROJECTS\LESSON PLAN WRITER 3\output\{input_subfolder}\{mmddyy}-{topic}-lesson-plan.json
```
Where:
- `input_subfolder` is the user-provided subfolder name (always under `C:\PROJECTS\LESSON PLAN WRITER 3\inputs`)
- `mmddyy` is today's date
- `topic` is the normalized topic name (lowercase, spaces replaced with hyphens)

#### JSON Structure
```json
{
  "teacher": "[Teacher Name]",
  "duration": "[X] minutes",
  "date": "[mmddyy]",
  "topic": "[Topic]",
  "objective": "[Auto-generated based on shape template + topic + materials]",
  "materials": "[Materials reference]",
  "lesson_plan": {
    "shape": "[A/B/C/D/E/F/G]",
    "shape_name": "[Shape name]",
    "cefr_level": "[CEFR Level]",
    "class": "[Class]",
    "stages": [
      {
        "stage_number": 1,
        "stage": "[Stage name]",
        "stage_aim": "[Aim]",
        "procedure": "[Procedure steps]",
        "time": [minutes],
        "interaction": "[T-Ss/Ss-Ss/S]"
      }
    ]
  },
  "transcript": "[Transcript location or 'none']",
  "answer_key": "[Answer key location or 'none']",
  "slideshow_url": "[URL or empty]",
  "cefr_level": "[CEFR Level]",
  "class": "[Class]"
}
```

#### Objective Auto-generation
Use the shape's `main_aim_format` template combined with:
- Target language from materials (if identifiable)
- Topic provided by user
- CEFR level

### Step 9: Confirm Output
Inform the user where the lesson plan has been saved.

## Template Files Location
Lesson plan shape templates are stored at:
```
C:\PROJECTS\LESSON PLAN WRITER 3\knowledge-base\lesson plan shapes\json\
```

Available templates:
- `shape-a.json` - Text-based Presentation of Language
- `shape-b.json` - Language Practice
- `shape-c.json` - Test-Teach-Test
- `shape-d.json` - Situational Presentation (PPP)
- `shape-e.json` - Receptive Skills (Traditional)
- `shape-f.json` - Productive Skills (Traditional)
- `shape-g.json` - Task-Based Learning/TBT

## Notes
- Always use today's date in `mmddyy` format for the filename
- Normalize topic names for filenames (lowercase, spaces to hyphens)
- Set `transcript` and `answer-key` to "none" if not provided
- `slideshow_url` is an optional field; populated by `lesson-plan-to-reveal` after deployment
- The `lesson plan` section uses the selected shape's template structure
- **CRITICAL: Always read the input folder contents BEFORE asking about materials, answer keys, or transcripts**
- Scan markdown files for answer patterns ("Answer:", "**Answer:**", "Answers:") to auto-detect answer keys
- Scan for transcript patterns ("Transcript", "Audio transcript") to auto-detect transcripts
- Only ask the user about answers/transcripts if they are NOT found in the input folder
- The `materials` field must use a concise reference format (e.g., "OFD 3, Workbook, pp 4-5"), NOT a descriptive summary of file contents
- If the materials reference is not found in the input folder files, ask the user for it
- **Language quality: Write with temperature 0.7. Use natural, idiomatic English. Vary sentence structure. Avoid robotic patterns.**

## Writing Style

### Stage Aim Quality

Stage aims must be written in natural, idiomatic English — never in the deterministic style of a template. The LLM should vary phrasing across stages.

**UNACCEPTABLE (robotic/deterministic)**:
- "To lead-in to the topic of generational differences"
- "To reading for gist"
- "To reading for detail and specific information"
- "To post-reading speaking task"
- "To wrap-up and reflection"

**ACCEPTABLE (natural/probabilistic)**:
- "To activate learners' interest in the theme of generational differences"
- "To get the general idea of the text"
- "To identify key facts and supporting details"
- "To discuss ideas from the reading and share personal responses"
- "To reflect on key takeaways and consolidate learning"

### Writing Principles

1. **Vary sentence openers** — do not start every aim with "To" followed by a verbatim stage name
2. **Use natural collocations** — e.g., "get the gist", "activate interest", "draw out", "build on", "set the scene"
3. **Write aims as meaningful teaching intentions** — not mechanical labels
4. **Adapt language to CEFR level** — simpler phrasing for A1/A2, more sophisticated for B2/C1
5. **Use temperature 0.7** — produce varied, human-sounding output rather than deterministic template fills
