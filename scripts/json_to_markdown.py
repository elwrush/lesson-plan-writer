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
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
REFERENCE_DOC = PROJECT_ROOT / "docs" / "slide-design-reference.md"
SLIDES_TEMPLATE = PROJECT_ROOT / "templates" / "slides-template.html"

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


# Note: Pixabay search/download functions were removed to prevent automatic image downloads.
# Images should be manually placed in assets/ and the script will pick them up via find_existing_asset().

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


def generate_lesson_strap(data):
    objective = data.get("objective", "").lower()
    topic = data.get("topic", "")

    # Map objective keywords to natural skill labels
    skill_map = {
        "gist": "Reading for the main idea",
        "detail": "Reading for key facts",
        "specific information": "Reading for specific information",
        "inference": "Reading between the lines",
        "conclusion": "Drawing conclusions",
        "opinion": "Distinguishing facts and opinions",
        "fact": "Distinguishing facts and opinions",
        "speaking": "Discussing and sharing ideas",
        "writing": "Writing about",
        "listening": "Listening to understand",
    }

    skills = []
    for keyword, label in skill_map.items():
        if keyword in objective:
            skills.append(label)

    # Extract context after "in the context of" or "about"
    context = ""
    for pattern in ["in the context of", "about"]:
        if pattern in objective:
            idx = objective.index(pattern) + len(pattern)
            raw_context = objective[idx:].strip().rstrip(".").strip()
            # Remove common filler words for natural output
            for filler in ["an article about ", "a text about ", "the article ", "the text "]:
                if raw_context.startswith(filler):
                    raw_context = raw_context[len(filler):]
            context = raw_context
            break

    # Build strap with natural teacher voice
    if skills and context:
        # Deduplicate skills
        unique_skills = []
        for s in skills:
            if s not in unique_skills:
                unique_skills.append(s)

        if len(unique_skills) == 1:
            return f"{unique_skills[0]} \u2014 {context}"
        elif len(unique_skills) == 2:
            return f"{unique_skills[0]} and {unique_skills[1].lower()} \u2014 {context}"
        else:
            # Multiple skills: use first + "... and more"
            return f"{unique_skills[0]} and more \u2014 {context}"
    elif skills:
        return skills[0]
    elif context:
        return f"Understanding {context}"
    else:
        return f"Exploring {topic}"


def copy_to_assets(slides_dir, image_path, prefix=""):
    """Copy an image to slides/assets/. Returns assets-relative path or None."""
    if not image_path or not slides_dir:
        return None
    src = Path(image_path)
    if not src.exists():
        return None
    assets_dir = Path(slides_dir) / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{prefix}{src.name}" if prefix else src.name
    dest = assets_dir / filename
    shutil.copy2(src, dest)
    return f"assets/{filename}"


def find_existing_asset(slides_dir, file_prefix=None):
    """Check slides_dir/assets/ for existing images. Returns asset-relative path or None."""
    if not slides_dir:
        return None
    assets_dir = Path(slides_dir) / "assets"
    if not assets_dir.exists():
        return None
    for f in assets_dir.iterdir():
        if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png"):
            if file_prefix:
                if f.stem.startswith(file_prefix) or file_prefix in f.stem:
                    return f"assets/{f.name}"
            elif f.name != "logo.png":
                return f"assets/{f.name}"
    return None


def generate_title_slide(data, title_image_path=None, title_attribution=None, slides_dir=None, logo_path=None):
    topic = escape_md(data.get("topic", ""))
    cefr = data.get("lesson_plan", {}).get("cefr_level", "")
    strap = generate_lesson_strap(data)

    existing = None
    if title_image_path:
        image_path = Path(title_image_path).resolve()
    else:
        existing = find_existing_asset(slides_dir, "pixabay_486")
        if not existing:
            existing = find_existing_asset(slides_dir, "title")
        if existing:
            image_path = None
        else:
            image_path = None

    bg_directive = ""
    if existing:
        bg_directive = f'<!-- .slide: data-background-image="{existing}" data-background-opacity="0.8" -->'
    elif image_path and slides_dir:
        rel_path = os.path.relpath(str(image_path), str(slides_dir)).replace("\\", "/")
        bg_directive = f'<!-- .slide: data-background-image="{rel_path}" data-background-opacity="0.8" -->'
    elif image_path:
        rel_path = image_path.relative_to(OUTPUT_DIR.parent).as_posix()
        bg_directive = f'<!-- .slide: data-background-image="{rel_path}" data-background-opacity="0.8" -->'
    else:
        bg_directive = '<!-- .slide: data-background-gradient="linear-gradient(to bottom, #2c3e50, #3498db)" -->'

    lines = [
        '<!-- slide-section: title -->',
        bg_directive,
    ]

    if logo_path:
        logo_path_resolved = Path(logo_path).resolve()
        if slides_dir:
            logo_rel = os.path.relpath(str(logo_path_resolved), str(slides_dir)).replace("\\", "/")
        else:
            logo_rel = logo_path_resolved.relative_to(OUTPUT_DIR.parent).as_posix()
        lines.append(f'<img src="{logo_rel}" class="title-logo" />')
        lines.append("")

    lines.extend([
        f"# {topic} <span class=\"cefr-badge {cefr}\">{cefr}</span>",
        "",
        f"*{escape_md(strap)}*",
    ])
    return "\n".join(lines)


