"""
json_to_pdf.py - Convert lesson plan JSON to PDF using Typst CLI

Usage:
    python json_to_pdf.py <json_file_path> [--output-dir <dir>]

Example:
    python scripts/json_to_pdf.py output/substitute-lesson-1-M3/050726-what-connects-us-lesson-plan.json
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
PDF_OUTPUT_DIR = PROJECT_ROOT / "PDF"

# Roboto OTF font directory (TinyTeX bundled)
ROBOTO_FONT_DIR = Path(
    os.path.expandvars(r"%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto")
)

# Required fields in lesson plan JSON
REQUIRED_FIELDS = [
    "teacher",
    "duration",
    "date",
    "topic",
    "materials",
    "lesson_plan",
]

REQUIRED_LESSON_PLAN_FIELDS = [
    "shape",
    "shape_name",
    "cefr_level",
    "class",
    "stages",
]

REQUIRED_STAGE_FIELDS = [
    "stage_number",
    "stage",
    "stage_aim",
    "procedure",
    "time",
    "interaction",
]


def validate_json(data):
    """Validate lesson plan JSON against required schema."""
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not data[field]:
            errors.append(f"Empty required field: {field}")

    if "lesson_plan" in data and isinstance(data["lesson_plan"], dict):
        lp = data["lesson_plan"]
        for field in REQUIRED_LESSON_PLAN_FIELDS:
            if field not in lp:
                errors.append(f"Missing required lesson_plan field: {field}")
            elif field == "stages" and (not lp[field] or not isinstance(lp[field], list)):
                errors.append("lesson_plan.stages must be a non-empty array")

        if "stages" in lp and isinstance(lp["stages"], list):
            for i, stage in enumerate(lp["stages"]):
                for field in REQUIRED_STAGE_FIELDS:
                    if field not in stage:
                        errors.append(f"Missing required field in stage {i + 1}: {field}")
    else:
        errors.append("lesson_plan must be a valid object")

    return errors


def normalize_topic(topic):
    """Normalize topic for filename: lowercase, spaces to hyphens."""
    return topic.lower().replace(" ", "-").replace("/", "-")


def get_output_path(json_path, topic):
    """Generate output PDF path: PDF/{input_subfolder}/{mmddyy}-{topic}-lesson-plan.pdf"""
    json_path = Path(json_path)

    try:
        output_idx = json_path.parts.index("output")
        subfolder = json_path.parts[output_idx + 1]
    except (ValueError, IndexError):
        subfolder = "default"

    today = datetime.now().strftime("%m%d%y")
    normalized_topic = normalize_topic(topic)
    filename = f"{today}-{normalized_topic}-lesson-plan.pdf"

    output_dir = PDF_OUTPUT_DIR / subfolder
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir / filename


def escape_typst_string(text):
    """Escape text for safe inclusion in a Typst string literal."""
    if not text:
        return ""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def format_date(date_str):
    """Convert MMDDYY to 'D Month, YYYY' format."""
    date_str = date_str.strip()
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    if len(date_str) == 6 and date_str.isdigit():
        mm = int(date_str[0:2])
        dd = int(date_str[2:4])
        yy = int(date_str[4:6])
        year = 2000 + yy
        if 1 <= mm <= 12 and 1 <= dd <= 31:
            return f"{dd} {months[mm - 1]}, {year}"

    return date_str


def clean_procedure(text):
    """Remove minute indicators from procedure text (e.g. '3 min.', '2 min.')."""
    text = re.sub(r",?\s*\d+\s*min\.?\s*$", "", text)
    text = re.sub(r",?\s*\d+\s*min\.", ".", text)
    text = re.sub(r"\s*\d+\s*min\.?\s*$", "", text)
    text = re.sub(r"(\d+)\s*min\.?\s*\n", r"\n", text)
    return text.strip()


def humanize_stage_aim(aim):
    """Rewrite robotic stage aims into natural English."""
    mappings = {
        "To lead-in": "To activate interest",
        "To lead in": "To activate interest",
        "To reading for gist": "To understand the general idea of the text",
        "To reading for detail and specific information": "To identify key facts and details in the text",
        "To reading for inference and conclusion": "To draw inferences and conclusions from the text",
        "To post-reading": "To discuss and apply ideas",
        "To wrap-up and reflection": "To reflect on what was learned and consolidate understanding",
        "To wrap-up": "To reflect on what was learned",
        "To reading for": "To practise reading for",
    }

    if aim in mappings:
        return mappings[aim]

    for pattern, replacement in sorted(mappings.items(), key=lambda x: -len(x[0])):
        if aim.startswith(pattern):
            return aim.replace(pattern, replacement, 1)

    return aim


def render_typst(typ_path, output_path):
    """Render the .typ file to PDF using Typst CLI."""
    typ_path = Path(typ_path)
    output_path = Path(output_path)

    cmd = [
        "typst",
        "compile",
        str(typ_path),
        str(output_path),
        "--font-path",
        str(ROBOTO_FONT_DIR),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            print(f"Typst compile failed (exit code {result.returncode}):")
            print(result.stderr)
            return False

        print(f"PDF created: {output_path}")
        return True

    except subprocess.TimeoutExpired:
        print("Error: Typst compile timed out")
        return False
    except FileNotFoundError:
        print("Error: Typst CLI not found. Install from https://github.com/typst/typst")
        return False


def build_typ_content(data, json_path=None):
    """Build .typ file content from lesson plan data. No Jinja2.

    If json_path is provided, relative paths in answer_key/transcript
    fields are resolved against json_path.parent instead of the CWD.
    """
    base_dir = Path(json_path).parent if json_path else Path.cwd()
    lines = []

    # Page setup (no header — logo band is page-1 content only)
    lines.append('#set text(font: "Roboto", size: 10pt)')
    lines.append("#set par(leading: 0.55em)")
    lines.append("")
    lines.append("#show: it => {")
    lines.append("  set page(margin: (x: 0.75in, top: 0.75in, bottom: 0.75in))")
    lines.append("  it")
    lines.append("}")
    lines.append("")
    lines.append("#block(")
    lines.append("  stroke: (bottom: 0.5pt + black),")
    lines.append("  inset: (bottom: 6pt, top: 12pt),")
    lines.append("  grid(")
    lines.append("    columns: (1fr, 1fr, 1fr),")
    lines.append("    align: (left + horizon, center + horizon, right + horizon),")
    lines.append('    image("Image_20260324_141022.png", height: 1.35cm),')
    lines.append('    align(center, text(size: 14pt, weight: "bold")[Lesson Plan]),')
    lines.append('    image("cambridge.png", height: 1.8cm),')
    lines.append("  ),")
    lines.append(")")
    lines.append("#v(0.3em)")
    lines.append("")
    lines.append("= Lesson Information")
    lines.append("")
    topic = data.get("topic", "")
    lines.append(f"*Topic:* {topic}")
    lines.append("")

    # Info table
    teacher = data.get("teacher", "")
    formatted_date = format_date(data.get("date", ""))
    lesson_plan = data.get("lesson_plan", {})
    class_name = lesson_plan.get("class", "")
    duration = data.get("duration", "")
    cefr = lesson_plan.get("cefr_level", "")
    shape = lesson_plan.get("shape", "")
    shape_name = lesson_plan.get("shape_name", "")
    materials = data.get("materials", "")
    slideshow_url = data.get("slideshow_url", "")
    objective = data.get("objective", "")

    lines.append("#table(")
    lines.append("  columns: (auto, 1fr, auto, 1fr),")
    lines.append("  stroke: 1pt,")
    lines.append(f"  [*Teacher:*], [{teacher}],")
    lines.append(f"  [*Date:*], [{formatted_date}],")
    lines.append(f"  [*Class:*], [{class_name}],")
    lines.append(f"  [*Duration:*], [{duration}],")
    lines.append(f"  [*CEFR Level:*], [{cefr}],")
    lines.append(f"  [*Lesson Shape:*], [{shape} ({shape_name})],")
    lines.append(f"  [*Materials:*], table.cell(colspan: 3)[{materials}],")
    lines.append(f"  [*Slideshow URL:*], table.cell(colspan: 3, fill: luma(220))[{slideshow_url}],")
    lines.append(")")
    lines.append("")
    lines.append("#v(0.5em)")
    lines.append("")

    # Lesson Aim
    lines.append("= Lesson Aim")
    lines.append("")
    lines.append(f"#block(stroke: (left: 2pt + black), inset: 8pt, [{objective}])")
    lines.append("")
    lines.append("#v(0.5em)")
    lines.append("")

    # Lesson Stages
    lines.append("= Lesson Stages")
    lines.append("")
    lines.append("#{")
    lines.append("  table(")
    lines.append("    columns: (auto, 1fr, 2fr, auto),")
    lines.append("    stroke: 1pt,")
    lines.append("    table.header([*Time*], [*Goal*], [*Procedure*], [*Int*]),")

    stages = lesson_plan.get("stages", [])
    if stages:
        lines.append("    ..(")
        for st in stages:
            aim = humanize_stage_aim(st.get("stage_aim", ""))
            proc = clean_procedure(st.get("procedure", ""))
            stage_num = st.get("stage_number", "")
            stage_name = st.get("stage", "").upper()
            time_val = st.get("time", "")
            interaction = st.get("interaction", "")

            lines.append("      table.cell(colspan: 4, fill: luma(230))[")
            lines.append(f"        *STAGE {stage_num}: {stage_name}*")
            lines.append("      ],")
            lines.append(f"      [{time_val} min],")
            lines.append(f"      [{aim}],")
            lines.append(f"      [{proc}],")
            lines.append(f"      [{interaction}],")
        lines.append("    ),")
    else:
        lines.append("    (),")

    lines.append("  )")
    lines.append("}")
    lines.append("")

    # Transcript (only .typ files accepted — markdown intermediary is forbidden)
    transcript = data.get("transcript", "")
    if transcript and transcript != "none":
        transcript_path = Path(transcript)
        if not transcript_path.is_absolute():
            transcript_path = (base_dir / transcript).resolve()
        if transcript_path.exists() and transcript_path.suffix == ".typ":
            try:
                transcript_content = transcript_path.read_text(encoding="utf-8")
                lines.append("#pagebreak()")
                lines.append("")
                lines.append("= Transcript")
                lines.append("")
                lines.append(transcript_content)
            except Exception:
                pass

    # Answer Key (only .typ files accepted — markdown intermediary is forbidden)
    answer_key = data.get("answer_key", "")
    if answer_key and answer_key != "none":
        answer_key_path = Path(answer_key)
        if not answer_key_path.is_absolute():
            answer_key_path = (base_dir / answer_key).resolve()
        if answer_key_path.exists() and answer_key_path.suffix == ".typ":
            try:
                ak_content = answer_key_path.read_text(encoding="utf-8")
                lines.append("#pagebreak()")
                lines.append("")
                lines.append("= Answer Key")
                lines.append("")
                lines.append(ak_content)
            except Exception:
                pass

    return "\n".join(lines)


def render_template(data):
    """Render the .typ content from lesson plan data. No Jinja2."""
    return build_typ_content(data)


def fix_mojibake_chars(text):
    """Replace known mojibake character sequences with correct Unicode.

    When UTF-8 bytes (especially E2 80 9X sequences for dashes and quotes)
    are misinterpreted as Latin-1/Windows-1252 and then re-encoded as UTF-8,
    the result is valid Unicode but wrong characters like 'â€™' instead of "'".
    This function detects and replaces those patterns.
    """
    # Map of mojibake sequences → intended Unicode character
    # The sequence is: â (U+00E2) + € (U+20AC) + third byte read as Latin-1
    _mojibake_map = {
        # â€™ → ' (right single quote, U+2019)
        "\u00e2\u20ac\u2122": "\u2019",
        # â€œ → " (left double quote, U+201C)
        "\u00e2\u20ac\u0153": "\u201c",
        # â€" → " (right double quote, U+201D)
        "\u00e2\u20ac\u201d": "\u201d",
        # â€â€œ → – (en dash, U+2013) — double corruption pattern
        "\u00e2\u20ac\u00e2\u20ac\u0153": "\u2013",
        # â€â€" → – (en dash, U+2013)
        "\u00e2\u20ac\u00e2\u20ac\u201d": "\u2013",
        # â€š → ‚ (single low-9 quote, U+201A)
        "\u00e2\u20ac\u0161": "\u201a",
        # horizontal ellipsis … (U+2026)
        "\u00e2\u20ac\u00a6": "\u2026",
    }
    for old, new in _mojibake_map.items():
        if old in text:
            text = text.replace(old, new)
    return text


def read_json_with_encoding_fix(path):
    """Read JSON file, auto-fixing mojibake (UTF-8 read as Latin-1/Windows-1252).

    In PowerShell on Windows, saving JSON files with Set-Content or piping
    through redirection can corrupt UTF-8 multi-byte sequences (em dashes,
    curly quotes, IPA characters) into Latin-1 mojibake. This function
    detects and reconstructs the original UTF-8 automatically.
    """
    raw = path.read_bytes()
    seen_utf8_bom = raw[:3] == b"\xef\xbb\xbf"

    # Strategy 1: try direct UTF-8 decode, then fix any mojibake
    try:
        text = raw.decode("utf-8")
        fixed = fix_mojibake_chars(text)
        if fixed != text:
            json.loads(fixed)
            print(f"  Note: Fixed mojibake characters in {path.name}")
            return fixed, True
        json.loads(text)
        return text, True
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass

    # Strategy 2: try UTF-8 with BOM stripped
    if seen_utf8_bom:
        try:
            text = raw.decode("utf-8-sig")
            fixed = fix_mojibake_chars(text)
            if fixed != text:
                json.loads(fixed)
                print(f"  Note: Fixed mojibake characters in {path.name}")
                return fixed, True
            json.loads(text)
            return text, True
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass

    # Strategy 3: reconstruct corrupted byte-level UTF-8
    # The raw bytes are valid UTF-8 but were stored as Latin-1 (cp1252).
    # Decode as Latin-1 to get the original bytes back, then decode those as UTF-8.
    try:
        latin_text = raw.decode("latin-1")
        utf8_bytes = latin_text.encode("latin-1")
        text = utf8_bytes.decode("utf-8")
        fixed = fix_mojibake_chars(text)
        final = fixed if fixed != text else text
        json.loads(final)
        print(f"  Note: Reconstructed byte-level mojibake in {path.name}")
        return final, True
    except Exception:
        pass

    # Strategy 4: replace orphaned Latin-1 control bytes
    try:
        text = raw.decode("latin-1")
        orphan_map = {
            "\x93": "\u2013",
            "\x94": "\u2014",
            "\x99": "\u2019",
            "\x9c": "\u201c",
            "\x9d": "\u201d",
        }
        for byte_val, unicode_char in orphan_map.items():
            text = text.replace(byte_val, unicode_char)
        text = re.sub(r"[\x80-\x9f]", "", text)
        json.loads(text)
        print(f"  Note: Reconstructed orphaned bytes in {path.name}")
        return text, True
    except Exception:
        pass

    # Final: try reading with UTF-8 and raise the original error
    return raw.decode("utf-8"), False


def convert_json_to_pdf(json_path, output_dir=None):
    """Main conversion function: JSON -> PDF via Typst CLI."""
    json_path = Path(json_path)

    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}")
        return False

    # Read JSON with auto-fix for mojibake (PowerShell encoding corruption)
    json_text, ok = read_json_with_encoding_fix(json_path)
    if not ok:
        print(f"Error: Cannot decode {json_path} as UTF-8 or reconstruct corrupted encoding")
        return False

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_path}: {e}")
        return False

    # Validate JSON
    errors = validate_json(data)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    # Get output path
    topic = data.get("topic", "untitled")
    if output_dir:
        output_path = (
            Path(output_dir)
            / f"{datetime.now().strftime('%m%d%y')}-{normalize_topic(topic)}-lesson-plan.pdf"
        )
    else:
        output_path = get_output_path(json_path, topic)

    # Build .typ content
    try:
        typ_content = build_typ_content(data, json_path)
    except Exception as e:
        print(f"Error building Typst content: {e}")
        return False

    # Write temporary .typ file
    temp_typ = json_path.parent / f"_temp_{json_path.stem}.typ"
    temp_dir = temp_typ.parent
    try:
        with open(temp_typ, "w", encoding="utf-8") as f:
            f.write(typ_content)
    except Exception as e:
        print(f"Error writing temporary .typ file: {e}")
        return False

    # Copy logo images to temp directory so Typst can find them
    logo_files = ["Image_20260324_141022.png", "cambridge.png"]
    copied_files = []
    for logo in logo_files:
        src = TEMPLATES_DIR / logo
        dst = temp_dir / logo
        if src.exists():
            shutil.copy2(src, dst)
            copied_files.append(dst)

    # Render with Typst
    success = render_typst(temp_typ, output_path)

    # Clean up temporary files
    try:
        temp_typ.unlink()
    except Exception:
        pass
    for f in copied_files:
        try:
            f.unlink()
        except Exception:
            pass

    return success


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json_to_pdf.py <json_file_path> [--output-dir <dir>]")
        sys.exit(1)

    json_file = sys.argv[1]
    output_dir = None

    if len(sys.argv) >= 4 and sys.argv[2] == "--output-dir":
        output_dir = sys.argv[3]

    success = convert_json_to_pdf(json_file, output_dir)
    sys.exit(0 if success else 1)
