"""HTML fragment builders for reveal.js slides.

Every function returns a string of well-formed HTML suitable for
insertion into <div class="slides">. All strings are raw HTML --
no templating engine, no escape gotchas. The caller composes them
into the splice file.

Design principles:
- Functions output fragment strings, not file-write or file-read
- No side effects -- pure string builders
- Indentation uses 4-space for readability in output
- All text content is the caller's responsibility since we
  generate static files, not template user input
"""

import html as _html

# ---------------------------------------------------------------------------
# Answer-list row (the most frequently repeated pattern)
# ---------------------------------------------------------------------------


def answer_row(
    num: str,
    question: str,
    answer: str,
    fragment_index: int,
    *,
    is_correct: bool = True,
    why: str | None = None,
    show_icon: bool = True,
) -> str:
    """Generate one answer-list row with fragment fade-up reveal.

    Uses template CSS classes:
      .a-row, .a-num, .a-q, .a-ans, .a-cor, .a-inc, .a-why
    The SKILL.md Step 2b inline <style> block provides:
      .a-q { color: #ffdd00 } -- yellow question text for green backgrounds
      .a-ans { color: #ffdd00 } -- yellow answer text for green backgrounds
    The template base provides the structural flex layout.

    Produces:
        <div class="a-row">
            <span class="a-num">N.</span>
            <span class="a-q">question text</span>
            <span class="fragment fade-up a-ans {a-cor|a-inc}"
                  data-fragment-index="N">
                <i class="fa-solid {check|times}" style="color:#fff;"></i>
                answer text
            </span>
            <span class="a-why fragment fade-up" data-fragment-index="N">
                WHY: explanation
            </span>
        </div>
    """
    cls = "a-cor" if is_correct else "a-inc"
    icon = "fa-check" if is_correct else "fa-times"
    icon_html = f'<i class="fa-solid {icon}" style="color:#fff;"></i> ' if show_icon else ""

    lines = []
    lines.append('        <div class="a-row">')
    lines.append(f'            <span class="a-num">{_html.escape(num)}</span>')
    lines.append(f'            <span class="a-q">{_html.escape(question)}</span>')
    lines.append(
        f'            <span class="fragment fade-up a-ans {cls}" data-fragment-index="{fragment_index}">{icon_html}{_html.escape(answer)}</span>'
    )
    if why:
        lines.append(
            f'            <span class="a-why fragment fade-up" data-fragment-index="{fragment_index}">WHY: {_html.escape(why)}</span>'
        )
    lines.append("        </div>")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Answer slide wrapper
# ---------------------------------------------------------------------------


