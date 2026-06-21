# Troubleshooting

## Common Errors

| Symptom | Fix |
|---------|-----|
| Vertical slides (down arrow) | Use `--slide-level=1`, not `--slide-level=2` |
| YouTube Error 153 | Serve from HTTP server, not file://. Check `slides-header.html` has referrer meta tag |
| Fragment answer always visible | Check CSS doesn't set `opacity: 1` on `.fragment.answer-reveal` |
| Text too wide/narrow | Adjust `margin` in build command: `-V margin=0.125` = 75% content width |
| Blockquote too large | CSS sets `blockquote { font-size: 0.85em }` |
| Empty heading showing space | CSS `.reveal h1:empty { display: none }` handles this |
| Audio doesn't play | Check `data-audio-src` is on the `#` heading, not a `##` heading |
| YouTube embed not showing | Ensure `youtube-embed.lua` is in `--lua-filter` |
| Logo not showing | Ensure `assets/logo.png` exists (copied from `templates/ACT.png`) |
| Splash image not showing | Check `data-background-image` path is relative to `slides/` directory |
| Auto-animate not working | Both slides need `data-auto-animate="true"` and same `data-auto-animate-id` |

## Visual Effects — Correct Approach (NOT CSS)

When you need a visual effect, use one of these Pandoc Markdown or Lua filter mechanisms.
**Do NOT read or edit CSS/HTML files.** The answer is always below.

| Visual problem | Correct approach | Syntax / Lua function |
|---|---|---|
| Text needs to be yellow / call-to-action | Use `.cta-text` bracketed span | `[text]{.cta-text}` |
| Text needs yellow CTA with bold | Use `.cta` bracketed span | `[text]{.cta}` |
| Text needs dark backdrop on image-bg slide | Use `.shield` fenced div | `::: {.shield} ... :::` |
| Text needs to be larger | Use heading level (h1 for slide title, ### for sub-heading) | `### heading` |
| Content needs centering | Use `.shield` fenced div (flexbox centers content) | `::: {.shield} ... :::` |
| Columns needed | Use stacked `.shield` divs (shield-block.lua forces vertical stack) | Three `::: {.shield}` in sequence |
| Fragments (click-to-reveal) | Add `.fragment` class to fenced div | `::: {.fragment} ... :::` |
| Answer reveal (fragment) | Add `.fragment.answer-reveal` | `::: {.fragment .answer-reveal} ... :::` |
| Title row with CEFR badge | Use bracketed span with `.badge` class | `[B1]{.badge}` inside `# heading` |
| Audio autoplay on slide | Add `data-audio-src` attribute to `# heading` | `# heading {data-audio-src="assets/file.mp3"}` |
| YouTube embed | Use `::: {.youtube}` fenced div with ID on next line | `::: {.youtube}` / `VIDEO_ID` / `:::` |
| Background image on slide | Add `data-background-image` to `# heading` | `# heading {data-background-image="assets/img.jpg"}` |
| Background color on slide | Add `data-background-color` to `# heading` | `# heading {data-background-color="#333"}` |