def generate_objective_slide(data):
    objective_text = data.get("objective", "")
    cefr = data.get("lesson_plan", {}).get("cefr_level", "")
    topic = data.get("topic", "")

    outcome_map = {
        "gist": "Understand what the article is mainly about",
        "detail": "Find the most important facts and mistakes",
        "specific information": "Find the most important facts and mistakes",
        "inference": "Understand what the writer really means",
        "conclusion": "Understand how the story ends and why",
        "opinion": "Tell the difference between facts and opinions",
        "fact": "Tell the difference between facts and opinions",
        "speaking": "Talk about ideas from the reading",
        "writing": "Write your own thoughts about the topic",
    }

    outcomes = []
    seen_outcomes = set()
    objective_lower = objective_text.lower()
    for key, simple_outcome in outcome_map.items():
        if key in objective_lower and simple_outcome not in seen_outcomes:
            outcomes.append(simple_outcome)
            seen_outcomes.add(simple_outcome)

    if not outcomes:
        outcomes = [
            "Read and understand the main ideas",
        ]

    outcomes = outcomes[:3]

    lines = [
        '<!-- slide-section: objective -->',
        "## Here's what you'll be able to do",
        "",
    ]
    for outcome in outcomes:
        lines.append(f"- {outcome}")

    lines.extend([
        "",
        "*These are the same skills you need for the PET reading test!*",
    ])

    return "\n".join(lines)


def extract_keywords_from_text(data):
    """Extract vocabulary words from actual lesson content with clean definitions."""
    answer_key = parse_answer_key(data)
    cefr = data.get("lesson_plan", {}).get("cefr_level", "")

    if not answer_key:
        return extract_keywords(data)

    words_to_consider = {
        "A1": ["family", "friend", "school", "teacher", "student", "house", "name", "like", "love", "help"],
        "A2": ["agree", "explain", "experience", "opinion", "situation", "belong", "compare", "disagree", "expect", "value"],
        "B1": ["generation", "empathy", "resolve", "perspective", "influence", "communicate", "conflict", "attitude", "balance", "opportunity"],
        "B2": ["generational", "gap", "bridge", "assume", "perceive", "inevitable", "frustration", "redefine", "workplace", "expectation"],
        "C1": ["paradigm", "reconcile", "entrenched", "discourse", "alleviate", "juxtapose", "dichotomy", "ubiquitous"],
        "C2": ["ostensibly", "acquiescence", "ameliorate", "diametrically", "presuppose", "inherent", "ephemeral", "cogent"],
    }

    # Clean definitions for common ESL B1-B2 vocabulary (derived from lesson content)
    definition_map = {
        "gap": "the difference between two groups or generations",
        "frustration": "the feeling of being upset because things aren't going as expected",
        "redefine": "to change how we think about what belongs in a group",
        "workplace": "the place where you work",
        "generational": "relating to different age groups",
        "empathy": "the ability to understand how someone else feels",
        "resolve": "to find a solution to a problem",
        "perspective": "the way someone thinks about something",
        "influence": "the power to change how someone behaves",
        "communicate": "to share information or ideas with others",
        "conflict": "a serious disagreement or argument",
        "attitude": "the way you think and feel about something",
        "balance": "a state where things are equal",
        "opportunity": "a good chance to do something",
        "assume": "to think something is true without proof",
        "perceive": "to notice or see something",
        "inevitable": "something that will definitely happen",
        "expectation": "what you think should happen",
    }

    level_words = words_to_consider.get(cefr, words_to_consider["B2"])
    combined = answer_key.lower()

    selected = []
    for word in level_words:
        if word in combined:
            # Use a clean definition from our map, or derive from surrounding text
            if word in definition_map:
                definition = definition_map[word]
            else:
                # Find a clean sentence context by searching for the word in sentences
                import re as re_module
                sentences = re_module.split(r'[.!?]', combined)
                definition = ""
                for sentence in sentences:
                    if word in sentence:
                        # Clean up the sentence and use it as definition
                        cleaned = sentence.strip()
                        if len(cleaned) > 10 and len(cleaned) < 120:
                            definition = cleaned
                            break
                if not definition:
                    definition = f"relating to {word}"

            phonemic = get_phonemic(word, cefr)
            selected.append((word, phonemic, definition))

        if len(selected) >= 4:
            break

    if len(selected) < 3:
        return extract_keywords(data)

    return selected[:5]


