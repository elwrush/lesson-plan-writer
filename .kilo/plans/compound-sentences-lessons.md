# Plan: M2-4A Compound Sentences — Two-Lesson Sequence

**Date:** 31 May 2026  
**Status:** PLAN — awaiting execution  
**Author:** Kilo (planning agent)

---

## 1. Overview

Two consecutive grammar lessons for M2-4A (B1 EFL, Thai learners). Both lessons source from *First Steps in Academic Writing*, Chapter 2, pages 54–61. The MD source file is:

```
C:\PROJECTS\LESSON-PLAN-WRITER-3\inputs\M2-WRITING-COMPOUND-SENTENCES\First_Steps_in_Academic_Writing.md
```

| | Lesson 1 | Lesson 2 |
|---|---|---|
| **Topic** | Writing compound sentences (coordinators: and, but, or, so) | Fixing run-ons and comma splices |
| **Pages** | 54–59 | 59–61 |
| **Exercises** | Practice 7, 8A, 8B, 9, 10A | Practice 10B (warm-up), 11 |
| **Shape** | C (Test-Teach-Test) | C (Test-Teach-Test) |
| **Pixabay theme** | Bolts holding things together | Shattered glass |
| **Output subfolder** | `M2-WRITING-COMPOUND-SENTENCES` | `M2-WRITING-COMPOUND-SENTENCES-L2` |
| **PDF feedback** | `C:\PROJECTS\ERRANT-ANALYSIS\PDF\M2-4A Assignment 2\31-05-26-M2-4A-combined.pdf` | N/A |

**Rationale for TTT on Lesson 2:** Students have written paragraphs before (Assignment 1 + upcoming CA prep) and likely produce run-ons without knowing the term. A diagnostic test of error-correction sentences at the start of Lesson 2 reveals what they already know. The TTT arc (diagnose → clarify → practice) fits error-remediation skills perfectly.

---

## 2. File Paths & Output Structure

```
inputs/
  M2-WRITING-COMPOUND-SENTENCES/
    First_Steps_in_Academic_Writing.md          ← SOURCE (exists)
    answer_key.typ                              ← TO CREATE

output/
  M2-WRITING-COMPOUND-SENTENCES/
    310526-compound-sentences-lesson-plan.json   ← Lesson 1 JSON
    slides/
      index.html                                ← Lesson 1 slideshow
      timer-plugin.js, timer-plugin.css
      assets/
        logo.png
        bolts.jpg                               ← Lesson 1 Pixabay
  M2-WRITING-COMPOUND-SENTENCES-L2/
    310526-run-ons-and-comma-splices-lesson-plan.json  ← Lesson 2 JSON
    slides/
      index.html                                ← Lesson 2 slideshow
      timer-plugin.js, timer-plugin.css
      assets/
        logo.png
        shattered-glass.jpg                     ← Lesson 2 Pixabay
```

---

## 3. Pre-Flight: Grammar Accuracy Feedback (PDF 1)

**PDF path:**
```
C:\PROJECTS\ERRANT-ANALYSIS\PDF\M2-4A Assignment 2\31-05-26-M2-4A-combined.pdf
```

**Action in write-lesson-plan workflow:**
1. Extract text via `pypdf`:
```
python -c "import pypdf; reader = pypdf.PdfReader(r'C:\PROJECTS\ERRANT-ANALYSIS\PDF\M2-4A Assignment 2\31-05-26-M2-4A-combined.pdf'); [print(f'=== PAGE {i+1} ===\n{p.extract_text()}\n') for i,p in enumerate(reader.pages)]"
```
2. The extracted feedback populates the Lesson 1 Lead-in stage (students review their own errors)
3. This content does NOT go into the answer key — it's teacher material

---

## 4. Lesson 1: Writing Compound Sentences (pp. 54–59)

**JSON fields:**

