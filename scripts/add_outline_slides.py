"""Add outline slides to M3 and M2 slideshows with fragment reveals for answers."""

import re
from pathlib import Path


def build_outline_slide(slide_id, heading, items, fragment_start=0):
    """Build an outline slide HTML section with fragment reveals on answers.

    items: list of (indent_level, text_before_blank, answer, text_after_blank or None)
    """
    lines = []
    lines.append(
        f'<section id="{slide_id}" data-background-color="#1a1a2e" data-background-transition="none">'
    )
    lines.append(f'    <h2 style="font-size: 1.6em; color: #ffdd00;">{heading}</h2>')
    lines.append('    <div style="font-size: 0.85em; line-height: 1.6; padding: 0 1em;">')

    fi = fragment_start
    for indent, before, answer, after in items:
        indent_px = 20 * indent
        style = f'style="padding-left: {indent_px}px; margin: 0.2em 0;"'

        if answer is None:
            # No blank - plain text
            lines.append(f'        <p {style}><span style="color: #fff;">{before}</span></p>')
        else:
            a_style = "display: none;"
            b_color = "#888"
            html = (
                f"        <p {style}>"
                f'<span style="color: #fff;">{before}</span>'
                f'<span class="fragment custom out-blank" data-fragment-index="{fi}">'
                f'<span class="blank" style="color: {b_color};">____________</span>'
                f'<span class="ans" style="color: #ffdd00;">{answer}</span>'
                f"</span>"
            )
            if after:
                html += f'<span style="color: #fff;">{after}</span>'
            html += "</p>"
            lines.append(html)
            fi += 1

    lines.append("    </div>")
    lines.append(
        '    <aside class="notes">Review outline answers with class. Click through each blank to reveal the answer. Discuss any questions students have about why each answer is correct.</aside>'
    )
    lines.append("</section>")
    return "\n".join(lines)


def insert_after_slide(html, slide_id, new_section):
    """Insert new_section after the closing </section> of the slide with given id."""
    pattern = rf'(<section\s+id="{slide_id}"[^>]*>.*?</section>\s*\n?)'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        print(f"  WARNING: Could not find slide id={slide_id}")
        return html
    end = match.end()
    return html[:end] + "\n" + new_section + "\n" + html[end:]


def insert_before_slide(html, slide_id, new_section):
    """Insert new_section before the opening <section> of the slide with given id."""
    pattern = rf'(<section\s+id="{slide_id}")'
    match = re.search(pattern, html)
    if not match:
        print(f"  WARNING: Could not find slide id={slide_id}")
        return html
    start = match.start()
    return html[:start] + new_section + "\n" + html[start:]


# ============================================================
# M3 Gender Roles — Outline Content
# ============================================================
M3_OUTLINES = {
    "slide-outline-p1": {
        "heading": "Part 1: Traditional Gender Roles",
        "items": [
            (0, "I. Traditional Gender Roles in Society", None, None),
            (1, "A. 1950s TV shows portrayed clear gender roles", None, None),
            (2, "1. Women shown as the ", "homemaker", None),
            (2, "2. Men shown as the ", "breadwinner", None),
            (1, "B. Kings College study — 23,000 people from 29 countries", None, None),
            (2, "1. Gen Z holds the ", "strongest", " traditional beliefs"),
            (2, "2. ", "31%", " of Gen Z men believe a wife should obey her husband"),
            (2, "3. ", "33%", " of Gen Z men say a husband should have the final word"),
            (1, "C. Attitudes beyond the home", None, None),
            (2, "1. ", "61%", " of Gen Z men say enough has been done for gender equality"),
            (2, "2. ", "57%", " of Gen Z men feel men are now discriminated against"),
        ],
    },
    "slide-outline-p2": {
        "heading": "Part 2: The Role of Social Media",
        "items": [
            (0, "II. The Role of Social Media", None, None),
            (1, "A. Josh Glover — facilitator at ", "Man Cave", None),
            (2, "1. His organisation tackles ", "gender stereotypes", " in schools"),
            (2, "2. Social media helps bring back ", "outdated", " gender norms"),
            (1, "B. How social media algorithms work", None, None),
            (2, "1. Algorithms create ", "echo chambers", " where users hear agreeing voices"),
            (2, "2. No one presents ", "alternative", " opinions"),
            (2, "3. Users only see opinions that get debunked or ", "smashed", None),
            (1, "C. The definition problem", None, None),
            (
                2,
                "1. Teenage boys\u2019 definition of ",
                "feminism",
                " differs from the intended meaning",
            ),
            (
                2,
                "2. This results from algorithms and lack of ",
                "conversation",
                " with people who hold different views",
            ),
        ],
    },
    "slide-outline-p3": {
        "heading": "Part 3: Tradwives and Solutions",
        "items": [
            (0, "III. Tradwives and Solutions", None, None),
            (1, 'A. "Tradwife" influencers', None, None),
            (2, "1. Glamorise ", "traditional domestic", " lifestyles"),
            (2, "2. Create content about cooking, cleaning, and ", "domestic", " roles"),
            (1, "B. Effects on young people", None, None),
            (
                2,
                "1. University of Melbourne study of 2,300 adults and 1,100 young people",
                None,
                None,
            ),
            (
                2,
                "2. Support for violence to resist feminism was highest among ",
                "adolescent boys",
                None,
            ),
            (
                2,
                "3. Around ",
                "40%",
                " of boys aged 13-17 agree women lie about domestic and sexual violence",
            ),
            (1, "C. Josh\u2019s perspective on solutions", None, None),
            (2, "1. Two parts needed: ", "awareness", " and problem-solving"),
            (2, "2. Need for ", "safe", " conversations where people are not judged"),
            (
                2,
                "3. Importance of ",
                "role modelling",
                " \u2014 older generations investing in younger people",
            ),
        ],
    },
}