def get_phonemic(word, cefr=None):
    """Return IPA phonemic transcription for a word."""
    phonemic_bank = {
        "gap": "/ɡæp/",
        "frustration": "/frʌˈstreɪʃn/",
        "redefine": "/ˌriːdɪˈfaɪn/",
        "workplace": "/ˈwɜːkpleɪs/",
        "generational": "/ˌdʒenəˈreɪʃənl/",
        "empathy": "/ˈempəθi/",
        "resolve": "/rɪˈzɒlv/",
        "perspective": "/pəˈspektɪv/",
        "influence": "/ˈɪnfluəns/",
        "communicate": "/kəˈmjuːnɪkeɪt/",
        "conflict": "/ˈkɒnflɪkt/",
        "attitude": "/ˈætɪtjuːd/",
        "balance": "/ˈbæləns/",
        "opportunity": "/ˌɒpəˈtjuːnəti/",
        "assume": "/əˈsjuːm/",
        "perceive": "/pəˈsiːv/",
        "inevitable": "/ɪnˈevɪtəbl/",
        "expectation": "/ˌekspekˈteɪʃn/",
        "generation": "/ˌdʒenəˈreɪʃn/",
    }
    return phonemic_bank.get(word, f"/{word}/")


def generate_vocabulary_slides(data, slides_dir=None):
    """Generate vocabulary slides - one word per slide with maroon background."""
    keywords = extract_keywords_from_text(data)
    if not keywords:
        return None

    cefr = data.get("lesson_plan", {}).get("cefr_level", "")
    slides = []

    for idx, (word, phonemic, _) in enumerate(keywords):
        image_path = None
        existing = find_existing_asset(slides_dir, f"vocab-{word}")
        if existing:
            image_path = existing

        slide_content = generate_single_vocabulary_slide(word, phonemic, image_path, idx + 1)
        if slide_content:
            slides.append(slide_content)

    return slides if slides else None


def generate_single_vocabulary_slide(word, phonemic, image_path=None, slide_num=1):
    """Generate a single vocabulary slide with word in context."""
    context_sentences = {
        "gap": "There is a big **generation gap** between old people and young people.",
        "frustration": "I felt **frustration** when my phone died during an important call.",
        "redefine": "The new CEO wants to **redefine** success in our company.",
        "workplace": "The **workplace** is changing. Now more people work from home.",
        "generational": "There is a **generational** difference. My grandparents do not use smartphones.",
        "empathy": "She showed **empathy** when her friend was sad.",
        "resolve": "They sat down and tried to **resolve** their problem.",
        "perspective": "From my **perspective**, things look different.",
        "influence": "Music had a strong **influence** on her career.",
        "communicate": "It is hard to **communicate** when you do not speak the same language.",
        "conflict": "The **conflict** started over something small.",
        "attitude": "Her positive **attitude** made everyone feel better.",
        "balance": "It is hard to **balance** work and family.",
        "opportunity": "This is a great **opportunity** to learn something new.",
        "assume": "I **assume** you already know the basics.",
        "perceive": "We each **perceive** the situation differently.",
        "inevitable": "Change is **inevitable**. Nothing stays the same forever.",
        "expectation": "My parent's **expectation** is that I go to university.",
        "generation": "My **generation** grew up with the internet.",
    }

    display_word = "generation gap" if word == "gap" else word
    phonemic_display = "/ˌdʒenəˈreɪʃn ɡæp/" if word == "gap" else phonemic
    context = context_sentences.get(word, f"I understand **{display_word}** now.")

    lines = [
        f'<!-- slide-section: vocab-{slide_num} -->',
    ]

    if image_path:
        if image_path.startswith("assets/"):
            rel_path = Path(image_path).name
            lines.extend([
                f'<!-- .slide: data-background-image="{image_path}" -->',
            ])
        else:
            rel_path = Path(image_path).name
            lines.extend([
                f'<!-- .slide: data-background-image="assets/{rel_path}" -->',
            ])
    else:
        lines.append('<!-- .slide: data-background-gradient="linear-gradient(to bottom, #667eea, #764ba2)" -->')

    if slide_num == 1:
        lines.extend([
            "## Important Words",
            "",
        ])
        lines.extend([
            f"**{display_word}**",
            f"_{phonemic_display}_",
            "",
            f"*{context}*",
        ])
    else:
        lines.extend([
            f"**{display_word}**",
            f"_{phonemic_display}_",
            "",
            f"*{context}*",
        ])

    return "\n".join(lines)