| Field | Value |
|-------|-------|
| `teacher` | Ed Rush |
| `duration` | 46 minutes |
| `date` | 310526 |
| `topic` | Compound Sentences |
| `shape` | C |
| `shape_name` | Test-Teach-Test |
| `cefr_level` | B1 |
| `class` | M2-4A |
| `materials` | "- Coursebook: First Steps in Academic Writing, pp 54-59\n- Grammar accuracy feedback: 31-05-26-M2-4A-combined.pdf" |
| `answer_key` | `C:\\PROJECTS\\LESSON-PLAN-WRITER-3\\inputs\\M2-WRITING-COMPOUND-SENTENCES\\answer_key.typ` |
| `transcript` | none |
| `objective` | By the end of the lesson, learners will be better able to use coordinating conjunctions (and, but, or, so) to write compound sentences in the context of describing a friend. |

### 4.1 Lesson Plan Stages

| # | Stage | Aim | Procedure | Time | Int. |
|---|-------|-----|-----------|------|------|
| 1 | Lead-in — Grammar Feedback Review | To activate learners' awareness of their own writing accuracy and build motivation for the grammar focus | - Distribute grammar accuracy feedback from PDF 1. Ss review individual errors silently (3 min). Praise improvements: "Class accuracy went up." Then: "Your first CA is coming — a paragraph introducing a friend and their interests. But first, we need to learn how to write compound sentences properly." Write goal on board. | 5 | T-Ss |
| 2 | Test 1 — Diagnostic (Compound Sentences) | To diagnose baseline ability to recognize and form compound sentences | - Display 6 pairs of simple sentences on screen. Ss join each pair into one compound sentence using and/but/or/so. No instruction given — discovery task. Individual work (5 min). Pair check (2 min). Teacher circulates, notes errors. | 7 | S, Ss-Ss |
| 3 | Teach — Coordinators: and, but, or, so | To clarify the meaning and function of the four coordinating conjunctions in compound sentences | - Display Practice 7 formula table: SV V vs SV, and SV. Elicit: "What makes a sentence compound?" (two subjects, two verb groups, comma + coordinator). Walk through each coordinator's meaning using textbook examples (pp. 56-57). Highlight comma rule: comma BEFORE coordinator. | 10 | T-Ss |
| 4 | Test 2 — Controlled Practice: Practice 8A+B | To give structured practice distinguishing simple from compound sentences | - Ss complete Practice 8A (items 1-10) + 8B (Teenagers, items 1-9). Underline S/V, circle coordinator, write formula, add commas. Individual (8 min). Pair check (4 min). Display answers, address tricky items (9: compound subject; 10: imperative). | 12 | S, Ss-Ss, T-Ss |
| 5 | Test 3 — Freer Practice: Practice 9 + 10A | To give extended practice choosing coordinators and writing own compound sentences | - Practice 9 (13 coordinator blanks): rapid oral check with screen answers (2 min). Practice 10A (9 sentence pairs to join): individual writing focused on comma + coordinator choice (6 min). Pair compare + display model answers (3 min). | 11 | S, Ss-Ss, T-Ss |
| 6 | Wrap-up | To consolidate key learning and connect to CA writing task | - Quick review: "How do you make a compound sentence?" (SV, coordinator SV). "What does 'but' signal?" (contrast). "Where does the comma go?" (before coordinator). Connect to CA: "In your paragraph about your friend, use compound sentences." Preview: "Next time — fixing broken sentences." | 4 | T-Ss |

**Total:** 5+7+10+12+11+4 = 49 minutes. Trim: reduce Practice 10A from 6→4 min (fast finishers pair-check during task). New total: 5+7+10+12+9+4 = 47. Reduce lead-in from 5→4 min. Final: **46 min** ✓

### 4.2 Exercises Covered

| Exercise | Page | Items | Answer key needed? |
|----------|------|-------|-------------------|
| Practice 7 | 54 | Reference table (6 rows) | No (teaching tool) |
| Practice 8A | 54–55 | Items 1–10 | Yes |
| Practice 8B | 55–56 | Items 1–9 (Teenagers) | Yes |
| Practice 9 | 57 | Items 1–13 | Yes |
| Practice 10A | 57–58 | Items 1–9 | Yes (model answers) |

---

## 5. Lesson 2: Fixing Run-ons and Comma Splices (pp. 59–61)

