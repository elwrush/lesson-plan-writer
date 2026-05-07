"""
json_to_markdown.py - Convert lesson plan JSON to mkslides-compatible markdown

Reads docs/slide-design-reference.md for slide design rules.
Generates pedagogical ESL slides: vocabulary, task, answer, transitions.
Usage:
    python scripts/json_to_markdown.py <json_file_path>
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
REFERENCE_DOC = PROJECT_ROOT / "docs" / "slide-design-reference.md"

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
    else:
        errors.append("lesson_plan must be a valid object")

    return errors


def format_date(date_str):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    date_str = date_str.strip()
    if len(date_str) == 6 and date_str.isdigit():
        dd = int(date_str[0:2])
        mm = int(date_str[2:4])
        yy = int(date_str[4:6])
        year = 2000 + yy
        if 1 <= mm <= 12 and 1 <= dd <= 31:
            return f"{dd} {months[mm - 1]}, {year}"
    return date_str


def humanize_stage_aim(aim):
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


def normalize_topic(topic):
    return topic.lower().replace(" ", "-").replace("/", "-")


def clean_procedure(text):
    text = re.sub(r",?\s*\d+\s*min\.?\s*$", "", text)
    text = re.sub(r",?\s*\d+\s*min\.", ".", text)
    text = re.sub(r"\s*\d+\s*min\.?\s*$", "", text)
    text = re.sub(r"(\d+)\s*min\.?\s*\n", r"\n", text)
    return text.strip()


def escape_md(text):
    return text.replace("</textarea>", "<\\/textarea>")


def parse_answer_key(data):
    answer_key = data.get("answer_key", "")
    if not answer_key or answer_key == "none":
        return ""
    answer_key_path = Path(answer_key)
    if answer_key_path.exists() and answer_key_path.suffix == ".md":
        try:
            with open(answer_key_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return ""


def extract_keywords(data):
    """Extract 3-5 challenging CEFR-level words from lesson context."""
    topic = data.get("topic", "").lower()
    materials = data.get("materials", "").lower()
    objective = data.get("objective", "").lower()
    cefr = data.get("lesson_plan", {}).get("cefr_level", "")

    answer_key = parse_answer_key(data)
    combined = f"{topic} {materials} {objective} {answer_key}"

    keyword_bank = {
        "A1": {
            "family": ("/ˈfæməli/", "My mother, father, brother and I are a family."),
            "friend": ("/frend/", "I play football with my friend every Saturday."),
            "school": ("/skuːl/", "I go to school to learn with my classmates."),
            "teacher": ("/ˈtiːtʃə/", "My teacher helps me when I don't understand."),
            "student": ("/ˈstjuːdnt/", "Every student in our class has a desk and books."),
            "house": ("/haʊs/", "We live in a house with a garden and three bedrooms."),
            "name": ("/neɪm/", "My name is written on my notebook so nobody takes it."),
            "like": ("/laɪk/", "I like swimming — it makes me feel happy and free."),
        },
        "A2": {
            "agree": ("/əˈɡriː/", "We both think pizza is the best food — we agree."),
            "explain": ("/ɪkˈspleɪn/", "She drew a picture to explain how the machine works."),
            "experience": ("/ɪkˈspɪəriəns/", "Flying alone for the first time was a scary experience."),
            "opinion": ("/əˈpɪnjən/", "She thinks this book is boring but that is just her opinion."),
            "situation": ("/ˌsɪtjuˈeɪʃn/", "We were lost and the phone was dead — a difficult situation."),
            "belong": ("/bɪˈlɒŋ/", "I finally felt I belong here when everyone smiled at me."),
            "compare": ("/kəmˈpeə/", "When you compare a car to a bicycle, the car is faster."),
            "disagree": ("/ˌdɪsəˈɡriː/", "I think it's cold but you think it's hot — we disagree."),
        },
        "B1": {
            "generation": ("/ˌdʒenəˈreɪʃn/", "My grandmother and I are from different generations."),
            "empathy": ("/ˈempəθi/", "When her friend lost his dog, she cried too — she has empathy."),
            "resolve": ("/rɪˈzɒlv/", "After they talked calmly, they resolved the problem."),
            "perspective": ("/pəˈspektɪv/", "From a child's perspective, school can feel very long."),
            "influence": ("/ˈɪnfluəns/", "Her sister's love of art had a big influence on her."),
            "communicate": ("/kəˈmjuːnɪkeɪt/", "They communicate better now — they listen to each other."),
            "conflict": ("/ˈkɒnflɪkt/", "The conflict started when each side wanted different things."),
            "attitude": ("/ˈætɪtjuːd/", "Her calm attitude helped everyone stay relaxed."),
        },
        "B2": {
            "empathy": ("/ˈempəθi/", "Without understanding how others feel, we cannot connect — that is what empathy gives us."),
            "generational": ("/ˌdʒenəˈreɪʃənl/", "My parents and I see phones differently — that's a generational divide."),
            "resolve": ("/rɪˈzɒlv/", "After weeks of fighting, a simple apology was enough to resolve it."),
            "gap": ("/ɡæp/", "A 40-year age gap means they grew up in completely different worlds."),
            "bridge": ("/brɪdʒ/", "Talking openly helps bridge the distance between young and old."),
            "assume": ("/əˈsjuːm/", "I assumed she was angry, but really she was just tired."),
            "perceive": ("/pəˈsiːv/", "Two people can watch the same film and perceive it differently."),
            "inevitable": ("/ɪnˈevɪtəbl/", "People grow older — it's inevitable, like the seasons changing."),
        },
        "C1": {
            "paradigm": ("/ˈpærədaɪm/", "The internet changed the whole paradigm — how we shop, learn, and talk."),
            "reconcile": ("/ˈrekənsaɪl/", "Trying to reconcile freedom with safety is a constant challenge."),
            "entrenched": ("/ɪnˈtrentʃt/", "His habits were so entrenched he couldn't imagine breakfast without coffee."),
            "discourse": ("/ˈdɪskɔːs/", "The way we speak about immigration — the public discourse — shapes opinion."),
            "alleviate": ("/əˈliːvieɪt/", "A good joke can alleviate tension in an awkward room."),
            "juxtapose": ("/ˌdʒʌkstəˈpəʊz/", "Old black-and-white photos juxtaposed with modern selfies."),
            "dichotomy": ("/daɪˈkɒtəmi/", "The simple dichotomy of good versus bad rarely captures real life."),
            "ubiquitous": ("/juːˈbɪkwɪtəs/", "Smartphones went from rare gadgets to being ubiquitous in ten years."),
        },
        "C2": {
            "ostensibly": ("/ɒˈstensəbli/", "The meeting was ostensibly about budgets but everyone knew it was about layoffs."),
            "acquiescence": ("/ˌækwiˈesns/", "His silence was taken as acquiescence — he didn't object, so they went ahead."),
            "ameliorate": ("/əˈmiːliəreɪt/", "Building parks in poor areas helped ameliorate living conditions."),
            "diametrically": ("/ˌdaɪəˈmetrɪkli/", "North and South — their opinions were diametrically opposite."),
            "presuppose": ("/ˌpriːsəˈpəʊz/", "This question presupposes that money makes people happy."),
            "inherent": ("/ɪnˈhɪərənt/", "Risk is inherent in adventure — you cannot separate the two."),
            "ephemeral": ("/ɪˈfemərəl/", "A mayfly lives only one day — its life is ephemeral."),
            "cogent": ("/ˈkəʊdʒnt/", "Her argument was so cogent that nobody could find a flaw in it."),
        },
    }

    level_words = keyword_bank.get(cefr, keyword_bank["B2"])
    selected = []

    for word, (phonemic, example) in level_words.items():
        if word in combined:
            selected.append((word, phonemic, example))
        if len(selected) >= 5:
            break

    if len(selected) < 3:
        fallback = list(level_words.items())
        needed = 3 - len(selected)
        for word, (phonemic, example) in fallback:
            if word not in [s[0] for s in selected]:
                selected.append((word, phonemic, example))
                needed -= 1
                if needed == 0:
                    break

    return selected[:5]


def generate_title_slide(data):
    teacher = escape_md(data.get("teacher", ""))
    date_str = format_date(data.get("date", ""))
    topic = escape_md(data.get("topic", ""))
    duration = escape_md(data.get("duration", ""))
    materials = escape_md(data.get("materials", ""))
    cefr = data.get("lesson_plan", {}).get("cefr_level", "")

    lines = [
        '<!-- .slide: data-background-gradient="linear-gradient(to bottom, #2c3e50, #3498db)" -->',
        f"# {topic} <span class=\"cefr-badge {cefr}\">{cefr}</span>",
        "",
        f"**{date_str}** | {duration}",
        "",
        f"Teacher: {teacher}",
        "",
        f"*{materials}*",
    ]
    return "\n".join(lines)


def generate_objective_slide(data):
    objective_text = data.get("objective", "")
    cefr = data.get("lesson_plan", {}).get("cefr_level", "")

    outcomes = []
    if "gist" in objective_text.lower():
        outcomes.append("Identify the main purpose of any article")
    if "detail" in objective_text.lower() or "specific information" in objective_text.lower():
        outcomes.append("Find key facts and correct false statements")
    if "inference" in objective_text.lower() or "conclusion" in objective_text.lower():
        outcomes.append("Draw conclusions using evidence from the text")
    if "opinion" in objective_text.lower() or "fact" in objective_text.lower():
        outcomes.append("Distinguish between facts and opinions")

    if not outcomes:
        outcomes = [
            escape_md(objective_text[:60]) + "...",
        ]

    outcomes = outcomes[:3]

    lines = [
        "## What you will be able to do by the end",
        "",
    ]
    for outcome in outcomes:
        lines.append(f"- {outcome}")

    return "\n".join(lines)


def generate_vocabulary_slide(data):
    keywords = extract_keywords(data)
    if not keywords:
        return None

    lines = [
        "## Key vocabulary",
        "",
    ]
    for word, phonemic, example in keywords:
        lines.append(f"- **{word}** {phonemic} — *{escape_md(example)}*")

    lines.extend([
        "",
        "Notes:",
        "Drill each word: teacher says → class repeats (×3). "
        "Ask: 'What does it mean? Can you make a sentence?'",
    ])

    return "\n".join(lines)


def generate_leadin_slide(stage, data):
    procedure = clean_procedure(stage.get("procedure", ""))
    stage_aim = humanize_stage_aim(stage.get("stage_aim", ""))
    topic = data.get("topic", "")
    stage_name = stage.get("stage", "")

    question = f'What do you notice about the theme of "{escape_md(topic)}"?'
    if "photo" in procedure.lower() or "image" in procedure.lower():
        question = "What do you see? What do you wonder?"
    elif "difference" in procedure.lower():
        question = "What differences do you notice?"
    elif "discuss" in procedure.lower() or "tell" in procedure.lower():
        question = "Think of a time when... can you share?"

    lines = [
        '<!-- .slide: data-background="#f5f0eb" -->',
        f"## {escape_md(stage_name)}",
        "",
        f"### {escape_md(question)}",
        "",
        "Notes:",
        f"Display the photo from the materials. Give students 20 seconds to look.",
        f"{escape_md(procedure)}",
        f"Goal: {escape_md(stage_aim)}",
    ]
    return "\n".join(lines)


def generate_prereading_slide(stage, data):
    topic = data.get("topic", "")
    materials = data.get("materials", "")

    lines = [
        '<!-- .slide: data-background="#f5f0eb" -->',
        f"## Before you read: {escape_md(topic)}",
        "",
        "- What is the writer trying to do?",
        "- What solution might they suggest?",
        "",
        f"*{escape_md(materials)}*",
        "<!-- .element: class=\"material-ref\" -->",
        "",
        "Notes:",
        "Students read the title and predict what the article is about.",
        "Give them 30 seconds to share predictions in pairs.",
        "Write 2-3 predictions on the board.",
    ]
    return "\n".join(lines)


def generate_task_slide(stage, data):
    stage_name = escape_md(stage.get("stage", ""))
    procedure = clean_procedure(stage.get("procedure", ""))
    stage_aim = humanize_stage_aim(stage.get("stage_aim", ""))
    materials = escape_md(data.get("materials", ""))
    time_min = stage.get("time", 0)
    interaction = stage.get("interaction", "")
    stage_num = stage.get("stage_number", 0)

    proc_lines = [p.strip()[2:] for p in procedure.split("\n") if p.strip().startswith("- ")]

    lines = [
        f"## {stage_name}",
        f'<span class="aim-label">Stage {stage_num} &middot; {time_min} min &middot; {interaction}</span>',
        "",
    ]
    for i, step in enumerate(proc_lines[:3]):
        lines.append(f"{i+1}. {escape_md(step)}")

    lines.extend([
        "",
        f"*{materials}*",
        "<!-- .element: class=\"material-ref\" -->",
        "",
        "Notes:",
        f"Full procedure: {escape_md(procedure)}",
        f"Goal: {escape_md(stage_aim)}",
        f"Students work individually for {time_min} min. Do NOT reveal answers yet.",
    ])
    return "\n".join(lines)


def generate_task_slide_no_steps(stage, data):
    """For post-reading stages without structured exercises — discussion slide."""
    stage_name = escape_md(stage.get("stage", ""))
    procedure = clean_procedure(stage.get("procedure", ""))
    stage_aim = humanize_stage_aim(stage.get("stage_aim", ""))
    materials = escape_md(data.get("materials", ""))
    time_min = stage.get("time", 0)
    interaction = stage.get("interaction", "")
    stage_num = stage.get("stage_number", 0)

    lines = [
        f"## {stage_name}",
        f'<span class="aim-label">Stage {stage_num} &middot; {time_min} min &middot; {interaction}</span>',
        "",
    ]

    proc_lines = procedure.split("\n")
    for pl in proc_lines:
        stripped = pl.strip()
        if stripped.startswith("- "):
            content = stripped[2:]
            lines.append(f"- {escape_md(content)}")
        elif re.match(r"^\d+\.\s", stripped):
            lines.append(escape_md(stripped))

    lines.extend([
        "",
        f"*{materials}*",
        "<!-- .element: class=\"material-ref\" -->",
        "",
        "Notes:",
        f"Full procedure: {escape_md(procedure)}",
        f"Goal: {escape_md(stage_aim)}",
    ])
    return "\n".join(lines)


def generate_answer_slides(answer_key_content):
    if not answer_key_content:
        return ""

    lines = answer_key_content.split("\n")
    slides = []
    current_slide = []
    current_heading = ""
    in_answer_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## ") or stripped.startswith("# "):
            if current_slide:
                slides.append("\n".join(current_slide))
                current_slide = []
            current_heading = stripped.lstrip("#").strip()
            current_slide.append(f"## Answer key — {escape_md(current_heading)}")
            current_slide.append('<!-- .element: class="aim-label" -->')
            current_slide.append("")

        elif stripped.startswith("### "):
            if current_slide and len(current_slide) > 3:
                slides.append("\n".join(current_slide))
                current_slide = [f"## Answer key — {escape_md(current_heading)}", '<!-- .element: class="aim-label" -->', ""]
            current_slide.append(f"### {escape_md(stripped[4:])}")

        elif stripped == "---":
            if current_slide:
                slides.append("\n".join(current_slide))
                current_slide = []

        elif stripped.startswith("**Answer"):
            answer_text = stripped.replace("**", "").replace("Answer:", "").replace("Answers:", "").strip()
            if answer_text.startswith("**"):
                answer_text = answer_text.strip("*")
            current_slide.append(f"✓ **{escape_md(answer_text)}** <!-- .element: class=\"fragment highlight-green\" -->")

        elif re.match(r"^\d+\.\s\*\*", stripped):
            match = re.match(r"^\d+\.\s\*\*(.+?)\*\*", stripped)
            if match:
                question_text = escape_md(match.group(1)[:80])
                current_slide.append(f"**{question_text}**")

        elif stripped.startswith("- **Answer:**"):
            answer = stripped.replace("- **Answer:**", "").strip()
            current_slide.append(f"✓ **{escape_md(answer)}** <!-- .element: class=\"fragment highlight-green\" -->")

        elif stripped.startswith("- **Answer:** "):
            answer = stripped[12:].strip()
            current_slide.append(f"✓ **{escape_md(answer)}** <!-- .element: class=\"fragment highlight-green\" -->")

        elif stripped == "**Answers:**":
            current_slide.append(f"✓ Students' own answers. <!-- .element: class=\"fragment highlight-green\" -->")

        elif stripped and not stripped.startswith("*") and not stripped.startswith("**Answers**"):
            current_slide.append(escape_md(stripped))

    if current_slide:
        slides.append("\n".join(current_slide))

    if not slides:
        return ""

    return "\n\n---\n\n".join(slides)


def generate_transition_slide(stage_name, prev_stage="", question=""):
    stage_name = escape_md(stage_name)
    lines = [
        '<!-- .slide: data-background="#c0392b" -->',
        f"## {stage_name}",
    ]
    if question:
        lines.append("")
        lines.append(escape_md(question))

    lines.extend([
        "",
        "Notes:",
        f"Transition from {escape_md(prev_stage)} to {stage_name}.",
        "Give students a moment to reset. Introduce the next activity.",
    ])
    return "\n".join(lines)


def generate_summary_slide(data):
    objective_text = data.get("objective", "")
    topic = data.get("topic", "")

    outcomes = []
    if "gist" in objective_text.lower():
        outcomes.append("Identify the main purpose of a text")
    if "detail" in objective_text.lower() or "specific information" in objective_text.lower():
        outcomes.append("Find key facts and correct false statements")
    if "inference" in objective_text.lower() or "conclusion" in objective_text.lower():
        outcomes.append("Use text evidence to support conclusions")
    if "opinion" in objective_text.lower():
        outcomes.append("Express and support opinions about a topic")

    if not outcomes:
        outcomes = ["Understand and discuss the topic in more depth"]

    outcomes = outcomes[:3]

    lines = [
        "## What you can do now",
        "",
    ]
    for outcome in outcomes:
        lines.append(f"✓ {escape_md(outcome)}")

    lines.extend([
        "",
        "Notes:",
        "Elicit from students: What did you learn today?",
        "Connect back to their predictions from the beginning.",
        "Praise effort, mention one thing to improve.",
    ])
    return "\n".join(lines)


def generate_end_slide(data):
    topic = escape_md(data.get("topic", ""))
    cefr = data.get("lesson_plan", {}).get("cefr_level", "")
    lines = [
        '<!-- .slide: data-background="#2c3e50" -->',
        "## Thank you",
        "",
        f"*{topic}* | {cefr}",
    ]
    return "\n".join(lines)


def generate_markdown(data):
    """Main: generate complete markdown from lesson plan data."""
    stages = data.get("lesson_plan", {}).get("stages", [])
    total_stages = len(stages)

    answer_key_content = parse_answer_key(data)

    slides = []

    slides.append(generate_title_slide(data))

    obj_slide = generate_objective_slide(data)
    if obj_slide:
        slides.append(obj_slide)

    vocab_slide = generate_vocabulary_slide(data)
    if vocab_slide:
        slides.append(vocab_slide)

    prev_stage_name = ""

    for i, stage in enumerate(stages):
        stage_name = stage.get("stage", "")
        stage_lower = stage_name.lower()

        if i > 0 and should_add_transition(prev_stage_name, stage_name):
            question = get_transition_question(stage_name, stage)
            slides.append(generate_transition_slide(stage_name, prev_stage_name, question))

        if "lead-in" in stage_lower:
            slides.append(generate_leadin_slide(stage, data))

        elif "gist" in stage_lower and i == stages.index(stage):
            slides.append(generate_prereading_slide(stage, data))

        elif any(kw in stage_lower for kw in ["gist", "detail", "inference", "conclusion", "exercise"]):
            slides.append(generate_task_slide(stage, data))

        elif any(kw in stage_lower for kw in ["post-reading", "speaking", "discussion"]):
            slides.append(generate_task_slide_no_steps(stage, data))

        elif any(kw in stage_lower for kw in ["wrap-up", "reflection"]):
            slides.append(generate_task_slide_no_steps(stage, data))

        else:
            slides.append(generate_task_slide(stage, data))

        prev_stage_name = stage_name

    if answer_key_content:
        answer_section = generate_answer_slides(answer_key_content)
        if answer_section:
            slides.append(answer_section)

    slides.append(generate_summary_slide(data))
    slides.append(generate_end_slide(data))

    return "\n\n---\n\n".join(slides)


def should_add_transition(prev_name, next_name):
    """Determine if a transition slide is needed between stages."""
    transition_keywords = ["reading for gist", "reading for detail", "inference",
                           "post-reading", "wrap-up", "discussion", "exercise"]
    prev_lower = prev_name.lower()
    next_lower = next_name.lower()

    if any(kw in next_lower for kw in transition_keywords) and prev_lower != next_lower:
        return True

    if any(kw in prev_lower for kw in ["lead-in", "discussion"]) and any(
        kw in next_lower for kw in ["reading", "exercise", "detail"]):
        return True

    return False


def get_transition_question(stage_name, stage):
    stage_lower = stage_name.lower()
    stage_aim = humanize_stage_aim(stage.get("stage_aim", ""))

    if "gist" in stage_lower:
        return "What do you predict the text will be about?"
    if "detail" in stage_lower:
        return "What facts did you notice on your first read?"
    if "inference" in stage_lower:
        return "What do you think the writer really means?"
    if "conclusion" in stage_lower:
        return "Which point do you find most convincing?"
    if "post-reading" in stage_lower or "speaking" in stage_lower:
        return "How does this topic connect to your own life?"
    if "wrap-up" in stage_lower or "reflection" in stage_lower:
        return "What is one thing you learned today?"
    return ""


def get_output_path(json_path, date_str):
    json_path = Path(json_path)
    try:
        output_idx = json_path.parts.index("output")
        subfolder = json_path.parts[output_idx + 1]
    except (ValueError, IndexError):
        subfolder = "default"

    slides_dir = OUTPUT_DIR / subfolder / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    try:
        parts = json_path.stem.split("-")
        date_part = parts[0] if len(parts[0]) == 6 and parts[0].isdigit() else "000000"
    except IndexError:
        date_part = "000000"

    topic = "-".join(parts[1:-2]) if len(parts) > 3 else json_path.stem
    filename = f"{date_part}-{topic}-slides.md"
    return slides_dir / filename


def convert_json_to_markdown(json_path):
    json_path = Path(json_path)

    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}")
        return None

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_path}: {e}")
        return None

    errors = validate_json(data)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return None

    markdown_content = generate_markdown(data)

    output_path = get_output_path(json_path, data.get("date", ""))

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
    except Exception as e:
        print(f"Error writing markdown file: {e}")
        return None

    print(f"Markdown created: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/json_to_markdown.py <json_file_path>")
        sys.exit(1)

    json_file = sys.argv[1]
    result = convert_json_to_markdown(json_file)
    sys.exit(0 if result else 1)