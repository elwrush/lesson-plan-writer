---
name: write-lesson-plan
description: Interactively gathers teacher requirements and generates a lesson plan in JSON format. Use when a teacher asks to create a lesson plan.
---

# Skill: Write Lesson Plan

## Purpose
Interactively gather teacher requirements and generate a structured lesson plan in JSON format for later PDF generation via Quarto.

## Workflow

### Step 1: Greet the User
```
Welcome to the Lesson Plan Writer!
I'll help you create a structured lesson plan. Let me ask you a few questions to customize it for your needs.
```

### Step 2: Enumerate Lesson Plan Shapes
Display the available lesson plan shapes:

| Shape | Name |
|-------|------|
| A | Text-based Presentation of Language |
| B | Language Practice |
| C | Test-Teach-Test |
| D | Situational Presentation (PPP) |
| E | Receptive Skills (Traditional) |
| F | Productive Skills (Traditional) |
| G | Task-Based Learning/TBT |

Ask the user to identify their choice. This is the only question in this step — issue exactly one `question` call.

### Step 3: Collect Basic Information (Batch)

Issue a **single `question` call** containing ALL of the following fields together:
- Teacher name
- Lesson length (in minutes)
- CEFR level (pre-define options: A1, A2, B1, B2, C1, C2)
- Topic of lesson
- Class (class name/identifier)
- Materials type (bespoke or existing)

Do NOT split this into multiple question calls. Do NOT ask about materials reference here — that belongs in Step 4.

### Step 4: Collect Input Subfolder, Scan, and Gather Remaining Info

**Step 4a:** Issue a single `question` call asking for the input subfolder name (the subfolder under `C:\PROJECTS\LESSON PLAN WRITER 3\inputs\`).

**Step 4b: Scan the input folder contents** using `read` or `glob`:
- List all files in the input folder
- Read the files to check if they contain a materials reference (e.g., book name, unit, page numbers)
- If a materials reference is found in the files, use it for the `materials` field — do NOT ask the user
- Check if any file contains answers/answer keys (look for "Answer", "Answers:", "**Answer:**" patterns in markdown files, or files with "answer" or "key" in the name)
- Check if any file contains transcripts (look for "Transcript", "Audio transcript", or similar patterns, or files with "transcript" in the name)
- If answers are found in the folder, set `answer-key` to the file path automatically — do NOT ask the user
- If transcripts are found in the folder, set `transcript` to the file path automatically — do NOT ask the user

**Step 4c: Batch any remaining questions.** After scanning, issue a **single `question` call** for any remaining items not auto-detected:
- If no materials reference was found in files, include: "What is the materials reference for this lesson? (e.g., 'OFD 3, Workbook, pp 4-5')"
- If no answers were found, include: "No answer key found. Do you have one? If so, provide the path, or say 'none'."
- If no transcripts were found **and** audio/video files exist in the folder, include: "No transcript found. Do you have one? If so, provide the path, or say 'none'."
- If no transcripts were found and there are NO audio/video files, set `transcript` to "none" automatically — do NOT ask.

Do NOT split Step 4c into multiple question calls. All unresolved items go into one batch.

### Step 5: Generate and Write Lesson Plan

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

### Step 6: Confirm Output
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
