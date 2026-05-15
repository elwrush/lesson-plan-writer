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


def md_to_typst(text):
    """Convert markdown content to Typst markup."""
    text = re.sub(r"\\([#*_\[\]])", r"\1", text)
    text = (
        text.replace("&#x20;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    )
    lines = text.split("\n")
    result = []
    in_bullet = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("#### "):
            result.append("==== " + stripped[5:])
        elif stripped.startswith("### "):
            result.append("=== " + stripped[4:])
        elif stripped.startswith("## "):
            result.append("== " + stripped[3:])
        elif stripped.startswith("# "):
            result.append("= " + stripped[2:])
        elif stripped == "---" or stripped == "***" or stripped == "___":
            in_bullet = False
            if result:
                result.append("")
            result.append("#line(length: 100%)")
        elif re.match(r"^[-*]\s+", stripped):
            content = re.sub(r"^[-*]\s+", "", stripped)
            content = re.sub(r"\*\*(.+?)\*\*", r"*\1*", content)
            content = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"_\1_", content)
            if not in_bullet and result and result[-1] != "":
                result.append("")
            result.append(f"- {content}")
            in_bullet = True
        else:
            in_bullet = False
            line = re.sub(r"\*\*(.+?)\*\*", r"*\1*", stripped)
            line = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"_\1_", line)
            result.append(line)

    text = "\n".join(result)
    text = text.replace("$", "\\$")
    return text


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


def build_typ_content(data):
    """Build .typ file content from lesson plan data. No Jinja2."""
    lines = []

    # Header + page setup
    lines.append('#set text(font: "Roboto", size: 10pt)')
    lines.append("#set par(leading: 0.55em)")
    lines.append("")
    lines.append("#show: it => {")
    lines.append("  set page(")
    lines.append("    header: context {")
    lines.append("      if counter(page).get().first() == 1 {")
    lines.append("        block(")
    lines.append("          stroke: (bottom: 0.5pt + black),")
    lines.append("          inset: (bottom: 6pt, top: 12pt),")
    lines.append("          grid(")
    lines.append("            columns: (1fr, 1fr, 1fr),")
    lines.append("            align: (left + horizon, center + horizon, right + horizon),")
    lines.append('            image("Image_20260324_141022.png", height: 1.35cm),')
    lines.append('            align(center, text(size: 14pt, weight: "bold")[Lesson Plan]),')
    lines.append('            image("1135082720.png", height: 1.8cm),')
    lines.append("          ),")
    lines.append("        )")
    lines.append("      }")
    lines.append("    },")
    lines.append("    margin: (x: 0.75in, top: 1.25in, bottom: 0.75in),")
    lines.append("  )")
    lines.append("  it")
    lines.append("}")
    lines.append("")

    # Lesson Information
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

    # Transcript
    transcript = data.get("transcript", "")
    if transcript and transcript != "none":
        transcript_path = Path(transcript)
        if transcript_path.exists() and transcript_path.suffix in (".md", ".txt"):
            try:
                transcript_content = transcript_path.read_text(encoding="utf-8")
                transcript_content = md_to_typst(transcript_content)
                lines.append("#pagebreak()")
                lines.append("")
                lines.append("= Transcript")
                lines.append("")
                lines.append(transcript_content)
            except Exception:
                pass

    # Answer Key
    answer_key = data.get("answer_key", "")
    if answer_key and answer_key != "none":
        answer_key_path = Path(answer_key)
        if answer_key_path.exists():
            try:
                if answer_key_path.suffix == ".md":
                    ak_content = md_to_typst(answer_key_path.read_text(encoding="utf-8"))
                else:
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


def convert_json_to_pdf(json_path, output_dir=None):
    """Main conversion function: JSON -> PDF via Typst CLI."""
    json_path = Path(json_path)

    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}")
        return False

    # Read and parse JSON
    try:
        with open(json_path, encoding="utf-8") as f:
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
        output_path = (
            Path(output_dir)
            / f"{datetime.now().strftime('%m%d%y')}-{normalize_topic(topic)}-lesson-plan.pdf"
        )
    else:
        output_path = get_output_path(json_path, topic)

    # Build .typ content
    try:
        typ_content = build_typ_content(data)
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
