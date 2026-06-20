-- youtube-embed.lua
-- Converts fenced div with class "youtube" into a YouTube iframe embed
-- inside the slide (not fullscreen background).
--
-- Usage:  ::: {.youtube}
--         VIDEO_ID
--         :::
--
-- Uses slide-helper.lua for HTML generation (loaded via dofile).

if FORMAT:match('revealjs') then
  local source = debug.getinfo(1).source:gsub('^@', '')
  local script_dir = source:match("(.*[/\\])")
  local slide = dofile(script_dir .. 'slide-helper.lua')

  function Div(d)
    if d.classes:includes('youtube') then
      local video_id = nil
      for _, block in ipairs(d.content) do
        if block.t == 'Para' or block.t == 'Plain' then
          for _, inline in ipairs(block.content) do
            if inline.t == 'Str' then
              video_id = inline.text
              break
            end
          end
        end
        if video_id then break end
      end

      if video_id then
        return pandoc.RawBlock('html', slide.youtube_iframe(video_id))
      end
    end
  end
end