def generate_leadin_question(topic, procedure):
    topic_lower = topic.lower()

    if "generation" in topic_lower or "connect" in topic_lower:
        return "What do these two people have in common? What makes them different?"
    elif "photo" in procedure.lower() or "image" in procedure.lower():
        return "What do you see? What do you wonder?"
    elif "difference" in procedure.lower():
        return "What differences do you notice?"
    elif "discuss" in procedure.lower() or "tell" in procedure.lower():
        return "Think of a time when this happened to you. Can you share?"
    else:
        return f"What comes to mind when you think about {escape_md(topic_lower)}?"


def generate_leadin_slide(stage, data, slides_dir=None):
    procedure = clean_procedure(stage.get("procedure", ""))
    stage_aim = humanize_stage_aim(stage.get("stage_aim", ""))
    topic = data.get("topic", "")
    stage_name = stage.get("stage", "")

    question = generate_leadin_question(topic, procedure)

    existing = find_existing_asset(slides_dir, "pixabay_733")
    if not existing:
        existing = find_existing_asset(slides_dir, "leadin")
    if existing:
        rel_path = existing
    else:
        rel_path = None

    if rel_path:
        bg_directive = f'<!-- .slide: data-background-image="{rel_path}" data-background-opacity="0.7" -->'
    else:
        bg_directive = '<!-- .slide: data-background-gradient="linear-gradient(to bottom, #667eea, #764ba2)" -->'

    lines = [
        '<!-- slide-section: leadin -->',
        bg_directive,
        f"## {escape_md(friendly_stage_name(stage_name))}",
        "",
        f"### {escape_md(question)}",
        "",
        "Notes:",
        "Display the photo. Give students 20 seconds to look silently.",
        "Then ask the question. Elicit 3-4 responses.",
        f"Connect responses to today's topic: {escape_md(topic)}.",
        f"{escape_md(re.sub(r'\b[Ss]s\b', 'Students', procedure))}",
        f"Goal: {escape_md(stage_aim)}",
    ]
    return "\n".join(lines)


def friendly_stage_name(stage_name):
    """Convert formal stage names to friendly student-facing language."""
    mappings = {
        "Lead-in": "Let's get Started",
        "Lead in": "Let's get Started",
        "lead-in": "Let's get Started",
        "lead in": "Let's get Started",
        "Reading for gist": "What's the idea?",
        "Reading for detail and specific information": "Finding details",
        "Reading for detail": "Finding details",
        "Reading for inference and conclusion": "Making conclusions",
        "Reading for inference": "Making conclusions",
        "Post-reading speaking task": "Let's Discuss",
        "Post reading speaking task": "Let's Discuss",
        "post-reading speaking task": "Let's Discuss",
        "Wrap-up and reflection": "Let's Review",
        "Wrap up and reflection": "Let's Review",
        "Wrap-up": "Let's Review",
    }
    return mappings.get(stage_name, stage_name)


def generate_prereading_slide(stage, data, slides_dir=None):
    topic = data.get("topic", "")
    materials = data.get("materials", "")

    existing = find_existing_asset(slides_dir, "reading")
    if existing:
        rel_path = existing
    else:
        rel_path = None

    if rel_path:
        bg_directive = f'<!-- .slide: data-background-image="{rel_path}" data-background-opacity="0.7" -->'
    else:
        bg_directive = '<!-- .slide: data-background-gradient="linear-gradient(to bottom, #f5f0eb, #e8ddd3)" -->'

    lines = [
        '<!-- slide-section: prereading -->',
        bg_directive,
        f"## Before you read",
        "",
        "- What is the writer trying to do?",
        "- What solution might they suggest?",
        "",
        "Notes:",
        "Students read the title and look at the photo.",
        "Give them 30 seconds to share predictions in pairs.",
        "Write 2-3 predictions on the board.",
        f"Materials: {escape_md(materials)}" if materials else "",
    ]
    return "\n".join(lines)


def extract_task_instructions(procedure, stage_name):
    lines = procedure.strip().split("\n")
    task_lines = []

    for line in lines:
        stripped = line.strip().lstrip("- ")
        stripped_lower = stripped.lower()
        if any(skip in stripped_lower for skip in [
            "pair check", "whole-class feedback", "feedback",
            "elicit", "brief ", "tell ss", "teacher"
        ]):
            continue
        if re.match(r"\d+\s*min", stripped):
            continue
        stripped = re.sub(r"\b[Ss]s\b", "you", stripped)
        instruction = to_imperative(stripped)
        if instruction and instruction.strip():
            task_lines.append(instruction.strip())

    return task_lines[:3]


