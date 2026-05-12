---
name: write-lesson-plan
description: Interactively gathers teacher requirements and generates a lesson plan in JSON format. Use when a teacher asks to create a lesson plan.
---

# Skill: Write Lesson Plan

## Purpose
Interactively gather teacher requirements and generate a structured lesson plan in JSON format for later PDF generation via Quarto.

## Workflow

The entire information-gathering phase must use exactly **two question calls maximum**:

1. **Round 1** (single batch): Display shapes + ask EVERYTHING in one `question` call
2. **Round 2** (single batch, if needed): After folder scan, ask any remaining items not auto-detected

Do NOT split into more than two rounds. The user must not see back-to-back questions.

### Step 1: Greet the User
```
Welcome to the Lesson Plan Writer!
I'll help you create a structured lesson plan.
```

### Step 2: Collect Everything (Single Batch Question)

Display the available lesson plan shapes as part of the question:
| Shape | Name |
|-------|------|
| A | Text-based Presentation of Language |
| B | Language Practice |
| C | Test-Teach-Test |
| D | Situational Presentation (PPP) |
| E | Receptive Skills (Traditional) |
| F | Productive Skills (Traditional) |
| G | Task-Based Learning/TBT |

Then issue **exactly one `question` call** containing ALL of the following fields:
- Shape selection (A–G, with the table as context)
- Teacher name
- Lesson length (in minutes)
- CEFR level (pre-define options: A1, A2, B1, B2, C1, C2)
- Topic of lesson
- Class (class name/identifier)
- Materials type (bespoke or existing)
- Input subfolder name (the subfolder under `C:\PROJECTS\LESSON PLAN WRITER 3\inputs\`)

**Critical: All of the above goes into a single `question` call.** Do NOT split shape into its own question. Do NOT split subfolder into its own question. One call.

### Step 3: Scan Input Folder and Batch Remaining Questions

**After receiving the Round 1 answers:**
1. Check if the subfolder exists; if not, create it
2. List all files in the input folder using `read` or `glob`
3. Read the files to check if they contain a materials reference (e.g., book name, unit, page numbers)
4. If materials reference is found in files, use it — do NOT ask
5. Check for answer keys (look for "Answer", "Answers:", "**Answer:**" patterns, or files with "answer"/"key" in name)
6. Check for transcripts (look for "Transcript", "Audio transcript", or files with "transcript" in name)
7. If answers found, set `answer-key` to the file path automatically
8. If transcripts found, set `transcript` to the file path automatically

**If any items remain unresolved after scanning**, issue a **single `question` call** containing all of them:
- If no materials reference found: "What is the materials reference? (e.g., 'OFD 3, Workbook, pp 4-5')"
- If no answer key found: "No answer key found. Do you have one? Provide path or say 'none'."
- If no transcript found AND audio/video files exist: "No transcript found. Do you have one? Provide path or say 'none'."
- If no transcript found AND no audio/video files: set to "none" automatically — do NOT ask

If ALL items were auto-detected during scanning, issue zero question calls and proceed directly to Step 4.

### Step 4: Generate and Write Lesson Plan

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

### Step 5: Confirm Output
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