**JSON fields:**

| Field | Value |
|-------|-------|
| `teacher` | Ed Rush |
| `duration` | 46 minutes |
| `date` | 310526 |
| `topic` | Run-ons and Comma Splices |
| `shape` | C |
| `shape_name` | Test-Teach-Test |
| `cefr_level` | B1 |
| `class` | M2-4A |
| `materials` | "- Coursebook: First Steps in Academic Writing, pp 59-61" |
| `answer_key` | `C:\\PROJECTS\\LESSON-PLAN-WRITER-3\\inputs\\M2-WRITING-COMPOUND-SENTENCES\\answer_key.typ` |
| `transcript` | none |
| `objective` | By the end of the lesson, learners will be better able to identify and correct run-on sentences and comma splices in the context of writing about a friend. |

### 5.1 Lesson Plan Stages

| # | Stage | Aim | Procedure | Time | Int. |
|---|-------|-----|-----------|------|------|
| 1 | Lead-in — Review + Practice 10B | To retrieve compound sentence knowledge from Lesson 1 and bridge into error correction | - Quick review: elicit compound sentence formula and four coordinators (2 min). Ss complete Practice 10B (7 sentence completions, p. 59) as warm-up. Individual writing (4 min). Pair share — compare answers (2 min). | 8 | T-Ss, S, Ss-Ss |
| 2 | Test 1 — Diagnostic (Error Correction) | To diagnose baseline ability to spot and fix run-on and comma splice errors | - Display 5 sentences: 2 run-ons, 2 comma splices, 1 correct. Ss mark each "OK" or "fix it" and write correction. Individual (3 min). Pair check (2 min). | 5 | S, Ss-Ss |
| 3 | Teach — Two Sentence Errors + Two Fixes | To explicitly teach definitions of run-ons and comma splices, and present two correction methods | - Re-display diagnostic sentences. Elicit: "What's wrong?" Name errors: comma splice (comma only, no coordinator) and run-on (nothing between sentences). Show textbook definitions (pp. 59-60). Present two fixes: (1) Period + capital, (2) Comma + coordinator. Walk through each diagnostic item with both methods. | 10 | T-Ss |
| 4 | Test 2 — Controlled Practice: Practice 11 | To give structured practice identifying and fixing run-ons and comma splices | - Ss complete Practice 11 (items 1-10). Step 1: mark errors with X. Step 2: correct using Method 1 or 2. Individual (8 min). Pair check — discuss different correction choices (4 min). Whole-class feedback, address tricky items: 4 (trailing "however"), 10 ("then" run-on). | 14 | S, Ss-Ss, T-Ss |
| 5 | Application — Write 3 Perfect Compound Sentences | To transfer combined skills to the CA writing context | - "Now you know how to build AND fix compound sentences." Ss write 3 original compound sentences about a friend/classmate, each with a different coordinator. Must be run-on-free. Individual (5 min). Pair swap — partner checks for errors (3 min). | 8 | S, Ss-Ss |
| 6 | Wrap-up | To consolidate error-correction strategies and preview CA | - "Name the two errors." (run-ons, comma splices). "Name the two fixes." (period, or comma+coordinator). "Before you write your CA paragraph, what will you check for?" Preview: "Next lesson — writing the CA paragraph about your friend." | 3 | T-Ss |

**Total:** 8+5+10+14+8+3 = 48 minutes. Trim Practice 11 individual from 8→7 min, pair check from 4→3 min. Final: **46 min** ✓

### 5.2 Exercises Covered

| Exercise | Page | Items | Answer key needed? |
|----------|------|-------|-------------------|
| Practice 10B | 59 | Items 1–7 | No (open-ended) |
| Practice 11 | 61 | Items 1–10 | Yes |

---

## 6. Answer Key — Typst (.typ)

**File path:** `C:\PROJECTS\LESSON-PLAN-WRITER-3\inputs\M2-WRITING-COMPOUND-SENTENCES\answer_key.typ`

The answer key covers only exercises with discrete, verifiable answers. Practice 10B is open-ended — excluded from the answer key but included in the lesson plan stages.

