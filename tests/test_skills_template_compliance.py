"""
test_skills_template_compliance.py — Enforces that every project-local
SKILL.md follows .kilo/skills/_TEMPLATE.md structure.

Required sections (from _TEMPLATE.md):
  1. YAML frontmatter (name, description)
  2. ## Purpose with **Output:** line
  3. ## When to Use with conditions, Trigger, and anti-pattern
  4. ## Workflow (N Steps) with ### Step N: numbering
  5. ## Examples with at least 2 examples
  6. ## Error Handling with symptom/cause/fix table
  7. ## Reference linking to reference/ files
  8. ## Scripts shipping with the skill
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / ".kilo" / "skills"
TEMPLATE_PATH = SKILLS_DIR / "_TEMPLATE.md"

SKILL_DIRS = sorted(
    d
    for d in SKILLS_DIR.iterdir()
    if d.is_dir() and d.name != "_TEMPLATE.md" and (d / "SKILL.md").exists()
)


def _load_skills():
    """Return list of (skill_name, text) for every project SKILL.md."""
    result = []
    for d in SKILL_DIRS:
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        result.append((d.name, text))
    return result


# ── Frontmatter ────────────────────────────────────────────────────────


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_frontmatter_name(name, text):
    assert re.search(r"^name:\s*\S", text, re.MULTILINE), f"{name}: missing 'name' field"


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_frontmatter_description(name, text):
    assert re.search(r"^description:\s*\S", text, re.MULTILINE), (
        f"{name}: missing 'description' field"
    )


# ── Purpose ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_purpose_section(name, text):
    assert "## Purpose" in text, f"{name}: missing ## Purpose section"


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_output_line(name, text):
    assert re.search(r"\*\*Output:\*\*", text), f"{name}: missing **Output:** line in Purpose"


# ── When to Use ────────────────────────────────────────────────────────


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_when_to_use(name, text):
    assert "## When to Use" in text, f"{name}: missing ## When to Use section"


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_trigger(name, text):
    assert re.search(r"\*\*Trigger:\*\*", text), f"{name}: missing **Trigger:** in When to Use"


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_antipattern(name, text):
    assert re.search(r"Do NOT use|anti-pattern", text, re.IGNORECASE), (
        f"{name}: missing anti-pattern in When to Use"
    )


# ── Workflow ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_workflow(name, text):
    assert re.search(r"## Workflow", text), f"{name}: missing ## Workflow section"


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_numbered_steps(name, text):
    assert re.search(r"### Step \d", text), f"{name}: Workflow has no numbered steps"


# ── Examples ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_examples(name, text):
    assert "## Examples" in text, f"{name}: missing ## Examples section"


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_two_examples(name, text):
    count = len(re.findall(r"### Example \d", text))
    assert count >= 2, f"{name}: only {count} example(s), need >= 2"


# ── Error Handling ──────────────────────────────────────────────────────


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_error_handling(name, text):
    assert "## Error Handling" in text, f"{name}: missing ## Error Handling section"


# ── Reference ───────────────────────────────────────────────────────────


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_reference(name, text):
    assert "## Reference" in text, f"{name}: missing ## Reference section"


# ── Scripts ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name,text", _load_skills(), ids=[s[0] for s in _load_skills()])
def test_has_scripts(name, text):
    assert "## Scripts" in text, f"{name}: missing ## Scripts section"
