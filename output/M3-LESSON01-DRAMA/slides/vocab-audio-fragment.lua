-- vocab-audio-fragment.lua
-- Injects <audio data-autoplay src="..."> inside Spans with data-audio-src.
-- When the Span is a reveal.js fragment, the audio starts when the fragment
-- is revealed (not on slide entry).
-- Usage: pandoc --lua-filter=vocab-audio-fragment.lua ...
-- Depends on: slide-helper.lua in same directory

if FORMAT:match('revealjs') then
  local source = debug.getinfo(1).source:gsub('^@', '')
  local script_dir = source:match("(.*[/\\])")
  local slide = dofile(script_dir .. 'slide-helper.lua')

  function Span(el)
    local audio_src = el.attributes['data-audio-src']
    if audio_src then
      -- Append <audio data-autoplay> inside the span content
      table.insert(el.content, pandoc.RawInline('html', slide.audio_tag(audio_src)))
      -- Remove the attribute so it doesn't appear as HTML attribute
      el.attributes['data-audio-src'] = nil
      return el
    end
  end
end