### 6.1 Typst Source (the code to write)

```typst
= Answer Key — Compound Sentences (Practice 7–11)
= *First Steps in Academic Writing*, Chapter 2, pp. 54–61

== PRACTICE 8A — Identify Simple and Compound Sentences (items 1–10)

#table(
  columns: 3,
  table.header[*\#*][*Simple or Compound?*][*Formula*],
  [1], [simple], [SV],
  [2], [compound], [SV, so SSV],
  [3], [simple], [SVV],
  [4], [compound], [SV, or SVV],
  [5], [simple], [SV],
  [6], [compound], [SV, and SV],
  [7], [compound], [SV, but SV],
  [8], [compound], [SV, but SV],
  [9], [simple], [SSV],
  [10], [simple], [(S) V V],
)

*Notes:*

- Item 4: "We played games such as hide-and-seek and tag, or we just sat on the grass and told stories." — compound; second clause has compound verb SVV. Comma added before "or."
- Item 6: "We put the fireflies into a glass jar, and our father punched air holes in the metal lid." — compound; comma added before "and."
- Item 7: "My sisters were afraid of most bugs, but they loved fireflies." — compound; comma added before "but."
- Item 8: "We usually went to bed at nine o'clock, but we stayed up until ten on really warm evenings." — compound; comma added before "but."
- Item 9: Simple with compound subject. One subject "our mother and father" (SS), one verb "told" (V). Formula: SSV.
- Item 10: Imperative. Implied subject "(you)" with compound verb "come" and "leave." Simple: (S) V V. No comma.

== PRACTICE 8B — Identify Simple and Compound Sentences (Teenagers, items 1–9)

#table(
  columns: 3,
  table.header[*\#*][*Simple or Compound?*][*Formula*],
  [1], [simple], [SV],
  [2], [compound], [SV, or SV],
  [3], [simple], [SVV],
  [4], [simple], [SV],
  [5], [compound], [SV, but SV],
  [6], [compound], [SV, but SV],
  [7], [simple], [SV],
  [8], [compound], [SV, so SV],
  [9], [compound], [SV, but SV],
)

*Notes:*

- Seven commas should be added: before "or" (sent. 2); before "but" (sent. 5, 6, 9); before "so" (sent. 8); and two more commas: sent. 4 begins with "In addition" — add comma after it. Sent. 6: the coordinator "but" needs a comma before it. The remaining comma budget = 1 remaining. Total of 7 added commas in the full paragraph.
- Sentence 7: one subject "they," one verb "are," compound predicate adjective joined by "but" ("old enough to drive but too young to pay for gas"). Simple, SV.
- Sentence 4: single verb "spend" with compound object of the preposition ("at the shopping mall and on the phone"). Simple, SV.

== PRACTICE 9 — And, But, Or, and So (items 1–13)

#table(
  columns: 3,
  table.header[*\#*][*Item context*][*Coordinator*],
  [1], [fried chicken `and` meatloaf], [and],
  [2], [I ordered meatloaf, `and` my friend ordered fried chicken], [and],
  [3], [We don't have chicken `or` meatloaf], [or],
  [4], [I wanted to leave ..., `but` my friend wanted to stay], [but],
  [5], [a hamburger `and` french fries, `but` I didn't order anything], [and / but],
  [6], [My new neighbors are vegetarians, `so` they don't eat meat], [so],
  [7], [They don't eat meat `or` chicken, `but` sometimes...fish], [or / but],
  [8], [I wanted to be friendly, `so` I invited them to my house], [so],
  [9], [They came `and` brought their young son], [and],
  [10], [He is just a baby, `so` he can't talk yet], [so],
  [11], [They don't drink coffee `or` tea, `so` I served lemonade], [or / so],
  [12], [a choice of chocolate cake `or` apple pie], [or],
  [13], [The husband wanted both, `but` the wife didn't want either], [but],
)

*Notes:*

- Item 5: first blank joins nouns ("hamburger and french fries"), second blank joins clauses ("but I didn't order"). The "and" is within a simple sentence.
- Item 7: negative simple sentence uses "or" (not "and") to join nouns; "but" joins clauses.
- Item 9: simple sentence with compound verb — "came and brought." No comma. "And" joins two verbs sharing one subject.
- Item 11: same pattern as item 7 — "or" in negative noun list; "so" for reason→result between clauses.

== PRACTICE 10A — Writing Compound Sentences (model answers; items 2–9)

Accept any reasonable compound sentence with appropriate coordinator. Model answers:

#table(
  columns: 2,
  table.header[*\#*][*Model Answer*],
  [2], [There are several hundred languages in the world, but not all of them have a written form.],
  [3], [Chinese is spoken by more people, but English is spoken in more countries.],
  [4], [Russian is the third most spoken language in the world, and Spanish is the fourth.],
  [5], [There are about one million words in English, but most people use only about ten thousand of them.],
  [6], [Chinese has many different dialects, so Chinese people cannot always understand each other.],
  [7], [French used to be the language of international diplomacy, but now it is English.],
  [8], [International companies are growing, so they will soon need more bilingual workers.],
  [9], [Young people should know a second language, or they will be at a disadvantage in the international job market.],
)

*Alternatives accepted for items 2 and 3:* "and" is also acceptable. Item 6: students may recast to resolve the logic issue (a language cannot understand).

== PRACTICE 10B — Completing Compound Sentences (items 1–7)

*Open-ended. Given example:*
My brother and I look like twins, but our personalities are very different.

#pagebreak()

== PRACTICE 11 — Fixing Run-ons and Comma Splices (items 1–10)

#table(
  columns: 3,
  table.header[*\#*][*Error?*][*Correction (Method 1 shown; Method 2 also acceptable)*],
  [1], [X], [Some people like cats. Others prefer dogs.],
  [2], [X], [Kittens are cute. They like to play.],
  [3], [—], [Correct as is.],
  [4], [X], [It's acceptable for dogs to bark at strangers. They shouldn't bite them, however.],
  [5], [—], [Correct as is.],
  [6], [X], [Penguins always wear tuxedos. They are good pets for people who like to go to fancy parties.],
  [7], [X], [A pet elephant can fan you with his ears and spray you with his trunk. You won't need air-conditioning or a shower.],
  [8], [—], [Correct as is.],
  [9], [X], [A giraffe can reach things on high shelves. It can see over the heads of people at parades.],
  [10], [X], [Keep a boa constrictor as a pet if you enjoy being alone. Then no one will ever visit you.],
)

*Error types:*
- Comma splices (comma only, no coordinator): items 1, 2, 6, 7, 9
- Run-ons (nothing between clauses): items 4, 10
- Correct: items 3, 5, 8

*Method 2 alternatives:*
- Item 1: "...cats, and others prefer dogs." / "...cats, but others prefer dogs."
- Item 2: "Kittens are cute, and they like to play."
- Item 4: "...strangers, but they shouldn't bite them."
- Item 6: "...tuxedos, so they are good pets..."
- Item 7: "...trunk, so you won't need..."
- Item 9: "...shelves, and it can see..."
- Item 10: "...alone, and then no one will ever visit you."

*Item 4 note:* The run-on is at "strangers they." "however" is a conjunctive adverb at the end — it does not fix the run-on.
*Item 10 note:* "alone then" — run-on. "then" is not a coordinator.
```

