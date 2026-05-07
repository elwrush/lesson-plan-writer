🔹 1. SPECIFICATION

Feature Name: handwriting-ocr-to-json

Input: Single file path to an A4 scan containing handwriting (.png, .jpg, .jpeg, .pdf)

Output: JSON file named <input\_stem>.json in the same directory

Processing Pipeline:

Preprocess: Resize \& compress image to an "economic minimum" for vision/OCR while preserving handwriting legibility.

Transcribe: Extract handwritten text via OCR or vision model.

Serialize: Write to JSON with exact schema: {"student\_text": "<transcribed\_string>"}

Constraints:

Target resolution: 1024×1448 px (A4 ratio @ \~100 DPI)

Max file size after compression: ≤ 300 KB

Strip EXIF/metadata

Fallback to null or explicit error string if transcription fails

No external dependencies that require paid API keys unless explicitly configured

🔹 2. ACCEPTANCE CRITERIA

ID

Criterion

Validation Method

AC1

Output JSON is created with exact naming <input\_stem>.json

File existence + name check

AC2

JSON parses successfully and contains exactly one top-level key: student\_text

json.loads() + len(keys) == 1

AC3

student\_text value is a string (or null on failure)

Type check

AC4

Preprocessed image meets size/dimension constraints

PIL.Image size check + os.path.getsize()

AC5

Handles .png, .jpg, .jpeg, .pdf without crashing

Format-specific test runs

AC6

No unhandled exceptions; failures log to stderr or console

Exception tracing + exit code

AC7

Token-efficient: image sent to OCR/vision is ≤ 300 KB

Log/verify payload size

🔹 3. TEST CASES

ID

Input

Expected Output

Validation

TC-01

sample\_clean.png (2.4 MB, legible print)

sample\_clean.json → {"student\_text": "Dear teacher, I finished the worksheet..."}

Text matches ground truth ± minor punctuation

TC-02

sample\_faded.pdf (1 page, low contrast)

sample\_faded.json → {"student\_text": "\[partial] ...math homework due Friday..."}

Acceptable degradation; no crash

TC-03

sample\_skewed.jpg (rotated 15°)

sample\_skewed.json → valid transcription or null

OCR handles rotation or fails gracefully

TC-04

sample\_corrupted.png (broken header)

No JSON created, error logged

Script exits cleanly, logs to console

TC-05

Batch: 3 files in ./test\_inputs/

3 corresponding JSONs in ./test\_outputs/

All pass AC1–AC7

🔹 4. HOW TO FEED THIS TO CLAUDE CODE

Use this exact prompt structure. Claude Code thrives on constraint-bound execution.

text

123456789101112131415

🔹 5. IMPLEMENTATION NOTES (Token-Economic Reality)

"Economic minimum" ≠ blind compression. Handwriting loses legibility fast below \~900px width. Target 1024px width, convert to JPEG or WebP, quality 70-75. This typically drops a 5MB PNG to \~150–250KB.

Local OCR vs Vision API:

pytesseract + opencv (deskew, threshold) = \~0 tokens, \~2–5 sec/file

easyocr or paddleocr = better handwriting accuracy, still local

Claude Vision / GPT-4V = high accuracy but burns tokens. Only use if local OCR fails, and always send the compressed version.

JSON naming: Strip extension safely: Path(input).stem + ".json"

🔹 6. REVIEW CHECKLIST (Post-Execution)

When Claude Code returns the code, verify against your spec, not token counts:

Does the script create <input>.json exactly?

Does json.load() reveal only {"student\_text": "..."}?

Is the preprocessed image ≤ 300 KB and ≤ 1024px wide?

Do all 5 test cases pass or fail explicitly with logs?

Is error handling deterministic (no silent failures)?

Can you run python transcribe\_handwriting.py --input scan.pdf and get correct output?

If any item fails, reply to Claude Code with:

"AC\[X] failed. Expected \[Y], got \[Z]. Fix and re-run tests."

This keeps you in control, bounds the agent’s behavior, and guarantees review against constraints. Let me know if you want the actual Python scaffolding pre-written to drop into your repo.