def to_imperative(text):
    if not text:
        return text
    text = text.strip()
    if not text:
        return text
    if "they" in text.lower():
        split_sentences = re.split(r"[.]", text)
        kept = []
        for s in split_sentences:
            s = s.strip()
            if s and "they" not in s.lower():
                kept.append(s)
        text = ". ".join(kept)
        text = text.strip()
    text = re.sub(r"\(Exercise \d+\)", "", text)
    text = re.sub(r"(\d+)\.\s*", "", text)
    text = re.sub(r"^[Ss]s ", "", text).strip()
    text = re.sub(r"^Students ", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^in pairs, ", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^individually, ", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^You ", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^you ", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"\b[Ss]s\b", "", text)
    text = re.sub(r"\byou\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    if text and not text[0].isupper():
        text = text[0].upper() + text[1:]
    if text and not text.endswith((".", "!")):
        text = text + "."
    return text


def generate_task_slide(stage, data):
    stage_name = escape_md(stage.get("stage", ""))
    procedure = clean_procedure(stage.get("procedure", ""))
    stage_aim = humanize_stage_aim(stage.get("stage_aim", ""))
    materials = escape_md(data.get("materials", ""))
    time_min = stage.get("time", 0)
    interaction = stage.get("interaction", "")
    stage_num = stage.get("stage_number", 0)

    task_lines = extract_task_instructions(procedure, stage_name)

    lines = [
        f'<!-- slide-section: task-{stage_num} -->',
    ]

    timer_seconds = int(stage.get("time", 0)) * 60
    if timer_seconds > 0:
        lines.append(f'<!-- .slide: data-timer="{timer_seconds}" -->')

    lines.extend([
        f"## {friendly_stage_name(stage_name)}",
        "",
    ])

    for task_line in task_lines:
        lines.append(f"- {escape_md(task_line)}")

    lines.extend([
        "",
        "Notes:",
        f"Stage {stage_num} · {time_min} min · {interaction}",
        f"Goal: {escape_md(stage_aim)}",
    ])

    # Add material ref in notes
    if materials:
        lines.append(f"Materials: {materials}")

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
        f'<!-- slide-section: task-{stage_num} -->',
    ]

    timer_seconds = int(stage.get("time", 0)) * 60
    if timer_seconds > 0:
        lines.append(f'<!-- .slide: data-timer="{timer_seconds}" -->')

    lines.extend([
        f"## {friendly_stage_name(stage_name)}",
        "",
    ])

    proc_lines = procedure.split("\n")
    for pl in proc_lines:
        stripped = pl.strip()
        if stripped.startswith("- "):
            content = stripped[2:]
            # Replace "Ss" with "Students" for teacher reference
            content = re.sub(r"\b[Ss]s\b", "Students", content)
            if not any(skip in content.lower() for skip in ["pair check", "feedback", "elicit"]):
                lines.append(f"- {escape_md(content)}")
        elif re.match(r"^\d+\.\s", stripped):
            lines.append(escape_md(stripped))

    lines.extend([
        "",
        "Notes:",
        f"Stage {stage_num} · {time_min} min · {interaction}",
        f"Goal: {escape_md(stage_aim)}",
    ])

    # Add material ref in notes
    if materials:
        lines.append(f"Materials: {materials}")

    return "\n".join(lines)


