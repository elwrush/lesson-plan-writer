# Troubleshooting

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