def answer_slide(
    slide_id: str,
    heading: str,
    rows: list[str],
    *,
    notes: str | None = None,
) -> str:
    """Wrap answer rows in a full green-background answer slide."""
    parts = [
        f'<section id="{slide_id}" data-background-color="#052e0d" data-background-transition="none">',
        f"    <h2>{_html.escape(heading)}</h2>",
        '    <div class="answer-list">',
    ]
    parts.extend(rows)
    parts.append("    </div>")
    if notes:
        parts.append(f'    <aside class="notes">{_html.escape(notes)}</aside>')
    parts.append("</section>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Transition slide
# ---------------------------------------------------------------------------


def transition_slide(slide_id: str, heading: str) -> str:
    """Red-background phase-change signal. Heading only."""
    return (
        f'<section id="{slide_id}" data-background-color="#c0392b" data-background-transition="none">\n'
        f"    <h2>{_html.escape(heading)}</h2>\n"
        f"</section>"
    )


# ---------------------------------------------------------------------------
# Task instruction slide
# ---------------------------------------------------------------------------


def task_slide(
    slide_id: str,
    heading: str,
    instruction: str,
    *,
    audio_src: str | None = None,
    timer: int | None = None,
    notes: str | None = None,
) -> str:
    """Task slide -- brief student-facing instruction + audio OR timer.

    Raises ValueError if both audio_src and timer are set (per CRITICAL rule:
    never place a timer pill on a slide that plays audio).
    """
    if audio_src and timer:
        raise ValueError("task_slide: cannot have both audio_src and timer")

    attrs = f' id="{slide_id}" data-background-color="#1a1a2e"'
    if audio_src:
        attrs += f' data-audio-src="{_html.escape(audio_src)}"'
    if timer is not None:
        attrs += f' data-timer="{timer}"'

    parts = [
        f"<section{attrs}>",
        f"    <h2>{_html.escape(heading)}</h2>",
        f"    <p>{_html.escape(instruction)}</p>",
    ]
    if notes:
        parts.append(f'    <aside class="notes">{_html.escape(notes)}</aside>')
    parts.append("</section>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Pedagogical strategy slide (non-auto-animate)
# ---------------------------------------------------------------------------


def pedagogical_slide(
    slide_id: str,
    content_html: str,
    *,
    notes: str | None = None,
) -> str:
    """Teal-background pedagogical slide wrapper.

    Uses template CSS:
      section.pedagogical h2, h3, p, li all get white text
      with text-shadow:none and h2 gets bottom border.
    """
    parts = [
        f'<section id="{slide_id}" class="pedagogical" data-background-color="#1a237e" data-background-transition="none">',
        f'<section data-auto-animate data-auto-animate-id="{auto_animate_id}" id="{entry_id}" class="pedagogical" data-background-color="#1a237e" data-background-transition="none">',
        f'<section data-auto-animate data-auto-animate-id="{auto_animate_id}" id="{reveal_id}" class="pedagogical" data-background-color="#1a237e" data-background-transition="none">',
        f'<section data-auto-animate data-auto-animate-id="{auto_animate_id}" id="{entry_id}" class="pedagogical" data-background-color="#1a237e" data-background-transition="none">',
        f'<section data-auto-animate data-auto-animate-id="{auto_animate_id}" id="{reveal_id}" class="pedagogical" data-background-color="#1a237e" data-background-transition="none">',
        f'    <h2 data-id="{entry_title_id}">{_html.escape(title)}</h2>',
    ]
    if intro_text:
        lines_reveal.append(f'    <p style="font-size:0.85em;">{_html.escape(intro_text)}</p>')
    lines_reveal.append('    <ul style="font-size:0.8em;">')
    lines_reveal.extend(render_items(underline_color))
    lines_reveal.append("    </ul>")
    if reveal_extra_html:
        lines_reveal.append(reveal_extra_html)
    if reveal_notes:
        lines_reveal.append(f'    <aside class="notes">{_html.escape(reveal_notes)}</aside>')
    lines_reveal.append("</section>")

    return "\n".join(lines_entry), "\n".join(lines_reveal)


# ---------------------------------------------------------------------------
# Auto-animate: grammar rule highlight (Pattern 2)
# ---------------------------------------------------------------------------


def auto_animate_highlight_pair(
    auto_animate_id: str,
    slide_id_prefix: str,
    title: str,
    entry_parts: list[dict],
    reveal_parts: list[dict],
    *,
    rule_text: str | None = None,
    explanation_html: str | None = None,
    reveal_notes: str | None = None,
) -> tuple[str, str]:
    """Generate auto-animate pair for grammar rule transformations.

    ``entry_parts`` and ``reveal_parts`` are lists of dicts:
        {"html": "text content", "data_id": "optional-data-id", "style": "optional-inline-style"}

    Elements with matching data_id animate between entry and reveal states.
    This is Pattern 2 (grammar rules -- M3-Grammar-1).
    """

    def render_parts(parts: list[dict]) -> list[str]:
        result = []
        for p in parts:
            html_text = p.get("html", "")
            data_id = p.get("data_id")
            style = p.get("style", "")
            if data_id:
                if style:
                    result.append(f'<span data-id="{data_id}" style="{style}">{html_text}</span>')
                else:
                    result.append(f'<span data-id="{data_id}">{html_text}</span>')
            else:
                if style:
                    result.append(f'<span style="{style}">{html_text}</span>')
                else:
                    result.append(html_text)
        return result

    entry_id = f"{slide_id_prefix}-entry"
    reveal_id = f"{slide_id_prefix}-reveal"

    entry_lines = [
        f'<section data-auto-animate data-auto-animate-id="{auto_animate_id}" id="{entry_id}" class="pedagogical" data-background-color="#1a237e" data-background-transition="none">',
        f"    <h2>{_html.escape(title)}</h2>",
    ]
    if rule_text:
        entry_lines.append(f"    <p><u><strong>{_html.escape(rule_text)}</strong></u></p>")
    entry_lines.append(
        f'    <p data-id="{auto_animate_id}-sentence"><em>{"".join(render_parts(entry_parts))}</em></p>'
    )
    entry_lines.append("</section>")

    reveal_lines = [
        f'<section data-auto-animate data-auto-animate-id="{auto_animate_id}" id="{reveal_id}" class="pedagogical" data-background-color="#1a237e" data-background-transition="none">',
        f"    <h2>{_html.escape(title)}</h2>",
    ]
    if rule_text:
        reveal_lines.append(f"    <p><u><strong>{_html.escape(rule_text)}</strong></u></p>")
    reveal_lines.append(
        f'    <p data-id="{auto_animate_id}-sentence"><em>{"".join(render_parts(reveal_parts))}</em></p>'
    )
    if explanation_html:
        reveal_lines.append(f"    {explanation_html}")
    if reveal_notes:
        reveal_lines.append(f'    <aside class="notes">{_html.escape(reveal_notes)}</aside>')
    reveal_lines.append("</section>")

    return "\n".join(entry_lines), "\n".join(reveal_lines)


# ---------------------------------------------------------------------------
# Auto-animate: S/V/O annotation pair (Pattern 3)
# ---------------------------------------------------------------------------


def auto_animate_svo_pair(
    auto_animate_id: str,
    slide_id_prefix: str,
    title: str,
    subject_word: str,
    verb_word: str,
    object_word: str,
    *,
    reveal_extra_html: str | None = None,
    reveal_notes: str | None = None,
) -> tuple[str, str]:
    """Generate S/V/O annotation auto-animate pair (Pattern 3).

    Uses template CSS classes (.a-s, .a-v, .a-ls, .a-lv) for annotation
    styling instead of raw inline styles. Object gets inline border since
    no .a-o class exists in the template.

    Entry slide: plain sentence with invisible superscripts and transparent borders.
    Reveal slide: colored borders + visible S/V/O labels + legend row.
    Used for grammar lead-in demonstrations (M2-Grammar-2 pattern).
    """
    entry_id = f"{slide_id_prefix}-entry"
    reveal_id = f"{slide_id_prefix}-annotated"

    entry = (
        f'<section id="{entry_id}" data-auto-animate data-auto-animate-id="{auto_animate_id}" data-background-color="#1a1a2e">\n'
        f'    <h2 data-id="title">{_html.escape(title)}</h2>\n'
        f'    <p style="font-size: 1.3em; margin-top: 1em;">\n'
        f'        <span data-id="subject" class="a-s" style="border-bottom: 2px solid transparent;">\n'
        f'            <sup style="color: transparent; font-size: 0.5em;">S </sup>{_html.escape(subject_word)}\n'
        f"        </span>\n"
        f'        <span data-id="verb" class="a-v" style="border-bottom: 2px solid transparent;">\n'
        f'            <sup style="color: transparent; font-size: 0.5em;">V </sup>{_html.escape(verb_word)}\n'
        f"        </span>\n"
        f'        <span data-id="object" style="border: 2px solid transparent;">\n'
        f'            <sup style="color: transparent; font-size: 0.5em;">O </sup>{_html.escape(object_word)}\n'
        f"        </span>\n"
        f"    </p>\n"
        f"</section>"
    )

    reveal = (
        f'<section id="{reveal_id}" data-auto-animate data-auto-animate-id="{auto_animate_id}" data-background-color="#1a1a2e">\n'
        f'    <h2 data-id="title">{_html.escape(title)}</h2>\n'
        f'    <p style="font-size: 1.3em; margin-top: 1em;">\n'
        f'        <span data-id="subject" class="a-s">\n'
        f'            <span class="a-ls">S </span>{_html.escape(subject_word)}\n'
        f"        </span>\n"
        f'        <span data-id="verb" class="a-v" style="box-shadow: 0 5px 0 0 #ffdd00;">\n'
        f'            <span class="a-lv">V </span>{_html.escape(verb_word)}\n'
        f"        </span>\n"
        f'        <span data-id="object" style="border: 2px solid #fff; padding: 0 4px; border-radius: 4px;">\n'
        f'            <sup style="color: #fff; font-size: 0.5em;">O </sup>{_html.escape(object_word)}\n'
        f"        </span>\n"
        f"    </p>\n"
        f'    <p style="font-size: 0.85em; margin-top: 0.3em; color: #fff;">\n'
        f'        <span style="color: #ffdd00;"><strong>Subject</strong></span>\n'
        f"        &nbsp;&middot;&nbsp;\n"
        f'        <span style="color: #fff;"><strong>Verb</strong></span>\n'
        f"        &nbsp;&middot;&nbsp;\n"
        f'        <span style="color: #fff;"><strong>Object</strong></span>\n'
        f"    </p>\n"
    )
    if reveal_extra_html:
        reveal += f"    {reveal_extra_html}\n"
    if reveal_notes:
        reveal += f'    <aside class="notes">{_html.escape(reveal_notes)}</aside>\n'
    reveal += "</section>"

    return entry, reveal