def generate_answer_slides(answer_key_content):
    if not answer_key_content:
        return ""

    lines = answer_key_content.split("\n")
    slides = []
    current_slide_lines = []
    in_article_section = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## Article:"):
            in_article_section = True
            continue
        if in_article_section and stripped.startswith("**Paragraph"):
            continue
        if in_article_section:
            if stripped and not stripped.startswith("#"):
                continue
            else:
                in_article_section = False

        if stripped.startswith("### Exercise"):
            if current_slide_lines:
                slides.append("\n".join(current_slide_lines))
            exercise_name = stripped.lstrip("#").strip()
            current_slide_lines = [
                '<!-- slide-section: answers -->',
                f"## {escape_md(exercise_name)}",
                '<!-- .element: class="aim-label" -->',
                "",
            ]
            continue

        if stripped == "---":
            continue

        answer_match = re.search(r"\*\*Answer:\*\*\s*(.+)", stripped)
        if answer_match:
            answer = answer_match.group(1).strip()
            if answer.startswith("F."):
                correction = answer[2:].strip()
                current_slide_lines.append(
                    f'✗ **False** <!-- .element: class="fragment highlight-red" -->'
                )
                current_slide_lines.append(
                    f"✓ *{escape_md(correction)}* <!-- .element: class=\"fragment highlight-green\" -->"
                )
            elif answer == "T":
                current_slide_lines.append(
                    f'✓ **True** <!-- .element: class="fragment highlight-green" -->'
                )
            elif answer.lower() in ["students' own answers.", "students own answers."]:
                current_slide_lines.append(
                    f"✓ Students' own answers. <!-- .element: class=\"fragment highlight-green\" -->"
                )
            elif answer and len(answer) <= 3:
                current_slide_lines.append(
                    f'✓ **{escape_md(answer)}** <!-- .element: class="fragment highlight-green" -->'
                )
            continue

        if stripped == "**Answers:**":
            current_slide_lines.append(
                f"✓ Students' own answers. <!-- .element: class=\"fragment highlight-green\" -->"
            )
            continue

        if stripped.startswith("*") and not stripped.startswith("**"):
            continue
            continue

        answer_match = re.search(r"\*\*Answer:\*\*\s*(.+)", stripped)
        if answer_match:
            answer = answer_match.group(1).strip()
            if answer.startswith("F."):
                correction = answer[2:].strip()
                current_slide_lines.append(
                    f'✗ **False** <!-- .element: class="fragment highlight-red" -->'
                )
                current_slide_lines.append(
                    f"✓ *{escape_md(correction)}* <!-- .element: class=\"fragment highlight-green\" -->"
                )
            elif answer == "T":
                current_slide_lines.append(
                    f'✓ **True** <!-- .element: class="fragment highlight-green" -->'
                )
            elif answer.lower() in ["students' own answers.", "students own answers."]:
                current_slide_lines.append(
                    f"✓ Students' own answers. <!-- .element: class=\"fragment highlight-green\" -->"
                )
            elif answer and len(answer) <= 3:
                current_slide_lines.append(
                    f'✓ **{escape_md(answer)}** <!-- .element: class="fragment highlight-green" -->'
                )
            continue

        if stripped == "**Answers:**":
            current_slide_lines.append(
                f"✓ Students' own answers. <!-- .element: class=\"fragment highlight-green\" -->"
            )
            continue

        q_match = re.match(r"^(\d+)\.\s+\*\*(.+?)\*\*", stripped)
        if q_match:
            num, question_text = q_match.groups()
            if len(question_text) > 100:
                question_text = question_text[:97] + "..."
            current_slide_lines.append(f"**{escape_md(question_text)}**")
            continue

        opt_match = re.match(r"^([a-c])\.\s+(.+)", stripped)
        if opt_match:
            letter, text = opt_match.groups()
            current_slide_lines.append(f"{letter}. {escape_md(text)}")
            continue

    if current_slide_lines:
        slides.append("\n".join(current_slide_lines))

    if not slides:
        return ""

    return "\n\n---\n\n".join(slides)


def generate_transition_slide(stage_name, stage_num=0, prev_stage="", question=""):
    stage_name = escape_md(stage_name)
    lines = [
        f'<!-- slide-section: transition-{stage_num} -->',
        '<!-- .slide: data-background="#c0392b" -->',
        f"## {friendly_stage_name(stage_name)}",
    ]
    if question:
        lines.append("")
        lines.append(escape_md(question))

    lines.extend([
        "",
        "Notes:",
        f"Moving from {escape_md(prev_stage)}.",
        "Give students a moment to reset. Introduce the next activity.",
    ])
    return "\n".join(lines)


def generate_summary_slide(data):
    objective_text = data.get("objective", "")
    topic = data.get("topic", "")

    outcome_map = {
        "gist": "I can find the main idea",
        "detail": "I can find important facts",
        "specific information": "I can find important facts",
        "inference": "I can understand what the writer means",
        "conclusion": "I can explain the ending",
        "opinion": "I can share my ideas",
        "fact": "I can tell fact from opinion",
    }

    outcomes = []
    seen = set()
    obj_lower = objective_text.lower()
    for key, outcome in outcome_map.items():
        if key in obj_lower and outcome not in seen:
            outcomes.append(outcome)
            seen.add(outcome)

    if not outcomes:
        outcomes = ["I can understand and talk about the topic"]

    outcomes = outcomes[:3]

    lines = [
        '<!-- slide-section: summary -->',
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
        '<!-- slide-section: end -->',
        '<!-- .slide: data-background="#2c3e50" -->',
        "## Thank you",
        "",
        f"*{topic}* | {cefr}",
    ]
    return "\n".join(lines)