### 6.2 Typst Pitfalls — Pre-Write Checklist

Before writing the `.typ` file, verify:
- [x] `[*\#*]` in all table headers (not `[*#*]`) — Pitfall 2
- [x] No markdown pipe tables — using `#table()` throughout — Pitfall 5
- [x] Unicode characters pasted directly (em dash, apostrophes) — Pitfall 6
- [x] No `*M*y` mid-word bold patterns — Pitfall 1 not triggered
- [x] `#pagebreak()` for content separation
- [x] All `#table()` calls have explicit `columns:` parameter

---

## 7. Pixabay Image Strategy

### Lesson 1 — "Bolts"
```bash
python scripts/pixabay_download.py --query "bolts and nuts metal" --type image --count 3
# Best result → output/M2-WRITING-COMPOUND-SENTENCES/slides/assets/bolts.jpg
```
Title slide uses `r-stack` pattern with logo centered at top, title + B1 badge, then bolts image filling remaining space.

### Lesson 2 — "Shattered glass"
```bash
python scripts/pixabay_download.py --query "shattered glass crack" --type image --count 3
# Best result → output/M2-WRITING-COMPOUND-SENTENCES-L2/slides/assets/shattered-glass.jpg
```
Same `r-stack` title slide pattern.

---

## 8. Slideshow Build Plan

