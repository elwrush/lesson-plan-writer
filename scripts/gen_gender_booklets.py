"""Generate M3 Gender Roles worksheets as A5 booklets with student demographics."""

import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import fitz

PROJECT_ROOT = Path(r"C:\PROJECTS\LESSON-PLAN-WRITER-3")
TEMP_DIR = Path(os.environ.get("TEMP", "C:\\Users\\elwru\\AppData\\Local\\Temp")) / "kilo"
FONT_PATH = (
    Path(os.environ.get("APPDATA"))
    / "TinyTeX"
    / "texmf-dist"
    / "fonts"
    / "opentype"
    / "google"
    / "roboto"
)
CLASS_GROUPS_DIR = Path(r"C:\PROJECTS\LESSON-PLAN-WRITER-3\PDF\M3-GENDER-ROLES-BOOKLETS")

STUDENTS = [
    ("29643", "Aat", "M3-3A"),
    ("29530", "Army", "M3-3A"),
    ("35330", "Elenna", "M3-3A"),
    ("33919", "Fuji", "M3-3A"),
    ("30055", "Jomtub", "M3-3A"),
    ("30858", "Katie", "M3-3A"),
    ("34174", "Krabi", "M3-3A"),
    ("31614", "Lily", "M3-3A"),
    ("29866", "Mawin", "M3-3A"),
    ("29713", "PK", "M3-3A"),
    ("29580", "Plern", "M3-3A"),
    ("29799", "Ploy", "M3-3A"),
    ("32217", "Poopup", "M3-3A"),
    ("30082", "Porsch", "M3-3A"),
    ("29591", "Preme", "M3-3A"),
    ("29547", "Proud", "M3-3A"),
    ("33266", "Taia", "M3-3A"),
    ("29613", "Tam", "M3-3A"),
    ("29528", "Tonnam", "M3-3A"),
    ("35309", "Atom", "M3-4A"),
    ("29886", "Captain", "M3-4A"),
    ("34926", "Chopin", "M3-4A"),
    ("29720", "Dragon", "M3-4A"),
    ("29589", "Elle", "M3-4A"),
    ("34931", "Frame", "M3-4A"),
    ("34912", "Hero", "M3-4A"),
    ("29579", "Ka-nhom", "M3-4A"),
    ("33896", "Kati", "M3-4A"),
    ("29561", "Mathew", "M3-4A"),
    ("29832", "Nene", "M3-4A"),
    ("29844", "Ome", "M3-4A"),
    ("29665", "Peace", "M3-4A"),
    ("34924", "Ping-Ping", "M3-4A"),
    ("29599", "Praewwan", "M3-4A"),
    ("34936", "Richter", "M3-4A"),
    ("29623", "Siri", "M3-4A"),
    ("31416", "Tonnam", "M3-4A"),
    ("29604", "Yayar", "M3-4A"),
    ("29793", "Charles", "M3-5A"),
    ("29576", "Dee", "M3-5A"),
    ("34927", "Eri", "M3-5A"),
    ("34933", "Grace", "M3-5A"),
    ("29727", "Mark", "M3-5A"),
    ("37120", "Nadia", "M3-5A"),
    ("34932", "Natee", "M3-5A"),
    ("29745", "Pheem", "M3-5A"),
    ("29710", "PingPing", "M3-5A"),
    ("29749", "Pipe", "M3-5A"),
    ("29769", "Posh", "M3-5A"),
    ("30942", "Praewa", "M3-5A"),
    ("29615", "Punch", "M3-5A"),
    ("34929", "Saint", "M3-5A"),
    ("29508", "Satang", "M3-5A"),
    ("34034", "Singto", "M3-5A"),
    ("34091", "Tanya", "M3-5A"),
    ("30221", "Tata", "M3-5A"),
    ("29798", "Yaya (Kanchisar)", "M3-5A"),
    ("29584", "Yaya (Nadi)", "M3-5A"),
]

TYPST_HEAD = """#set text(font: "Roboto", size: 14pt)
#set par(leading: 0.65em)
#show: doc => {
  set page(paper: "a4", margin: (x: 1.5cm, top: 1cm, bottom: 1cm))
  doc
}

#let fl = box(width: 3.5cm, stroke: (bottom: 0.5pt + black))
#let fls = box(width: 1.5cm, stroke: (bottom: 0.5pt + black))
#let fll = box(width: 4.5cm, stroke: (bottom: 0.5pt + black))

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
#line(length: 100%, stroke: 0.3pt + luma(160))
#v(10pt)
"""