def generate_markdown(data, title_image_path=None, title_attribution=None, slides_dir=None, logo_path=None):
    """Main: generate complete markdown from lesson plan data."""
    stages = data.get("lesson_plan", {}).get("stages", [])
    total_stages = len(stages)

    answer_key_content = parse_answer_key(data)

    slides = []

    slides.append(generate_title_slide(data, title_image_path, title_attribution, slides_dir, logo_path))

    obj_slide = generate_objective_slide(data)
    if obj_slide:
        slides.append(obj_slide)

    prev_stage_name = ""

    for i, stage in enumerate(stages):
        stage_name = stage.get("stage", "")
        stage_num = stage.get("stage_number", i)
        stage_lower = stage_name.lower()

        if i > 0 and should_add_transition(prev_stage_name, stage_name):
            question = get_transition_question(stage_name, stage)
            slides.append(generate_transition_slide(stage_name, stage_num, prev_stage_name, question))

        if "lead-in" in stage_lower:
            slides.append(generate_leadin_slide(stage, data, slides_dir))
            vocab_slides = generate_vocabulary_slides(data, slides_dir)
            if vocab_slides:
                slides.extend(vocab_slides)

        elif "gist" in stage_lower and i == stages.index(stage):
            slides.append(generate_prereading_slide(stage, data, slides_dir))

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

    numbered = [f"<!-- slide: {n} -->\n{slide}" for n, slide in enumerate(slides)]
    return "\n\n---\n\n".join(numbered)


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

    question_map = {
        "gist": "What do you think the text is about?",
        "detail": "What did you learn from your first reading?",
        "inference": "What is the writer's real message?",
        "conclusion": "Which idea makes the most sense to you?",
        "post-reading": "Is this true in your life too?",
        "speaking": "Is this true in your life too?",
        "wrap-up": "What is one thing you learned today?",
        "reflection": "What is one thing you learned today?",
    }

    for key, question in question_map.items():
        if key in stage_lower:
            return question
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


def write_index_html(markdown_content, output_dir):
    """Write a self-contained index.html with markdown inlined."""
    template = SLIDES_TEMPLATE.read_text(encoding="utf-8")
    html = template.replace("{{ MARKDOWN }}", markdown_content)
    index_path = Path(output_dir) / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"index.html written: {index_path}")

    # Copy timer plugin files alongside index.html
    output_path = Path(output_dir)
    timer_css_src = TEMPLATES_DIR / "timer-plugin.css"
    timer_js_src = TEMPLATES_DIR / "timer-plugin.js"
    if timer_css_src.exists():
        shutil.copy2(timer_css_src, output_path / "timer-plugin.css")
    if timer_js_src.exists():
        shutil.copy2(timer_js_src, output_path / "timer-plugin.js")

    # Copy chime audio to slides/assets/
    chime_src = PROJECT_ROOT / "general-assets" / "audio" / "freesound_community-chime-sound-7143.mp3"
    if chime_src.exists():
        assets_dir = output_path / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(chime_src, assets_dir / "chime.mp3")


def load_image_references(md_path):
    """Extract existing image references from markdown, keyed by slide section."""
    references = {}
    content = Path(md_path).read_text(encoding="utf-8")
    current_section = None
    for line in content.split("\n"):
        m = re.match(r"<!--\s*slide-section:\s*(\S+)\s*-->", line)
        if m:
            current_section = m.group(1)
        img_match = re.search(r'data-background-image="([^"]+)"', line)
        if img_match and current_section:
            references[current_section] = img_match.group(1)
    return references


def restore_image_references(markdown_content, preserved_refs):
    """Replace newly generated image refs with preserved ones by section."""
    for section, old_path in preserved_refs.items():
        markdown_content = re.sub(
            rf'(<!--\s*slide-section:\s*{re.escape(section)}\s*-->.*?data-background-image=")[^"]+(")',
            r'\1' + old_path + r'\2',
            markdown_content,
            flags=re.DOTALL
        )
    return markdown_content


def convert_json_to_markdown(json_path, title_image_path=None, title_attribution=None, logo_path=None,
                              sections=None, merge=False):
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

    output_path = get_output_path(json_path, data.get("date", ""))
    slides_dir = output_path.parent

    existing_images = {}
    if output_path.exists():
        existing_images = load_image_references(output_path)
        if existing_images:
            print(f"Preserving {len(existing_images)} existing image references from {output_path.name}")

    topic = data.get("topic", "")

    if not logo_path:
        default_logo = TEMPLATES_DIR / "Image_20260324_141022.png"
        if default_logo.exists():
            import shutil
            assets_dir = slides_dir / "assets"
            assets_dir.mkdir(parents=True, exist_ok=True)
            dest_logo = assets_dir / "logo.png"
            shutil.copy2(default_logo, dest_logo)
            logo_path = str(dest_logo)

    if sections and merge and output_path.exists():
        existing = output_path.read_text(encoding="utf-8")
        new_sections = {}

        for section_id in sections:
            section_content = generate_section(
                data, section_id.strip(), slides_dir,
                title_image_path, title_attribution, logo_path
            )
            if section_content:
                new_sections[section_id.strip()] = section_content

        if new_sections:
            merged = merge_sections(existing, new_sections)
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(merged)
                print(f"Sections updated: {', '.join(sections)}")
                write_index_html(merged, slides_dir)
                return output_path
            except Exception as e:
                print(f"Error writing merged markdown file: {e}")
                return None
        else:
            print("No sections generated, file unchanged")
            write_index_html(existing, slides_dir)
            return output_path

    markdown_content = generate_markdown(data, title_image_path, title_attribution, slides_dir, logo_path)

    if existing_images:
        markdown_content = restore_image_references(markdown_content, existing_images)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
    except Exception as e:
        print(f"Error writing markdown file: {e}")
        return None

    print(f"Markdown created: {output_path}")
    write_index_html(markdown_content, slides_dir)
    return output_path


