# errors-fix.md — Slide Code Issues (index2.html V1)

## Critical

### 1. `fragment.strike` CSS breaks reveal.js built-in behavior (line 76-79)
**Severity: HIGH**

```css
/* CURRENT (WRONG) */
.reveal .fragment.strike {
    text-decoration: line-through;
    opacity: 0.6;
}
```

This custom CSS overrides the reveal.js built-in (confirmed in `knowledge-base\revealjs-packed.json`):
```css
.reveal .fragment.strike { opacity: 1; visibility: inherit; }           /* text always visible */
.reveal .fragment.strike.visible { text-decoration: line-through; }     /* strikethrough on CLICK */
```

**Effect:** Text with `class="fragment strike"` is ALWAYS struck through at 60% opacity, regardless of click state. The progressive reveal is broken.

**Affected slides:** Step 4 MC Strategy (lines 458-459) — options a and b are permanently struck through instead of appearing on click.

**Fix:** Remove lines 76-79. The built-in CSS already provides correct behavior.

---

### 2. `highlight-red` and `highlight-green` CSS override built-in fragment behavior (lines 61-75)
**Severity: LOW** (no usage conflict, but mask built-in effects)

```css
/* CURRENT */
.reveal .fragment.highlight-red { background: rgba(100,0,0,0.4); padding: 0.3em 0.5em; border-radius: 4px; }
.reveal .highlight-green { background: rgba(0,100,0,0.4); padding: 0.3em 0.5em; border-radius: 4px; }
.reveal .highlight-red { background: rgba(100,0,0,0.4); padding: 0.3em 0.5em; border-radius: 4px; }
```

reveal.js built-in (packed JSON):
```css
.reveal .fragment.highlight-red { opacity: 1; visibility: inherit; }
.reveal .fragment.highlight-red.visible { color: #ff2c2d; }
```

**Effect:** Fragment highlight-red adds a red-tinted background padding box rather than the reveal.js-native text-color change. The `.highlight-red`/`.highlight-green` without `.fragment` prefix are dead CSS (never used in any slide).

**Fix:** Remove lines 61-75 if native behavior is desired, or keep if background + padding is the intended design.

---

### 3. Stray empty comment block (lines 541-543)
**Severity: LOW**

```html
<!-- Exercise 5 Answer -->

```

A deleted section left behind a comment and blank lines.

**Fix:** Remove lines 541-543.

---

### 4. Lightbulb icon on Exercise 2 answers (line 259)
**Severity: LOW** (inconsistency)

```html
<i class="fa-solid fa-lightbulb slide-icon" style="color: rgba(255,255,255,0.9);"></i>
```

All other answer slides (Ex3, Ex4) have lightbulbs removed to save screen space. This one remains.

**Fix:** Remove line 259 for consistency.

---

### 5. Slide comment numbering is stale (multiple lines)
**Severity: LOW** (documentation)

Comments like `<!-- SLIDES 9-13: True/False Strategy -->` and `<!-- SLIDE 28: Summary -->` don't match the actual slide count or indices. These were copied from the template and never updated when slides were added/removed.

**Fix:** Update comment labels to match actual slide positions, or remove them entirely (script tooling ignores comments).

---

### 6. Ex3 Timer note says "3 min" but slideshow uses 180s (lines 338-341)
**Severity: LOW** (metadata only)

The `<aside class="notes">` for the Ex3 timer says "Stage 3 · 3 min" but the `data-timer="180"` (180 seconds = 3 min). Technically correct but the notes could be more descriptive.

---

## Structural Observations (not errors)

| Aspect | Status |
|---|---|
| One step per slide rule | ✓ Followed across all pedagogy blocks |
| Auto-animate underline (MC Step 2) | ✓ Correct: data-auto-animate on both slides, transparent→white border, matching data-id |
| Icon placement (first slide only) | ✓ Fa-icons only on block headers |
| Icon spacing (no float:left) | ✓ Fixed on T/F and Para Matching headers |
| Table answers with Why column | ✓ Ex2, Ex3, Ex4, MC Step 5 all have explanations |
| `wrap` class for long-text tables | ✓ Applied to Step 5 and Ex4 Answer |
| Fragment indices for simultaneous reveal | ✓ Matching `data-fragment-index` on paired cells |
| Text shadow for readability | ✓ Applied globally via CSS |
| Pedagogical vertical alignment | ✓ `align-self: flex-start; padding-top: 30px` |
| Slide deletion cleanup | ⚠ Row 36/37/39 deleted but residual comment lingers |
