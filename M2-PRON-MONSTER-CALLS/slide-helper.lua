-- slide-helper.lua — Reusable Lua library for reveal.js slides
--
-- A shared module providing utility functions for Pandoc Lua filters
-- that generate reveal.js HTML. Other Lua filters import this module
-- with `require('slide-helper')`.
--
-- Usage from another Lua filter:
--   local slide = require('slide-helper')
--   local html = slide.youtube_iframe('dQw4w9WgXcQ')
--   local html = slide.audio_tag('assets/clip.mp3')
--
-- This module is maintained by the developer. Do NOT hand-edit during
-- slide generation — the agent writes Markdown, Lua filters transform.

local M = {}

-- ── YouTube iframe ──────────────────────────────────────────────────

--- Generate a responsive YouTube embed iframe.
--- @param video_id string  11-char YouTube video ID
--- @return string  responsive iframe HTML
function M.youtube_iframe(video_id)
  local src = 'https://www.youtube.com/embed/' .. video_id
  return '<div class="iframe-container" style="width: 80%; padding-bottom: 45%;">'
    .. '<iframe src="' .. src .. '" '
    .. 'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
    .. 'gyroscope; picture-in-picture; web-share" '
    .. 'referrerpolicy="strict-origin-when-cross-origin" '
    .. 'allowfullscreen></iframe></div>'
end

-- ── Audio autoplay ──────────────────────────────────────────────────

--- Generate an <audio> tag with data-autoplay for reveal.js.
--- @param src string  path to audio file (relative to index.html)
--- @return string  audio HTML element
function M.audio_tag(src)
  return '<audio data-autoplay src="' .. src .. '"></audio>'
end

-- ── Countdown timer ─────────────────────────────────────────────────

--- Generate a reveal.js timer element.
--- @param seconds number  countdown in seconds
--- @return table  {Div} containing the timer HTML
function M.timer_div(seconds)
  local html = '<div data-timer="' .. tostring(seconds) .. '" '
    .. 'style="position: fixed; top: 20px; right: 20px; '
    .. 'background: rgba(0,0,0,0.85); color: #ffdd00; '
    .. 'padding: 12px 20px; border-radius: 6px; '
    .. 'font-size: 1.5em; z-index: 100; font-weight: bold;"></div>'
  return pandoc.RawBlock('html', html)
end

-- ── Slide background attributes ─────────────────────────────────────

--- Set background attributes on a heading.
--- Use:  Header = slide.set_background(Header, 'assets/img.jpg')
--- @param header table   Pandoc Header element
--- @param image string   path to background image (or nil for solid color)
--- @param color string   CSS color (default '#1a1a2e')
--- @return table  modified Header with data-background-* attrs
function M.set_background(header, image, color)
  color = color or '#1a1a2e'
  header.attributes['data-background-color'] = color
  if image then
    header.attributes['data-background-image'] = image
    header.attributes['data-background-size'] = 'cover'
  end
  return header
end

-- ── Fragment answer wrapper ─────────────────────────────────────────

--- Wrap content in a fragment answer-reveal div.
--- @param content table  list of Pandoc Block elements
--- @return table  Div with fragment + answer-reveal classes
function M.fragment_answer(content)
  return pandoc.Div(content, {class = 'fragment answer-reveal'})
end

-- ── Shield div (for text on image backgrounds) ──────────────────────

--- Wrap content in a shield div.
--- @param content table  list of Pandoc Block elements
--- @return table  Div with shield class
function M.shield(content)
  return pandoc.Div(content, {class = 'shield'})
end

-- ── Title row div ───────────────────────────────────────────────────

--- Create a title-row div with slide-title span.
--- @param title_text string  the title text
--- @param cefr_badge string|nil  optional CEFR badge like 'B2'
--- @return table  Div with title-row class
function M.title_row(title_text, cefr_badge)
  local content = {
    pandoc.Span(
      {pandoc.Strong({pandoc.Str(title_text)})},
      {class = 'slide-title'}
    )
  }
  if cefr_badge then
    table.insert(content, pandoc.Str(' '))
    table.insert(content, pandoc.Span(
      {pandoc.Str(cefr_badge)},
      {class = 'cefr-badge'}
    ))
  end
  return pandoc.Div(content, {class = 'title-row'})
end

-- ── CTA text span ───────────────────────────────────────────────────

--- Create a call-to-action text span.
--- @param text string  CTA text
--- @return table  Span with cta-text class
function M.cta(text)
  return pandoc.Span(
    {pandoc.Strong({pandoc.Str(text)})},
    {class = 'cta-text'}
  )
end

-- ── Extract heading attribute ───────────────────────────────────────

--- Safely get an attribute from a Pandoc element.
--- @param elem table   Pandoc element with .attributes
--- @param key string   attribute name (e.g. 'data-audio-src')
--- @return string|nil  attribute value or nil
function M.get_attr(elem, key)
  if elem and elem.attributes then
    return elem.attributes[key]
  end
  return nil
end

-- ── Auto-animate helpers ────────────────────────────────────────────

--- Set auto-animate on a heading.
--- @param header table  Pandoc Header element
--- @param animate_id string  shared auto-animate-id
--- @return table  modified Header
function M.set_auto_animate(header, animate_id)
  header.attributes['data-auto-animate'] = 'true'
  header.attributes['data-auto-animate-id'] = animate_id
  return header
end

return M
