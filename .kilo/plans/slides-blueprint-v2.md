# Design Blueprint — Who Do We Care About Most? (v2)

## Lead-in Image
- File: `assets/anxiety.webp` (2176×1450) — teen with therapist
- Used as full-bleed background on lead-in slides (same image across both)

## PET Prompt (exact Cambridge format)
```
ARTICLES WANTED — CLOSE FRIENDSHIPS

Write an article for your school magazine about how close friendships
can help teenagers.

Why is it important to have close friends? How can friends support
you when you feel stressed? What have you learned from your closest
friendship?

The best articles will be published next month.
```

## Stage-to-Slide Mapping

| Stage | Name | Slide Type(s) | IDs |
|-------|------|---------------|-----|
| — | Splash | image-only (anxiety.webp) | slide-splash |
| — | Title | logo + h2 + badge + strap + CTA | slide-title |
| — | Objective | 3 "I can" statements | slide-objective |
| 1 | Lead-in Q1 | anxiety.webp bg: "What's happening here?" | slide-lead-in-1 |
| 1 | Lead-in Q2 | anxiety.webp bg: "Top 5 teen issues?" | slide-lead-in-2 |
| 1→2 | Transition | Let's Review (red) | slide-transition-review |
| 2 | Review items 1-4 | sentence-swap × 4 | slide-review-1-4 |
| 2 | Review items 5-7 | sentence-swap × 3 | slide-review-5-7 |
| 2→3 | Transition | Let's Write (red) | slide-transition-write |
| 3 | PET Prompt | exact Cambridge format | slide-prompt |
| 3 | Article Structure | hook → reasons → conclusion | slide-structure |
| 3 | Linking 1: Opinions + Adding | 2 categories + examples | slide-linking-1 |
| 3 | Linking 2: Contrast + Conclude | 2 categories + examples | slide-linking-2 |
| 3 | Demo: sentence combine (entry) | auto-animate entry | slide-demo-entry |
| 3 | Demo: sentence combine (reveal) | auto-animate reveal | slide-demo-reveal |
| 3 | Writing Task | prompt + checklist + timer 1260s | slide-writing-task |
| — | Summary | 3 checkmarks | slide-summary |
| — | End | topic + badge | slide-end |

**Total: 19 slides**

## Lead-in Slides
Both slides share same `data-background-image="assets/anxiety.webp"`. 
Q1: "What do you think is happening in this picture?" — evokes "therapist," counseling, emotional support.
Q2: "What are the top 5 issues affecting teenagers today?" — leads into why close friendships matter for mental health.

## Lead-in Image Layout
Image anchors to center. Text on right side (like M2 Nureyev slides): `margin-left: 55%` with text-shield.

## PET Prompt Display
Shown as a clean announcement with:
- "ARTICLES WANTED — CLOSE FRIENDSHIPS" header in yellow
- Instruction line in white
- 3 questions as bullet points
- Closing incentive line
- Border box to distinguish as exam-style prompt (like M2 writing task slide)

## Writing Task Slide
Side-by-side layout (like M2 slide 16):
- **Left**: PET prompt in bordered box (same as slide-prompt but smaller)
- **Right**: Requirements checklist (6 items: hook, 2-3 reasons, linking phrases, compound sentence, ~100 words, check for run-ons/comma splices)
- Timer: data-timer="1260" (21 min)
