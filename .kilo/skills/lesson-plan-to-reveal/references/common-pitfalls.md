# Common Pitfalls — lesson-plan-to-reveal

## Plugin safety protocol

Adding a plugin to the base template's `plugins` array can cause a silent blank page if the plugin's `init()` fails. Protocol:
1. **Add to the `plugins` array LAST** — build and test WITHOUT the new plugin first
2. **Add one plugin at a time** — never add multiple untested plugins simultaneously
3. **Test in browser** — open slides, `F12` → Console tab. Verify: page shows content, zero red errors, navigation works
4. **Isolate on failure** — if page is blank, remove ALL recently added plugins, re-add one at a time

## Temp file workflow (proven pattern)

The ONLY reliable approach given Windows tooling constraints:
1. **Write slide sections** to `C:\Users\elwru\AppData\Local\Temp\kilo\slides_sections.html` via the Write tool
2. **Copy template** to output dir via PowerShell `cp`
3. **Write splice script** to `C:\Users\elwru\AppData\Local\Temp\kilo\splice_slides.py`
4. **Run splice script** via `python ...\splice_slides.py`
5. **Write verification script** to `C:\Users\elwru\AppData\Local\Temp\kilo\verify_slides.py`
6. **Clean up** temp files only after verification passes

**Do NOT:** Write large files (>300 lines) directly via Write tool to `output/` — may hit permission blocks. Use PowerShell `>`, `Out-File`, or `Set-Content` for files with Unicode — they add BOM or corrupt codepoints.

## Answer-list CSS alignment traps

The answer-list flex layout has three CSS properties that, if set incorrectly, break left-alignment. All three must be set correctly in the inline `<style>` block (Step 2b):

| Element | Correct value | Wrong value | What breaks |
|---------|--------------|-------------|-------------|
| `.a-num` | `text-align: left` | `text-align: right` | Number pushes away from text |
| `.a-q` | `flex: 0 0 auto` | `flex: 1 1 auto` | Question fills all space, answer pinned to far right |
| `.a-ans` | `flex: 1 1 auto; min-width: 0` | `flex: 0 0 auto; min-width: 160px` | Answer pinned to far right with fixed width |

**Rule of thumb:** The answer-list should read left-to-right naturally, like a sentence: `[1] [anxious →] [d — worried because...]`. If any column looks separated or floating on the right, check these three CSS values.

**Also verify the inline `<style>` block is present** — if the template CSS bug (missing `}` in `.cefr-badge`) broke the cascade, the flex rules may not apply at all, causing the browser to fall back to default inline layout (which looks broken). Step 2b is mandatory, not optional.

## Gray text on any background — universal ban

Per **Rule 0 (No Gray Text)**, gray/muted/low-opacity text is banned on ALL slide backgrounds, not just green. This section documents the specific traps in the base template:

**Template traps:**
- `.reveal .aim-label { color: #888; }` — gray label, invisible on `#1a1a2e`, `#1a237e`, `#052e0d`, `#c0392b`, and `#2c3e50`
- `.reveal .source-cite { color: #666; }` — darker gray, still invisible at projection distance
- `.reveal .material-ref { color: #888; }` — invisible gray
- `.reveal .a-num { color: rgba(255,255,255,0.5); }` — 50% white = gray
- `.reveal .image-caption { color: #888; }` — invisible gray

**Fix in Step 2b inline `<style>` block:**
```css
.reveal .aim-label { color: #fff; }
.reveal .source-cite { color: rgba(255,255,255,0.85); }
.reveal .material-ref { color: rgba(255,255,255,0.85); }
.reveal .a-num { color: #fff; }
.reveal .image-caption { color: rgba(255,255,255,0.85); }
```

**Test before commit:** Open the slides in a browser at full-screen projection brightness. If you can't read any text element clearly from 3 meters away, it's too gray. Fix it to `#fff`.
