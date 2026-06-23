"""Thin re-export — canonical source is PROJECT_ROOT/scripts/lint_slides.py."""

from pathlib import Path

_canonical = Path(__file__).resolve().parents[4] / "scripts" / Path(__file__).name
exec(_canonical.read_text(encoding="utf-8"))