# Insertion: after the transition slide for each part (which is before the task/video)
M3_INSERTIONS = [
    ("slide-ans-p1-q3", "slide-outline-p1"),
    ("slide-ans-p2-q3", "slide-outline-p2"),
    ("slide-ans-p3-q3", "slide-outline-p3"),
]

# ============================================================
# M2 Diphtheria — Outline Content (from answer key)
# ============================================================
M2_OUTLINES = {
    "slide-outline-p1": {
        "heading": "Part 1: History of Diphtheria",
        "items": [
            (0, "I. History of Diphtheria", None, None),
            (1, "A. About the disease", None, None),
            (2, "1. First described by ", "Hippocrates", None),
            (2, "2. Greek name means ", "leather", None),
            (1, "B. Medical breakthrough (1890s)", None, None),
            (2, "1. Scientists developed ", "serum", " therapy"),
            (2, "2. Won the first Nobel Prize in ", "1901", None),
            (1, "C. Safer vaccine (1923)", None, None),
            (2, "1. A ", "safer", " vaccine was made"),
        ],
    },
    "slide-outline-p2": {
        "heading": "Part 2: Vaccines and Outbreak",
        "items": [
            (0, "II. Vaccines and Outbreak in Australia", None, None),
            (1, "A. Vaccination in Australia", None, None),
            (2, "1. ", "93%", " of 5-year-olds are vaccinated"),
            (2, "2. A ", "booster", " is given at ages 11-13"),
            (1, "B. Current outbreak", None, None),
            (2, "1. More than ", "230", " cases"),
            (2, "2. Many cases in ", "Indigenous", " communities"),
        ],
    },
    "slide-outline-p3": {
        "heading": "Part 3: Government Response",
        "items": [
            (0, "III. Government Response", None, None),
            (1, "A. Communication problems", None, None),
            (2, "1. Over ", "100", " Aboriginal languages"),
            (2, "2. Need to fight ", "misinformation", None),
            (1, "B. Response so far", None, None),
            (2, "1. Over ", "10,000", " vaccinated in the NT"),
            (2, "2. New cases are going ", "down", None),
        ],
    },
}

M2_INSERTIONS = [
    ("slide-answers-p1c-2", "slide-outline-p1"),  # after p1 answers, before p2 transition
    ("slide-answers-p2c", "slide-outline-p2"),  # after p2 answers, before p3 transition
    ("slide-answers-p3c", "slide-outline-p3"),  # after p3 answers, before discuss transition
]


def add_outline_css(html):
    """Add CSS for outline blank fragments if not already present."""
    css = """
    .reveal .fragment.custom.out-blank { opacity: 1; visibility: inherit; }
    .reveal .fragment.custom.out-blank .blank { display: inline; }
    .reveal .fragment.custom.out-blank .ans { display: none; }
    .reveal .fragment.custom.out-blank.visible .blank { display: none; }
    .reveal .fragment.custom.out-blank.visible .ans { display: inline; }
"""
    if "out-blank" not in html:
        # Insert before </style>
        html = html.replace("</style>", css + "\n</style>")
    return html


def main():
    project = Path(r"C:\PROJECTS\LESSON-PLAN-WRITER-3")

    # Process M3
    m3_path = project / "output" / "M3-LISTENING-GENDER-ROLES" / "slides" / "index.html"
    html = m3_path.read_text(encoding="utf-8")
    html = add_outline_css(html)

    for after_id, out_id in M3_INSERTIONS:
        slide_html = build_outline_slide(
            out_id, M3_OUTLINES[out_id]["heading"], M3_OUTLINES[out_id]["items"], fragment_start=1
        )
        html = insert_after_slide(html, after_id, slide_html)

    m3_path.write_text(html, encoding="utf-8")
    print(f"M3: Inserted {len(M3_INSERTIONS)} outline slides")

    # Process M2
    m2_path = project / "output" / "M2-LISTENING-AI" / "slides" / "index.html"
    html = m2_path.read_text(encoding="utf-8")
    html = add_outline_css(html)

    for after_id, out_id in M2_INSERTIONS:
        slide_html = build_outline_slide(
            out_id, M2_OUTLINES[out_id]["heading"], M2_OUTLINES[out_id]["items"], fragment_start=1
        )
        html = insert_after_slide(html, after_id, slide_html)

    m2_path.write_text(html, encoding="utf-8")
    print(f"M2: Inserted {len(M2_INSERTIONS)} outline slides")


if __name__ == "__main__":
    main()