TYPST_BODY = """#align(center, text(size: 16pt, weight: "bold")[BTN High - Listening Worksheet])
#align(center, text(size: 13pt)[Gen Z Gender Roles])
#align(center, text(size: 9pt, fill: luma(80))[Episode 15 - 25 March 2026])
#v(0.3em)

#block(
  stroke: (left: 2pt + black),
  inset: 6pt,
  text(size: 11pt)[
    *Instructions:* Emerging (B1): complete the outline (max 3 words per gap). Established (B2): take your own notes, then answer comprehension questions after each section.
  ]
)
#v(0.4em)

= Part 1: Traditional Gender Roles
#v(0.2em)
I. Traditional Gender Roles in Society
  #h(1.5em) A. 1950s TV shows portrayed clear gender roles
    #h(3em) 1. Women shown as the #fll
    #h(3em) 2. Men shown as the #fll
  #h(1.5em) B. Kings College study — 23,000 people from 29 countries
    #h(3em) 1. Gen Z holds the #fll traditional beliefs
    #h(3em) 2. #fls of Gen Z men believe a wife should obey her husband
    #h(3em) 3. #fls of Gen Z men say a husband should have the final word
  #h(1.5em) C. Attitudes beyond the home
    #h(3em) 1. #fls of Gen Z men say enough has been done for gender equality
    #h(3em) 2. #fls of Gen Z men feel men are now discriminated against
#v(0.3em)
*Comprehension Questions*
#v(0.2em)
1. What did the Kings College study find about Gen Z's beliefs?
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))
2. What percentage of Gen Z men think a husband should have the final word?
   #line(length: 100%, stroke: 0.3pt + luma(120))
3. How do Gen Z women's views compare to Gen Z men's?
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))

#pagebreak()
= Part 2: The Role of Social Media
#v(0.2em)
II. The Role of Social Media
  #h(1.5em) A. Josh Glover — facilitator at #fll
    #h(3em) 1. His organisation tackles #fll in schools
    #h(3em) 2. Social media helps bring back #fll gender norms
  #h(1.5em) B. How social media algorithms work
    #h(3em) 1. Algorithms create #fll where users hear agreeing voices
    #h(3em) 2. No one presents #fll opinions
    #h(3em) 3. Users only see opinions that get debunked or #fll
  #h(1.5em) C. The definition problem
    #h(3em) 1. Teenage boys' definition of #fll differs from the intended meaning
    #h(3em) 2. This results from algorithms and lack of #fll with people who hold different views
#v(0.3em)
*Comprehension Questions*
#v(0.2em)
1. What is Man Cave and what does Josh Glover say their work involves?
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))
2. How do social media algorithms affect young people's views?
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))
3. How do teenage boys define feminism vs its intended meaning?
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))

#pagebreak()
= Part 3: Tradwives and Solutions
#v(0.2em)
III. Tradwives and Solutions
  #h(1.5em) A. "Tradwife" influencers
    #h(3em) 1. Glamorise #fll lifestyles
    #h(3em) 2. Create content about cooking, cleaning, and #fll roles
  #h(1.5em) B. Effects on young people
    #h(3em) 1. University of Melbourne study of 2,300 adults and 1,100 young people
    #h(3em) 2. Support for violence to resist feminism was highest among #fll
    #h(3em) 3. Around #fls of boys aged 13-17 agree women lie about domestic and sexual violence
  #h(1.5em) C. Josh's perspective on solutions
    #h(3em) 1. Two parts needed: #fll and problem-solving
    #h(3em) 2. Need for #fll conversations where people are not judged
    #h(3em) 3. Importance of #fll — older generations investing in younger people
#v(0.3em)
*Comprehension Questions*
#v(0.2em)
1. What is a "tradwife" and what kind of content do they create?
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))
2. What did the University of Melbourne study find about adolescent boys?
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))
3. What two things are needed to solve the problem, and why are safe conversations important?
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))
   #line(length: 100%, stroke: 0.3pt + luma(120))

#pagebreak()
= Part 4: Discussion
#v(0.2em)
== Discussion Techniques
#text(size: 11pt)[
  Use these phrases to introduce your views and respond to others.
  *Introducing:*
  - "I think that ... because ..."
  - "In my opinion, ..."
  - "It seems to me that ..."
  - "One piece of evidence that supports this is ..."
  *Acknowledging:*
  - "That's an interesting point. I'd add that ..."
  - "I see what you mean. However, ..."
  - "I hadn't thought of it that way. I think ..."
  - "You make a good point about ... but have you considered ...?"
]
#v(0.3em)
== Think-Pair-Share
1. To what extent do you agree Gen Z holds the strongest traditional beliefs? Use at least two pieces of evidence from the video.
#text(size: 11pt)[*Structure:* State position — Evidence 1 — Evidence 2 — Conclude]
#line(length: 100%, stroke: 0.3pt + luma(120))
#line(length: 100%, stroke: 0.3pt + luma(120))
#line(length: 100%, stroke: 0.3pt + luma(120))
#line(length: 100%, stroke: 0.3pt + luma(120))
2. How can young people critically evaluate social media content about gender roles?
#line(length: 100%, stroke: 0.3pt + luma(120))
#line(length: 100%, stroke: 0.3pt + luma(120))
#line(length: 100%, stroke: 0.3pt + luma(120))
#line(length: 100%, stroke: 0.3pt + luma(120))

#pagebreak()
= Transcript
#set text(size: 9pt)
#set par(leading: 0.35em)
https://www.youtube.com/watch?v=qkX5CPXzjxs
#v(0.1em)
LEAVE IT TO BEAVER, 1957 OLD MOVIE: Starring Barbara Billingsley.
JOE BARONIO, BTN REPORTER: If you watch TV shows from the 1950s, you get a fairly black-and-white picture of the roles men and women should play in a family.
1950s TV SHOW: Well, whenever we cook inside, Mom always seems to cook it, but whenever we cook outside, you always do it. How come? Well, sort of traditional, I guess. You know, they say a woman's place is in the home, and I suppose as long as she's in the home, she might as well be in the kitchen.
This is what some people call "traditional" gender roles, with a woman as the homemaker and the man as the breadwinner. But it's something that society has long since left behind, right?
PERSON: I feel like we've got much more diversity now in like, in Gen Z. I just think it wouldn't really work in our society anymore yeah.
It found that of all generations from Baby Boomers to Gen Z, it's Gen Z that holds the strongest traditional beliefs when it comes to gender roles, with 31 per cent men and 18 per cent of women believing that a wife should always obey her husband. And 33 per cent of men and 19 per cent of women saying a husband should have the final word on important decisions in the home.
These attitudes towards women extend beyond just home life. The study also asked about things like equality in society. 61 per cent of Gen Z men and 51 per cent of Gen Z women say they feel enough has already been done for gender equality, with 57 per cent of men and 38 per cent of women saying they feel men are now discriminated against.
JOSH GLOVER, MAN CAVE: It's not surprising. It's sad, but it's not surprising.
This is Josh. He's a facilitator at Man Cave, which is an organisation tackling issues like gender stereotypes in schools. He says social media, particularly things like manosphere content which we've seen in the spotlight a bit recently...
JOSH GLOVER: The whole narrative of echo chambers and what algorithms do and send us into this little shoot where we're just hearing all these people who agree with each other.
JOSH GLOVER: But there's no one there to sort of present another opinion or the only alternative opinions you see are the ones where, you know, the person you agree with then like debunks or smashes or slams them in a debate or whatever it is.
JOSH GLOVER: I just fundamentally think that a teenage boy's definition of feminism is very different to the intended definition of feminism like that's, that's just so clear.
There are a lot of popular influencers who identify as "Tradwives", or traditional wives, and create content that's all about glamorising traditional domestic lifestyles.
JOSH GLOVER: The whole thing, the whole narrative of 'oh this is what women want I guess', women want to be in this 'tradwife' role which feminism is about choice and one of those choices is a traditional role and great. I wonder how much... these 'tradwife' influencers, they don't actually care about what the best expression of being a woman is. They care about making money.
The effects that gendered content have on young people can be extreme. A recent study from the University of Melbourne surveyed more than 2,300 adults and 1,100 young people aged 13 to 17, and found that support for the use of violence to resist feminism was highest among adolescent boys, followed closely by adolescent girls, and that around 40 per cent of boys aged 13 to 17 agreed that women lie about domestic and sexual violence, partly from social media exposure.
Josh says it's a problem that needs to be recognised and addressed by all levels of society.
JOSH GLOVER: I think, you know, two parts of solving a problem. First one is awareness, and then second part is the actual problem-solving bit together. You know we talk a lot at the Man Cave about the importance of village. We just need to be able to have conversations, be, and, and safe conversations. And a safe conversation is with someone where I can trust that I can talk this idea out and not experience being judged or not experienced being shamed.
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
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    CLASS_GROUPS_DIR.mkdir(parents=True, exist_ok=True)
    indir = Path(r"C:\PROJECTS\LESSON-PLAN-WRITER-3\tmp\gender-individual")
    indir.mkdir(exist_ok=True)

    by_class = {}
    for sid, name, cls in STUDENTS:
        by_class.setdefault(cls, []).append((sid, name))

    generated = []

    for sid, name, cls in STUDENTS:
        safe = name.replace(" ", "_").replace("(", "").replace(")", "")
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
        out = CLASS_GROUPS_DIR / f"{cls.replace('-', '_')}-gender-roles-booklet.pdf"
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
        mega_path = CLASS_GROUPS_DIR / "ALL-M3-gender-roles-booklet.pdf"
        mega.save(str(mega_path))
        mega.close()
        print(f"\nALL: {mega_path}")


if __name__ == "__main__":
    main()
    # Post-generation validation
    import subprocess as _sp

    result = _sp.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "validate_booklet.py"),
            "--dir",
            str(CLASS_GROUPS_DIR),
            "--strict",
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)
