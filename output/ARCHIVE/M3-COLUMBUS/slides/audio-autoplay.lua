-- audio-autoplay.lua
-- Pandoc Lua filter: reads data-audio-src from headings and injects
-- <audio data-autoplay src="..."> for native reveal.js audio playback.
-- No plugins needed -- reveal.js autoplays <audio data-autoplay> when the slide enters.
-- Only activates for revealjs output.
-- Uses slide-helper.lua for HTML generation (loaded via dofile).

if FORMAT:match('revealjs') then
  local source = debug.getinfo(1).source:gsub('^@', '')
  local script_dir = source:match("(.*[/\\])")
  local slide = dofile(script_dir .. 'slide-helper.lua')

  function Header(h)
    local audio_src = slide.get_attr(h, 'data-audio-src')
    if audio_src then
      return {
        h,
        pandoc.RawBlock('html', slide.audio_tag(audio_src))
      }
    end
  end
end
