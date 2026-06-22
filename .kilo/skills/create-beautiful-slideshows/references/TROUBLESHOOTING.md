# Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Pandoc fails "Unknown writer" | Pandoc too old | Update Pandoc to 3.9+ |
| YouTube embed Error 153 | Used `data-background-iframe` | Use `::: {.youtube}` div pattern |
| Audio does not autoplay | Wrong path or missing filter | Verify `audio-autoplay.lua` in filter list, file exists |
| Fragments visible on entry | Missing `.fragment` class | Use `[text]{.fragment .answer-reveal}` |
| Auto-animate element vanishes | `data-id` missing on reveal slide | Every `data-id` from entry must exist on reveal |
| CEFR badge not rendering | Missing `.title-row` wrapper | Wrap badge in `::: {.title-row}` |
| Shield not visible | `shield-block.lua` missing | Add to pandoc build command |
| Text unreadable on image | Missing `.shield` wrapper | Wrap text in `::: {.shield}` |

## Browser/Server

- YouTube embeds require `http://localhost:8000/` — they block `file://`
- Refresh the browser after every rebuild (`Ctrl+F5` for hard refresh)
- If server won't start, port 8000 may be in use: kill the process or use a different port
