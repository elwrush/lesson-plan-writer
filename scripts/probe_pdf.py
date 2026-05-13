import fitz

doc = fitz.open(r"typst/PDF/May-13-2026-essay-paper/probe2.pdf")
print(f"Pages: {doc.page_count}")
page = doc[0]
print(f"Page size: {page.rect.width:.1f}x{page.rect.height:.1f}")
drawings = page.get_drawings()
print(f"Drawings: {len(drawings)}")
for d in drawings:
    items = d["items"]
    kind = items[0][0] if items else "?"
    r = d["rect"]
    print(f"  {kind} x=({r[0]:.1f},{r[2]:.1f}) y=({r[1]:.1f},{r[3]:.1f})")
