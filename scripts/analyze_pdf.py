import fitz

doc = fitz.open(r"typst/PDF/May-13-2026-essay-paper/index.pdf")
print(f"Pages: {doc.page_count}")

for i, page in enumerate(doc):
    print(f"\n=== Page {i + 1} (height={page.rect.height:.1f} pt) ===")

    # Text positions
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                for s in line["spans"]:
                    print(
                        f"  Text: '{s['text']}' at y={s['origin'][1]:.1f}, top={s['bbox'][1]:.1f}"
                    )

    # Drawing positions
    drawings = page.get_drawings()
    for d in drawings:
        kind = d["items"][0][0] if d["items"] else "?"
        y1 = d["rect"][1]
        y2 = d["rect"][3]
        x1 = d["rect"][0]
        x2 = d["rect"][2]
        # Thin horizontal lines are ruled lines
        is_thin = (y2 - y1) < 1
        is_wide = (x2 - x1) > 100
        tag = "RULED" if is_thin and is_wide else "LINE"
        print(f"  {tag} y={y1:.1f} to y={y2:.1f}, x={x1:.1f} to x={x2:.1f}")
