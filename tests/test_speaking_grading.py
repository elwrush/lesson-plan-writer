"""
test_speaking_grading.py — Red-green test for the speaking grading sheet pipeline.

Verifies that:
- The Markdown → Pandoc → Typst → PDF pipeline compiles successfully
- The PDF is non-empty and contains expected content (title, table headers, observations box)
"""

import subprocess
import sys
import os
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

ROOT = Path(__file__).parent.parent

# Known working tool paths (same as compile_speech.py)
PANDOC = r"C:\Program Files\Pandoc\pandoc.exe"
TYPST = (
    r"C:\Users\elwru\AppData\Local\Microsoft\WinGet\Packages"
    r"\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\typst-x86_64-pc-windows-msvc\typst.EXE"
)
FONT = (
    Path(os.environ.get("APPDATA", ""))
    / "TinyTeX"
    / "texmf-dist"
    / "fonts"
    / "opentype"
    / "google"
    / "roboto"
)
TEMPLATE = ROOT / "templates" / "speaking-grading.typ"
LUA_FILTER = ROOT / "scripts" / "speaking-grading-sheet.lua"

MINIMAL_MD = """---
class: M2-4A
student_id: "30321"
name: "Alin"
---

::: {.score}
:::

# Speaking Grading Sheet \u2014 Pronunciation

| Band | Intonation | Intelligibility | Sentence and Word Stress | Individual Sounds |
|------|-----------|----------------|------------------------|--------------------|
| 5 | Tests intonation. | Tests intelligibility. | Tests stress. | Tests sounds. |
| 4 | Between 5 and 3. | Between 5 and 3. | Between 5 and 3. | Between 5 and 3. |
| 3 | OK in patches. | Mostly clear. | OK in patches. | Some muddled. |
| 2 | Between 3 and 1. | Between 3 and 1. | Between 3 and 1. | Between 3 and 1. |
| 1 | Defects constant. | Often unclear. | Errors constant. | Many distorted. |

::: {.observations}
**Special Observations**
:::
"""


def _tools_available():
    """Check if pandoc and typst are accessible at known paths."""
    return Path(PANDOC).exists() and Path(TYPST).exists()


class TestSpeakingGradingPipeline:
    """End-to-end tests for the speaking grading sheet pipeline."""

    def test_md_body_contains_expected_elements(self):
        """Red: verify the test Markdown has all required elements."""
        assert "class: M2-4A" in MINIMAL_MD
        assert "student_id: \"30321\"" in MINIMAL_MD
        assert "name: \"Alin\"" in MINIMAL_MD
        assert "Speaking Grading Sheet" in MINIMAL_MD
        assert "::: {.score}" in MINIMAL_MD
        assert "::: {.observations}" in MINIMAL_MD
        assert "Special Observations" in MINIMAL_MD
        assert "Intonation" in MINIMAL_MD
        assert "Intelligibility" in MINIMAL_MD

    def test_lua_filter_loads_and_transforms_score_div(self):
        """Red: pipeline with .score div should produce a SCORE table in Typst."""
        if not _tools_available():
            pytest.skip("Pandoc or Typst not available")

        md_path = ROOT / "tmp" / "test_speaking_grading.md"
        typ_path = md_path.with_suffix(".typ")
        pdf_path = ROOT / "PDF" / "PRONUNCIATION-MARKING-SHEETS" / "test_grading_pipeline.pdf"

        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(MINIMAL_MD, encoding="utf-8")

        try:
            # Step 1: Pandoc → Typst
            r = subprocess.run(
                [PANDOC, str(md_path), "-t", "typst",
                 "--template", str(TEMPLATE),
                 "--lua-filter", str(LUA_FILTER),
                 "-o", str(typ_path), "--wrap=none"],
                capture_output=True, text=True, timeout=30,
            )
            assert r.returncode == 0, f"Pandoc failed: {r.stderr[:300]}"

            # Verify Typst output contains key elements
            typ_content = typ_path.read_text(encoding="utf-8")
            assert "SCORE" in typ_content, "SCORE table should be in Typst output"
            assert "Special Observations" in typ_content
            assert "Intonation" in typ_content

            # Step 2: Typst → PDF
            r = subprocess.run(
                [TYPST, "compile", "--root", str(ROOT),
                 "--font-path", str(FONT),
                 str(typ_path), str(pdf_path)],
                capture_output=True, text=True, timeout=60,
            )
            assert r.returncode == 0, f"Typst failed: {r.stderr[:300]}"
            assert pdf_path.exists(), "PDF should exist"
            assert pdf_path.stat().st_size > 10000, "PDF should be >10KB"

            # Verify PDF contains expected text
            try:
                import fitz
                doc = fitz.open(str(pdf_path))
                assert len(doc) == 1, "Should be a single page"
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()

                assert "Alin" in text, "PDF should contain student name"
                assert "M2-4A" in text, "PDF should contain class"
                assert "SCORE" in text, "PDF should contain SCORE label"
                assert "Intonation" in text, "PDF should contain Intonation"
                assert "Special Observations" in text
            except ImportError:
                pytest.skip("PyMuPDF not available for PDF text extraction")

        finally:
            if md_path.exists():
                md_path.unlink()
            if typ_path.exists():
                typ_path.unlink()
            if pdf_path.exists():
                pdf_path.unlink()

    def test_full_pipeline_produces_valid_pdf(self):
        """Green: full Markdown → Pandoc → Typst → PDF pipeline produces valid PDF."""
        if not _tools_available():
            pytest.skip("Pandoc or Typst not available")

        md_path = ROOT / "tmp" / "test_speaking_grading.md"
        typ_path = md_path.with_suffix(".typ")
        pdf_path = ROOT / "PDF" / "PRONUNCIATION-MARKING-SHEETS" / "test_grading_pipeline.pdf"

        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(MINIMAL_MD, encoding="utf-8")

        try:
            r = subprocess.run(
                [PANDOC, str(md_path), "-t", "typst",
                 "--template", str(TEMPLATE),
                 "--lua-filter", str(LUA_FILTER),
                 "-o", str(typ_path), "--wrap=none"],
                capture_output=True, text=True, timeout=30,
            )
            assert r.returncode == 0

            r = subprocess.run(
                [TYPST, "compile", "--root", str(ROOT),
                 "--font-path", str(FONT),
                 str(typ_path), str(pdf_path)],
                capture_output=True, text=True, timeout=60,
            )
            assert r.returncode == 0
            assert pdf_path.exists()
            assert pdf_path.stat().st_size > 10000

        finally:
            if md_path.exists():
                md_path.unlink()
            if typ_path.exists():
                typ_path.unlink()
            if pdf_path.exists():
                pdf_path.unlink()