### 8.1 Lesson 1 Slide Sequence (~29 slides)

| # | Type | ID | Content |
|---|------|----|---------|
| 0 | Title | `slide-title` | Title + B1 badge + "and, but, or, so" strap + bolts image |
| 1 | Objective | `slide-objective` | 3 "I can..." statements |
| 2 | Transition | `slide-transition-review` | Red bg: "Grammar Feedback Review" |
| 3 | Lead-in | `slide-lead-in` | Dark bg: Praise + CA goal. Error examples from PDF 1 (auto-animate: original→corrected) |
| 4 | Transition | `slide-transition-diagnostic` | Red bg: "What do you know?" |
| 5 | Diagnostic | `slide-diagnostic` | Dark bg: 6 sentence pairs to join (bespoke). Individual work + timer |
| 6 | Transition | `slide-transition-teach` | Red bg: "How to build a compound sentence" |
| 7 | Pedagogical | `slide-teach-formula` | Teal bg: Practice 7 table — SV V vs SV, and SV. Auto-animate: highlight subjects/verbs |
| 8 | Pedagogical | `slide-teach-and` | Teal bg: AND = similar ideas. Example + formula |
| 9 | Pedagogical | `slide-teach-but` | Teal bg: BUT = contrast. Example + formula |
| 10 | Pedagogical | `slide-teach-or-so` | Teal bg: OR = choice, SO = reason→result. Two examples |
| 11 | Pedagogical | `slide-teach-comma` | Teal bg: Comma rule reference — always BEFORE coordinator |
| 12 | Transition | `slide-transition-practice8` | Red bg: "Simple or Compound?" |
| 13 | Pedagogical | `slide-ped-p8` | Teal bg: Steps 1–4 strategy for Practice 8 |
| 14 | Task | `slide-p8a-task` | Dark bg: "Practice 8A — items 1–10" + timer (480s) |
| 15 | Answers | `slide-p8a-answers-1-5` | Green bg: answer-list (5 items) |
| 16 | Answers | `slide-p8a-answers-6-10` | Green bg: answer-list (5 items) |
| 17 | Task | `slide-p8b-task` | Dark bg: "Practice 8B — Teenagers" + timer (420s) |
| 18 | Answers | `slide-p8b-answers-1-5` | Green bg: answer-list (5 items) |
| 19 | Answers | `slide-p8b-answers-6-9` | Green bg: answer-list (4 items — acceptable) |
| 20 | Transition | `slide-transition-practice9` | Red bg: "Choose the right coordinator" |
| 21 | Task | `slide-p9-task` | Dark bg: "Practice 9 — And, But, Or, or So?" + timer (180s) |
| 22 | Answers | `slide-p9-answers-1-7` | Green bg: answer-list (7 items — split: 1–4 + 5–7?) ... actually 7 items on one slide is too many. **Split:** |
| 23 | Answers (2) | `slide-p9-answers-1-7` | Green bg: answer-list (7 items) ... **RECONSIDER**: max 3 per slide per skill doc rules. 13 items = 5 slides minimum. That's excessive for a rapid oral check. **Alternative:** Use a reference slide format (static table, no fragment reveals) since this is a quick oral check, not a graded exercise. Single static table on teal or green background. |
| 24 | Transition | `slide-transition-practice10` | Red bg: "Write your own" |
| 25 | Task | `slide-p10a-task` | Dark bg: "Practice 10A — Join the sentences" + timer (360s) |
| 26 | Answers | `slide-p10a-answers-1-5` | Green bg: answer-list (5 items) |
| 27 | Answers | `slide-p10a-answers-6-9` | Green bg: answer-list (4 items) |
| 28 | Transition | `slide-transition-summary` | Red bg: "Let's Review" |
| 29 | Summary | `slide-summary` | Dark bg: 3 "I can..." checkmarks |
| 30 | End | `slide-end` | Dark blue-gray: "Writing Compound Sentences — B1" |

