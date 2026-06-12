"""Generate M2 Diphtheria worksheets as A4 booklets with student demographics."""

import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import fitz

PROJECT_ROOT = Path(r"C:\PROJECTS\LESSON-PLAN-WRITER-3")
FONT_PATH = (
    Path(os.environ.get("APPDATA"))
    / "TinyTeX"
    / "texmf-dist"
    / "fonts"
    / "opentype"
    / "google"
    / "roboto"
)
OUT_DIR = PROJECT_ROOT / "PDF" / "M2-DIPHTHERIA-BOOKLETS"

STUDENTS = [
    ("30321", "Alin", "M2-4A"),
    ("30399", "Mick", "M2-4A"),
    ("30444", "Arlong", "M2-4A"),
    ("30570", "Atan", "M2-4A"),
    ("30584", "Mita", "M2-4A"),
    ("32376", "Boss", "M2-4A"),
    ("33262", "Plearn", "M2-4A"),
    ("34317", "Khan", "M2-4A"),
    ("35993", "Gimji", "M2-4A"),
    ("35994", "Tee", "M2-4A"),
    ("35995", "Porsche", "M2-4A"),
    ("36000", "Tul", "M2-4A"),
    ("36001", "Poch", "M2-4A"),
    ("36018", "Pooh", "M2-4A"),
    ("36047", "Disney", "M2-4A"),
    ("36052", "Benz", "M2-4A"),
    ("36111", "Wan", "M2-4A"),
    ("36122", "Yada", "M2-4A"),
    ("36127", "Pang Pang", "M2-4A"),
    ("29765", "August", "M2-5A"),
    ("30334", "Pran", "M2-5A"),
    ("30335", "Prin R", "M2-5A"),
    ("30365", "Anpan", "M2-5A"),
    ("30378", "Ti", "M2-5A"),
    ("30489", "Mil", "M2-5A"),
    ("30490", "Mile", "M2-5A"),
    ("30847", "Tonnam", "M2-5A"),
    ("33157", "Milin", "M2-5A"),
    ("33185", "Auto", "M2-5A"),
    ("35128", "Khun", "M2-5A"),
    ("35996", "Fah", "M2-5A"),
    ("36006", "Indy", "M2-5A"),
    ("36013", "Prin A", "M2-5A"),
    ("36023", "Good", "M2-5A"),
    ("36027", "Bluebell", "M2-5A"),
    ("36029", "Ai", "M2-5A"),
    ("36036", "Yada", "M2-5A"),
    ("36039", "Beya", "M2-5A"),
    ("36171", "Tietie", "M2-5A"),
]

TYPST_HEAD = """#set text(font: "Roboto", size: 14pt)
#set par(leading: 0.65em, spacing: 0.3em)
#show: doc => {
  set page(paper: "a4", margin: (x: 1.5cm, top: 1.5cm, bottom: 1.5cm))
  doc
}

#let ls = 24pt
#let ul(n) = str("_") * n
#let ruled-lines(n) = {
  for i in range(n) {
    if i == 0 { v(1.2em) } else { v(ls / 2) }
    line(length: 100%, stroke: 0.4pt + black)
    v(ls / 2)
  }
}

#block(
  stroke: (bottom: 0.5pt + black),
  inset: (bottom: 4pt),
  grid(
    columns: (1fr, 2fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image("/templates/ACT.png", height: 1.2cm),
    text(size: 14pt, weight: "bold")[Mathayom Program],
    image("/templates/cambridge.png", height: 1.6cm),
  )
)
#v(8pt)
#grid(
  columns: (auto, 1fr, auto, 1fr, auto, 1fr),
  column-gutter: 0.3em,
  align: bottom + left,
  [*CLASS:*], [CLASS_PLACEHOLDER],
  [*ID:*], [ID_PLACEHOLDER],
  [*NAME:*], [NAME_PLACEHOLDER],
)
#v(4pt)
#line(length: 100%, stroke: 0.4pt + black)
#v(10pt)
"""

