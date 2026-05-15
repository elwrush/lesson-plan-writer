"""
migrate_answer_keys.py - Convert existing .md answer keys to .typ

Finds all .md answer key files referenced in output JSON lesson plans,
converts them to .typ using md_to_typst(), and updates the JSON
references. After migration, answer keys are plain Typst markup,
eliminating the need for markdown conversion at compile time.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from json_to_pdf import PROJECT_ROOT, md_to_typst


def migrate_json_answer_keys(json_path):
    """Migrate a single JSON lesson plan's answer key from .md to .typ."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    ak = data.get("answer_key", "")
    if not ak or ak == "none":
        print("  (no answer key)")
        return False

    ak_path = Path(ak)
    if ak_path.suffix == ".typ":
        print(f"  (already .typ: {ak_path.name})")
        return False

    if ak_path.suffix != ".md":
        print(f"  (unexpected format: {ak_path.suffix})")
        return False

    if not ak_path.exists():
        print(f"  (file not found: {ak_path})")
        return False

    # Convert .md -> .typ
    md_content = ak_path.read_text(encoding="utf-8")
    typ_content = md_to_typst(md_content)

    typ_path = ak_path.with_suffix(".typ")
    typ_path.write_text(typ_content, encoding="utf-8")

    # Update JSON reference to .typ
    data["answer_key"] = str(typ_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"  {ak_path.name} -> {typ_path.name}")
    return True


def main():
    output_dir = PROJECT_ROOT / "output"
    if not output_dir.exists():
        print("No output/ directory found.")
        return

    json_files = list(output_dir.rglob("*.json"))
    if not json_files:
        print("No JSON files found in output/")
        return

    print(f"Found {len(json_files)} JSON file(s) in output/")
    converted = 0
    for jf in sorted(json_files):
        rel = jf.relative_to(PROJECT_ROOT)
        print(f"\n{rel}:")
        if migrate_json_answer_keys(jf):
            converted += 1

    print(f"\nDone. Converted {converted} answer key(s).")


if __name__ == "__main__":
    main()
