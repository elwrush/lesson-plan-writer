---
name: write-lesson-plan
description: Interactively gathers teacher requirements and generates a lesson plan in JSON format. Use when a teacher asks to create a lesson plan.
---

# Skill: Write Lesson Plan

## Purpose
Interactively gather teacher requirements and generate a structured lesson plan in JSON format for later PDF generation via Quarto.

## Workflow

The workflow asks exactly **one question per turn**. Questions alternate between two input methods:

| Input method | When to use | How |
|---|---|---|
| **`question` tool with predefined options** | Only for fields with a known closed set: shape (A–G) and CEFR level (A1–C2) | Call `question` with `options` array. User clicks an option to select. |
| **Chat message** | All other fields: teacher, duration, topic, class, materials type, subfolder name, materials reference, answer key path, transcript path | Write the question directly in your response text. The user types the answer in the normal message input. |

**Critical rules:**
- If using the `question` tool and the user types a custom answer (rather than picking a predefined option), **use their answer literally**. Do NOT map it back to one of the predefined options.
- Never use the `question` tool for anything other than shape or CEFR level.
- After each answer, do a brief visible action (read a file, confirm the value) before asking the next question.

### Step 1: Greet the User
```
Welcome to the Lesson Plan Writer!
I'll help you create a structured lesson plan.
```

### Step 2: Shape (question tool with options)
Display the shapes in your response text, then call `question` with options A–G:

| Shape | Name |
|-------|------|
| A | Text-based Presentation of Language |
| B | Language Practice |
| C | Test-Teach-Test |
| D | Situational Presentation (PPP) |
| E | Receptive Skills (Traditional) |
| F | Productive Skills (Traditional) |
| G | Task-Based Learning/TBT |

After the user answers, read the corresponding shape template from `knowledge-base/lesson plan shapes/json/shape-{letter}.json`. Report back: "Loaded Shape {letter} — {shape name}."

### Step 3: Teacher name (chat)
Default: "Ed Rush". Confirm with the teacher: "Teacher name: Ed Rush — is that still correct?" If they say no, ask for the new name.

### Step 4: Lesson length (chat)
Default: 46 minutes. Confirm with the teacher: "Lesson length: 46 minutes — is that still correct?" If they say no, ask for the new duration.

### Step 5: CEFR level (question tool with options)
Call `question` with options: A1, A2, B1, B2, C1, C2. Each with appropriate description.

### Step 6: Topic (chat)
Write: "What's the lesson topic?" in your response text. Wait for the user's chat reply.

### Step 7: Class (chat)
Write: "What's the class name or identifier?" in your response text. Wait for the user's chat reply.

### Step 8: Materials type (chat — free text, NOT selectable)
Write: "What type of materials will you use? (e.g., bespoke, existing coursebook, or none for first-day/intro lessons)" in your response text. Wait for the user's chat reply. Accept whatever they say — do NOT force-fit into predefined categories.

### Step 9: Input subfolder (chat)
Write: "What's the input subfolder name? (under inputs/)" in your response text. Wait for the user's chat reply.

After receiving the name:
1. Check if the folder exists under `inputs\`. If not, create it.
2. List all files in the folder using `read` or `glob`.
3. Read files to check for a materials reference (book name, unit, page numbers).
4. Check for answer keys ("Answer", "Answers:", "**Answer:**" patterns, or files with "answer"/"key" in name).
5. Check for transcripts ("Transcript", "Audio transcript" patterns, or files with "transcript" in name).

### Step 10: Resolve remaining items (chat only)
All asked directly in chat. Only ask if the item was not auto-detected in Step 9:
- If materials reference not found: "What's the materials reference for this lesson?"
- If answer key not found: "Do you have an answer key? If so, what path?"
- If transcript not found and audio/video files exist: "Do you have a transcript? If so, what path?"
- If transcript not found and no audio/video files: set to "none" automatically — do NOT ask.

### Step 11: Pre-teach vocabulary selection (human-in-the-loop)

This step only applies when the lesson involves a reading or listening text (transcript). If there is no text, skip to Step 12.

1. **Read the transcript/reading text** from the input materials.
2. **Identify 8-10 candidate words** that seem particularly difficult for the target CEFR level, using your own training data and linguistic judgement. Prioritise:
   - Words central to understanding the text (blocking vocabulary)
   - Words likely to be unfamiliar at the learners' level
   - Content words (nouns, verbs, adjectives) over function words
   - Do NOT include words that are clearly below the target level
3. **Verify each candidate** — before presenting, use `grep` or `bash` to confirm every candidate word actually appears in the transcript text. Remove any word not found. This prevents hallucinated suggestions.
4. **Present the candidates** to the teacher as a simple numbered list of word forms only (no definitions). Example:
   ```
   Here are words from the transcript that may be challenging for B1 learners:
   1. persuade
   2. trust
   3. session
   ...
   Which ones should we pre-teach? (max 5, or "none")
   ```
4. **Teacher selects** — the teacher picks 0-5 words from the list. Use their selection exactly.
5. If the teacher says "none" or "skip", set pre-teach vocab to none.

### Step 12: Check for special requests (chat)

### Step 13: Generate and Write Lesson Plan

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

### Step 13: Confirm Output
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
- The `materials` field must use a concise reference format with each separate item as a bullet point, using Typst list syntax (e.g., "- Coursebook, Unit 3, pp 10-12\n- Worksheet: gap-fill task"). Use `- ` prefix with `\n` between items in the JSON string. NOT a descriptive summary of file contents.
- **CRITICAL: Only include items explicitly stated by the user in materials.** Do NOT add derived/ancillary assets (e.g., logo files, background images, downloaded photos, slide assets). These are implementation details, not lesson materials.
- If the materials reference is not found in the input folder files, ask the user for it
- **In the procedure text, all exercise numbers must be precisely identified** (e.g., "Exercise A1" not "A Vocabulary preview", "While you watch Q1-Q3" not "While you watch", "Exercise C2" not "C matching"). Use the exact numbering from the source material.
- **Rule: When the user types a custom answer in the question tool, accept it literally. Do not remap to a predefined option.**
- **Language quality: Write with temperature 0.7. Use natural, idiomatic English. Vary sentence structure. Avoid robotic patterns.**
- **Answer key formatting: The answer key file must use proper markdown headers and paragraph breaks throughout. The OCR transcription section (if present) must have headers and paragraphs matching the original document structure — never leave it as a single run-on block of text.**
- **CRITICAL — Append only: When adding an answer key to an existing markdown file, ALWAYS append to the end of the file. NEVER overwrite or replace the file content. The original document text is the source of truth for all content verification. If the file needs reformatting, edit selectively — do not rewrite the entire file.**
- **Answer key file content depends on lesson type:**
  - **Reading lessons**: Answer key only + transcript of any YouTube videos used in the lesson.
  - **Listening lessons**: Full transcript of the audio/video + answer key.
  - The `answer_key` field in the JSON must point to a file that contains ONLY the answer key content (and video transcript if applicable), NOT the full source document. Create a separate `answer_key.md` file for the answer key content if the source document also contains the full lesson text.

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