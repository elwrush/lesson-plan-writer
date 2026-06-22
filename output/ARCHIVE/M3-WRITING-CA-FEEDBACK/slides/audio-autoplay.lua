-- audio-autoplay.lua
-- Pandoc Lua filter: reads data-audio-src from headings and injects
-- <audio data-autoplay src="..."> for native reveal.js audio playback.
-- No plugins needed -- reveal.js autoplays <audio data-autoplay> when the slide enters.
-- Only activates for revealjs output.

if FORMAT:match('revealjs') then
  function Header(h)
    local audio_src = h.attributes['data-audio-src']
    if audio_src then
      return {
        h,
        pandoc.RawBlock('html', '<audio data-autoplay src="' .. audio_src .. '"></audio>')
      }
    end
  end
end