TYPST_BODY = """#align(center, text(size: 18pt, weight: "bold")[BTN Classroom - Listening Worksheet])
#align(center, text(size: 15pt)[Diphtheria])
#align(center, text(size: 12pt)[4 June 2026])
#v(0.3em)

#block(
  stroke: (left: 2pt + black),
  inset: 6pt,
  text(size: 12pt)[
    *Instructions:* You will watch the video three times. Each time, focus on a different part of the outline. Each gap is no more than *three words*.
  ]
)
#v(0.4em)

= Part 1: History of Diphtheria
#v(0.1em)

I. History of Diphtheria \\
  #h(1.5em) A. About the disease \\
    #h(3em) 1\\. First described by #ul(15) \\
    #h(3em) 2\\. Greek name means #ul(15) \\
  #h(1.5em) B. Medical breakthrough (1890s) \\
    #h(3em) 1\\. Scientists developed #ul(15) therapy \\
    #h(3em) 2\\. Won the first Nobel Prize in #ul(10) \\
  #h(1.5em) C. Safer vaccine (1923) \\
    #h(3em) 1\\. A #ul(15) vaccine was made

#v(0.3em)
*Comprehension Questions*
#v(0.1em)
The disease was first described 2,400 years ago, but the vaccine took until 1923. What does this timeline tell us about how medical science develops?
#ruled-lines(2)

How did using animals to produce antibodies help scientists develop a treatment before they had a vaccine?
#ruled-lines(2)

#pagebreak()
= Part 2: Vaccines and Outbreak
#v(0.1em)

II. Vaccines and Outbreak in Australia \\
  #h(1.5em) A. Vaccination in Australia \\
    #h(3em) 1\\. #ul(6)% of 5-year-olds are vaccinated \\
    #h(3em) 2\\. A #ul(15) is given at ages 11-13 \\
  #h(1.5em) B. Current outbreak \\
    #h(3em) 1\\. More than #ul(6) cases \\
    #h(3em) 2\\. Many cases in #ul(15) communities

#v(0.3em)
*Comprehension Questions*
#v(0.1em)
93% of 5-year-olds are vaccinated, but there is still an outbreak. Why does this gap in vaccination matter for protecting the whole community?
#ruled-lines(2)

The outbreak is mostly in Indigenous communities. What barriers might make it harder for people in remote areas to access vaccines?
#ruled-lines(2)

#pagebreak()
= Part 3: Government Response
#v(0.1em)

III. Government Response \\
  #h(1.5em) A. Communication problems \\
    #h(3em) 1\\. Over #ul(6) Aboriginal languages \\
    #h(3em) 2\\. Need to fight #ul(15) \\
  #h(1.5em) B. Response so far \\
    #h(3em) 1\\. Over #ul(10) vaccinated in the NT \\
    #h(3em) 2\\. New cases are going #ul(15)

#v(0.3em)
*Comprehension Questions*
#v(0.1em)
Minister McCarthy says the government needs to communicate in over 100 languages. Why is language access important for public health campaigns?
#ruled-lines(2)

Minister Butler says diseases like diphtheria are re-emerging where vaccination rates drop. What does this tell us about the importance of maintaining vaccination programs?
#ruled-lines(2)

= Part 4: Discussion
#v(0.1em)

== Discussion Techniques

Use these phrases to introduce your views and respond to others.

*Introducing your point of view:*
- "I think that ... because ..."
- "In my opinion, ..."
- "It seems to me that ..."
- "One thing I noticed was ..."

*Acknowledging someone else\'s point of view:*
- "That\'s a good point. I\'d add that ..."
- "I see what you mean. However, ..."
- "I hadn\'t thought of it that way. I think ..."
- "That\'s interesting. But what about ...?"

#v(0.3em)
== Think-Pair-Share

1\\. Should vaccination be compulsory for everyone? Use at least one piece of evidence from the video.

#text(size: 12pt)[*Structure:* Say what you think \\ " Give evidence from the video \\ " Summarise]

#ruled-lines(4)

2\\. How can governments make sure everyone has access to vaccines, especially in remote communities?

#ruled-lines(4)
"""


def make_student_typ(sid, name, cls):
    head = (
        TYPST_HEAD.replace("CLASS_PLACEHOLDER", cls)
        .replace("ID_PLACEHOLDER", sid)
        .replace("NAME_PLACEHOLDER", name)
    )
    return head + TYPST_BODY


def pad_to_4(pdf_path):
    doc = fitz.open(str(pdf_path))
    n = len(doc)
    r = n % 4
    if r == 0:
        doc.close()
        return n
    blank = fitz.open()
    blank.new_page(width=595, height=842)
    for _ in range(4 - r):
        doc.insert_pdf(blank)
    blank.close()
    tmp = pdf_path.with_suffix(".tmp.pdf")
    doc.save(str(tmp))
    doc.close()
    tmp.replace(pdf_path)
    return n + (4 - r)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    indir = Path(r"C:\PROJECTS\LESSON-PLAN-WRITER-3\tmp") / "m2-individual"
    indir.mkdir(exist_ok=True)

    by_class = {}
    for sid, name, cls in STUDENTS:
        by_class.setdefault(cls, []).append((sid, name))

    generated = []

    for sid, name, cls in STUDENTS:
        safe = name.replace(" ", "_").replace("(", "").replace(")", "").replace("'", "_")
        typ_path = indir / f"{sid}-{safe}.typ"
        pdf_path = indir / f"{sid}-{safe}.pdf"

        typ_content = make_student_typ(sid, name, cls)
        typ_path.write_text(typ_content, encoding="utf-8")

        cmd = [
            "typst",
            "compile",
            "--root",
            str(PROJECT_ROOT),
            "--font-path",
            str(FONT_PATH),
            str(typ_path),
            str(pdf_path),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print(f"FAIL {sid}-{name}: {r.stderr[:200]}")
            continue

        final = pad_to_4(pdf_path)
        print(f"  {cls} {sid}-{name}: {final}p")
        generated.append((cls, sid, name, pdf_path))

    # Combine by class
    for cls in sorted(by_class):
        pdfs = [p for c, _, _, p in generated if c == cls]
        if not pdfs:
            continue
        combined = fitz.open()
        for p in pdfs:
            d = fitz.open(str(p))
            combined.insert_pdf(d)
            d.close()
        out = OUT_DIR / f"{cls.replace('-', '_')}-diphtheria-booklet.pdf"
        combined.save(str(out))
        combined.close()
        total_pages = sum(len(fitz.open(str(p))) for p in pdfs)
        print(f"\n{cls}: {len(pdfs)} students -> {out} ({total_pages} pages)")

    # Mega combined
    all_pdfs = [p for _, _, _, p in generated]
    if all_pdfs:
        mega = fitz.open()
        for p in all_pdfs:
            d = fitz.open(str(p))
            mega.insert_pdf(d)
            d.close()
        mega_path = OUT_DIR / "ALL-M2-diphtheria-booklet.pdf"
        mega.save(str(mega_path))
        mega.close()
        print(f"\nALL: {mega_path}")


if __name__ == "__main__":
    main()
    # Validate
    import subprocess as _sp

    result = _sp.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "validate_booklet.py"),
            "--dir",
            str(OUT_DIR),
            "--strict",
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)