**Total: ~31 slides.** The agent may consolidate during build (e.g., combine and/but/or/so into 2 pedagogical slides instead of 3 if space permits).

### 8.2 Lesson 2 Slide Sequence (~19 slides)

| # | Type | ID | Content |
|---|------|----|---------|
| 0 | Title | `slide-title` | Title + B1 badge + "run-ons & comma splices" strap + shattered glass |
| 1 | Objective | `slide-objective` | 3 "I can..." statements |
| 2 | Transition | `slide-transition-review` | Red bg: "What's a compound sentence?" |
| 3 | Lead-in | `slide-lead-in` | Dark bg: Quick review + Practice 10B task + timer |
| 4 | Transition | `slide-transition-diagnostic` | Red bg: "Find the mistakes" |
| 5 | Diagnostic | `slide-diagnostic` | Dark bg: 5 sentences (2 run-ons, 2 comma splices, 1 correct) |
| 6 | Transition | `slide-transition-teach` | Red bg: "Two sentence errors" |
| 7 | Pedagogical | `slide-teach-errors` | Teal bg: Define run-on vs comma splice. Auto-animate: WRONG → RIGHT on same sentence |
| 8 | Pedagogical | `slide-teach-fixes` | Teal bg: Two correction methods. Auto-animate: show both fixes |
| 9 | Transition | `slide-transition-practice11` | Red bg: "Fix the errors" |
| 10 | Pedagogical | `slide-ped-p11` | Teal bg: Practice 11 strategy — 2-step process |
| 11 | Task | `slide-p11-task` | Dark bg: "Practice 11 — items 1–10" + timer (480s) |
| 12 | Answers | `slide-p11-answers-1-5` | Green bg: answer-list (5 items with error type + correction) |
| 13 | Answers | `slide-p11-answers-6-10` | Green bg: answer-list (5 items) |
| 14 | Transition | `slide-transition-apply` | Red bg: "Use what you know" |
| 15 | Task | `slide-apply-task` | Dark bg: "Write 3 compound sentences about your friend" + timer (300s) |
| 16 | Transition | `slide-transition-summary` | Red bg: "Let's Review" |
| 17 | Summary | `slide-summary` | Dark bg: 3 "I can..." checkmarks + CA preview |
| 18 | End | `slide-end` | Dark blue-gray: "Fixing Run-ons & Comma Splices — B1" |

**Total: 19 slides.**

---

## 9. Key Pedagogical Intent Annotations

### For Practice 7 formula comparison (auto-animate):
```
PEDAGOGICAL INTENT: Student sees the same sentence transformed from SVV (simple) to SV, and SV (compound). The only difference is an added subject + comma. The transformation IS the learning.
WHY THIS FEATURE: Auto-animate morphs the sentence — a bare "and" becomes "and" with a new subject after it. Fragments can't show morphing.
COGNITIVE PRINCIPLE: Signaling (Mayer) — visual change draws attention to the critical feature: "a second subject = compound."
```

### For run-on → corrected error (auto-animate):
```
PEDAGOGICAL INTENT: Student sees a wrong sentence (comma splice or run-on) transform into a right sentence. The wrong→right transition makes the error VISIBLE.
WHY THIS FEATURE: Auto-animate morphs WRONG to RIGHT — the added period/capital or added coordinator appears while the original text stays in place. Fragments would require hiding first, losing the comparison.
COGNITIVE PRINCIPLE: Temporal Contiguity (Mayer) + Signaling — the correction appears simultaneously with the original structure.
```

---

## 10. Build Workflow Command Sequence

