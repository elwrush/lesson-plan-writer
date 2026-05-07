"""
json_to_pdf.py - Convert lesson plan JSON to PDF using Typst CLI

Usage:
    python json_to_pdf.py <json_file_path> [--output-dir <dir>]

Example:
    python scripts/json_to_pdf.py output/substitute-lesson-1-M3/050726-what-connects-us-lesson-plan.json
"""

import json
import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import re

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
PDF_OUTPUT_DIR = PROJECT_ROOT / "PDF"

# Roboto OTF font directory (TinyTeX bundled)
ROBOTO_FONT_DIR = Path(os.path.expandvars(
    r"%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto"
))

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

    # Check top-level required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not data[field]:
            errors.append(f"Empty required field: {field}")

    # Check lesson_plan nested fields
    if "lesson_plan" in data and isinstance(data["lesson_plan"], dict):
        lp = data["lesson_plan"]
        for field in REQUIRED_LESSON_PLAN_FIELDS:
            if field not in lp:
                errors.append(f"Missing required lesson_plan field: {field}")
            elif field == "stages" and (not lp[field] or not isinstance(lp[field], list)):
                errors.append("lesson_plan.stages must be a non-empty array")

        # Validate stages
        if "stages" in lp and isinstance(lp["stages"], list):
            for i, stage in enumerate(lp["stages"]):
                for field in REQUIRED_STAGE_FIELDS:
                    if field not in stage:
                        errors.append(f"Missing required field in stage {i+1}: {field}")
    else:
        errors.append("lesson_plan must be a valid object")

    return errors


def normalize_topic(topic):
    """Normalize topic for filename: lowercase, spaces to hyphens."""
    return topic.lower().replace(" ", "-").replace("/", "-")


def get_output_path(json_path, topic):
    """Generate output PDF path: PDF/{input_subfolder}/{mm-dd-yy}-{topic}.pdf"""
    json_path = Path(json_path)

    try:
        output_idx = json_path.parts.index("output")
        subfolder = json_path.parts[output_idx + 1]
    except (ValueError, IndexError):
        subfolder = "default"

    today = datetime.now().strftime("%m-%d-%y")
    normalized_topic = normalize_topic(topic)
    filename = f"{today}-{normalized_topic}.pdf"

    output_dir = PDF_OUTPUT_DIR / subfolder
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir / filename


def escape_typst_string(text):
    """Escape text for safe inclusion in a Typst string literal."""
    if not text:
        return ""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def md_to_typst(text):
    """Convert markdown content to Typst markup."""
    lines = text.split("\n")
    result = []
    in_bullet = False

    for line in lines:
        stripped = line.strip()

        # Headings
        if stripped.startswith("### "):
            result.append("=== " + stripped[4:])
        elif stripped.startswith("## "):
            result.append("== " + stripped[3:])
        elif stripped.startswith("# "):
            result.append("= " + stripped[2:])
        # Horizontal rules
        elif stripped == "---" or stripped == "***" or stripped == "___":
            in_bullet = False
            if result:
                result.append("")
            result.append("#line(length: 100%)")
        # Bullet points (markdown uses - or *)
        elif re.match(r"^[-*]\s+", stripped):
            content = re.sub(r"^[-*]\s+", "", stripped)
            # Inline bold: **text** → *text*
            content = re.sub(r"\*\*(.+?)\*\*", r"*\1*", content)
            # Inline italic: *text* → _text_
            content = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"_\1_", content)
            if not in_bullet and result and result[-1] != "":
                result.append("")
            result.append(f"- {content}")
            in_bullet = True
        else:
            in_bullet = False
            # Inline bold and italic
            line = re.sub(r"\*\*(.+?)\*\*", r"*\1*", stripped)
            line = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"_\1_", line)
            result.append(line)

    return "\n".join(result)


def format_date(date_str):
    """Convert YYMMDD or DDMMYY to 'D Month, YYYY' format."""
    date_str = date_str.strip()
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Try DDMMYY
    if len(date_str) == 6 and date_str.isdigit():
        dd = int(date_str[0:2])
        mm = int(date_str[2:4])
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

    # Check exact and partial matches
    if aim in mappings:
        return mappings[aim]

    # Try partial matches
    for pattern, replacement in sorted(mappings.items(), key=lambda x: -len(x[0])):
        if aim.startswith(pattern):
            return aim.replace(pattern, replacement, 1)

    return aim


def render_template(data):
    """Render the Jinja2 template with lesson plan data."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("lesson-plan-template.typ")

    # Process answer_key: if it's a file path, read its contents
    answer_key = data.get("answer_key", "")
    if answer_key and answer_key != "none":
        answer_key_path = Path(answer_key)
        if answer_key_path.exists() and answer_key_path.suffix == ".md":
            try:
                with open(answer_key_path, "r", encoding="utf-8") as f:
                    answer_key = f.read()
            except Exception:
                pass

    # Process transcript similarly
    transcript = data.get("transcript", "")
    if transcript and transcript != "none":
        transcript_path = Path(transcript)
        if transcript_path.exists() and transcript_path.suffix in (".md", ".txt"):
            try:
                with open(transcript_path, "r", encoding="utf-8") as f:
                    transcript = f.read()
            except Exception:
                pass

    # Convert markdown content to Typst
    answer_key_typst = md_to_typst(answer_key) if answer_key else ""
    transcript_typst = md_to_typst(transcript) if transcript else ""

    # Format the date
    formatted_date = format_date(data.get("date", ""))

    # Process stages: humanize aims and clean procedures
    stages = data.get("lesson_plan", {}).get("stages", [])
    processed_stages = []
    for stage in stages:
        s = dict(stage)
        s["stage_aim"] = humanize_stage_aim(s.get("stage_aim", ""))
        s["procedure"] = clean_procedure(s.get("procedure", ""))
        processed_stages.append(s)

    template_data = {
        "teacher": data.get("teacher", ""),
        "date": formatted_date,
        "duration": data.get("duration", ""),
        "topic": data.get("topic", ""),
        "cefr_level": data.get("lesson_plan", {}).get("cefr_level", ""),
        "class": data.get("lesson_plan", {}).get("class", ""),
        "shape": data.get("lesson_plan", {}).get("shape", ""),
        "shape_name": data.get("lesson_plan", {}).get("shape_name", ""),
        "objective": data.get("objective", ""),
        "materials": data.get("materials", ""),
        "stages": processed_stages,
        "transcript": transcript_typst,
        "answer_key": answer_key_typst,
    }

    return template.render(**template_data)


def render_typst(typ_path, output_path):
    """Render the .typ file to PDF using Typst CLI."""
    typ_path = Path(typ_path)
    output_path = Path(output_path)
    output_dir = output_path.parent

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
        print(
            "Error: Typst CLI not found. Install from https://github.com/typst/typst"
        )
        return False


def convert_json_to_pdf(json_path, output_dir=None):
    """Main conversion function: JSON -> PDF via Typst."""
    json_path = Path(json_path)

    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}")
        return False

    # Read and parse JSON
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
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
        output_path = Path(output_dir) / f"{datetime.now().strftime('%m-%d-%y')}-{normalize_topic(topic)}.pdf"
    else:
        output_path = get_output_path(json_path, topic)

    # Render template
    try:
        typ_content = render_template(data)
    except Exception as e:
        print(f"Error rendering template: {e}")
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
    logo_files = ["Image_20260324_141022.png", "1135082720.png"]
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