def merge_sections(existing_md, new_sections):
    """Merge new slide sections into existing markdown.

    existing_md: full markdown content of the existing file
    new_sections: dict of {section_id: new_content}

    Returns: merged markdown content
    """
    lines = existing_md.split("\n")
    result = []
    current_section = None
    in_section = False

    for line in lines:
        marker_match = re.match(r'<!-- slide-section: (\S+) -->', line)
        if marker_match:
            section_id = marker_match.group(1)
            if section_id in new_sections:
                # Replace this section with new content
                result.append(f'<!-- slide-section: {section_id} -->')
                result.append(new_sections[section_id])
                in_section = True
                current_section = section_id
                continue
            else:
                in_section = False
                current_section = None

        if in_section:
            if line.strip() == "---":
                # End of current section
                in_section = False
                result.append(line)
            # Skip old section content
            continue

        result.append(line)

    return "\n".join(result)


def generate_section(data, section_id, slides_dir, title_image_path, title_attribution, logo_path):
    """Generate a single slide section by ID."""
    if section_id == "title":
        return generate_title_slide(data, title_image_path, title_attribution, slides_dir, logo_path)
    elif section_id == "objective":
        return generate_objective_slide(data)
    elif section_id.startswith("vocab"):
        vocab_slides = generate_vocabulary_slides(data, slides_dir)
        if vocab_slides:
            return "\n\n---\n\n".join(vocab_slides)
        return None
    elif section_id == "leadin":
        stages = data.get("lesson_plan", {}).get("stages", [])
        for stage in stages:
            if "lead-in" in stage.get("stage", "").lower():
                return generate_leadin_slide(stage, data, slides_dir)
        return None
    elif section_id == "prereading":
        stages = data.get("lesson_plan", {}).get("stages", [])
        for stage in stages:
            if "gist" in stage.get("stage", "").lower():
                return generate_prereading_slide(stage, data, slides_dir)
        return None
    elif section_id.startswith("task-"):
        try:
            stage_num = int(section_id.split("-")[1])
        except (ValueError, IndexError):
            return None
        stages = data.get("lesson_plan", {}).get("stages", [])
        for stage in stages:
            if stage.get("stage_number", 0) == stage_num:
                return generate_task_slide(stage, data)
        return None
    elif section_id.startswith("transition-"):
        try:
            stage_num = int(section_id.split("-")[1])
        except (ValueError, IndexError):
            return None
        stages = data.get("lesson_plan", {}).get("stages", [])
        prev_name = ""
        for i, stage in enumerate(stages):
            if stage.get("stage_number", i) == stage_num and i > 0:
                question = get_transition_question(stage.get("stage", ""), stage)
                return generate_transition_slide(stage.get("stage", ""), stage_num,
                                                  stages[i - 1].get("stage", ""), question)
        return None
    elif section_id == "answers":
        answer_key_content = parse_answer_key(data)
        if answer_key_content:
            return generate_answer_slides(answer_key_content)
        return None
    elif section_id == "summary":
        return generate_summary_slide(data)
    elif section_id == "end":
        return generate_end_slide(data)
    return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert lesson plan JSON to reveal.js slides (markdown + self-contained HTML).")
    parser.add_argument("json_file", help="Path to lesson plan JSON file")
    parser.add_argument("--title-image", default=None,
                        help="Pre-downloaded image path for title slide")
    parser.add_argument("--title-attribution", default=None,
                        help="Attribution string for pre-downloaded title image")
    parser.add_argument("--logo-image", default=None,
                        help="Path to logo image to display at top of title slide")
    parser.add_argument("--section", default=None,
                        help="Comma-separated section IDs to regenerate (e.g., 'title,vocab-1,task-2')")
    parser.add_argument("--merge", action="store_true",
                        help="Merge regenerated sections into existing markdown file")
    args = parser.parse_args()

    result = convert_json_to_markdown(
        args.json_file, args.title_image, args.title_attribution, args.logo_image,
        sections=args.section.split(",") if args.section else None,
        merge=args.merge
    )
    sys.exit(0 if result else 1)