### Lesson 1:
```powershell
# Create directories
mkdir "output/M2-WRITING-COMPOUND-SENTENCES/slides/assets" -Force

# Run write-lesson-plan skill (interactive)
# → output/M2-WRITING-COMPOUND-SENTENCES/310526-compound-sentences-lesson-plan.json

# Write answer key: inputs/M2-WRITING-COMPOUND-SENTENCES/answer_key.typ

# Pixabay images
python scripts/pixabay_download.py --query "bolts and nuts metal" --type image --count 3
# Rename → output/M2-WRITING-COMPOUND-SENTENCES/slides/assets/bolts.jpg

# Copy template + plugins + logo
cp "templates/base-slides-template.html" "output/M2-WRITING-COMPOUND-SENTENCES/slides/index.html"
cp "templates/timer-plugin.js" "output/M2-WRITING-COMPOUND-SENTENCES/slides/"
cp "templates/timer-plugin.css" "output/M2-WRITING-COMPOUND-SENTENCES/slides/"
cp "templates/ACT.png" "output/M2-WRITING-COMPOUND-SENTENCES/slides/assets/logo.png"

# Build slide sections → C:\Users\elwru\AppData\Local\Temp\kilo\slides_sections.html
# Splice into index.html via Python script

# Validate
npx revealjs-validator --project "output/M2-WRITING-COMPOUND-SENTENCES/slides/"

# PDF
python scripts/json_to_pdf.py "output/M2-WRITING-COMPOUND-SENTENCES/310526-compound-sentences-lesson-plan.json"
```

### Lesson 2:
```powershell
mkdir "output/M2-WRITING-COMPOUND-SENTENCES-L2/slides/assets" -Force

# Run write-lesson-plan → output/M2-WRITING-COMPOUND-SENTENCES-L2/310526-run-ons-and-comma-splices-lesson-plan.json

python scripts/pixabay_download.py --query "shattered glass crack" --type image --count 3
# Rename → output/M2-WRITING-COMPOUND-SENTENCES-L2/slides/assets/shattered-glass.jpg

# Copy template, build slides, validate, PDF (same pattern as Lesson 1)
```

---

## 11. Diagnostic Test Items (Bespoke)

### Lesson 1 — Test 1
Six sentence pairs. Students join each into one compound sentence:

1. My friend speaks Thai. She also speaks English. _(and)_
2. I like football. My brother prefers basketball. _(but)_
3. We can go to the cinema. We can stay home and watch a movie. _(or)_
4. It started raining. We went inside. _(so)_
5. The test was difficult. I studied hard for it. _(but)_
6. He doesn't like coffee. He drinks tea every morning. _(so/and)_

### Lesson 2 — Test 1
Five sentences. Students mark "OK" or "Fix it" and correct:

1. My friend is very kind, she always helps me with homework. _(comma splice → FIX)_
2. I go to school by bus it takes about thirty minutes. _(run-on → FIX)_
3. My sister loves reading, and she has over a hundred books. _(correct → OK)_
4. The food was delicious we ate everything on the table. _(run-on → FIX)_
5. I wanted to call him, but I forgot my phone at home. _(correct → OK)_

---

## 12. Open Items

1. **PDF 1 extraction:** The agent executing `write-lesson-plan` must extract text from the feedback PDF using pypdf. The PDF path (`C:\PROJECTS\ERRANT-ANALYSIS\PDF\M2-4A Assignment 2\31-05-26-M2-4A-combined.pdf`) is outside the standard `inputs/` folder — the agent needs to be told explicitly where it is.

2. **Practice 9 answer reveal method:** With 13 items and a max-3-per-slide rule, a full fragment-based answer reveal would need 5 slides. Since this is a rapid oral check (not a graded exercise), the agent should consider a static reference table format instead.

3. **Lesson 1 answer-list sizing:** Practice 8A (10 items), 8B (9 items), 10A (9 items) all exceed the max-3 rule. Each must be split across 3-5 answer slides. The plan above accounts for this split.

---

**Plan complete.** Ready for the `write-lesson-plan` skill to execute each lesson, followed by `lesson-plan-to-reveal` for both slideshows.
