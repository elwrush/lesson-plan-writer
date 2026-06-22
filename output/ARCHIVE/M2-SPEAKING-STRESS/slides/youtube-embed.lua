-- youtube-embed.lua
-- Converts fenced div with class "youtube" into a YouTube iframe embed
-- inside the slide (not fullscreen background).
--
-- Usage:  ::: {.youtube}
--         VIDEO_ID
--         :::

if FORMAT:match('revealjs') then
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
        local src = 'https://www.youtube.com/embed/' .. video_id
        local html = '<div class="iframe-container" style="width: 80%; padding-bottom: 45%;">'
          .. '<iframe src="' .. src .. '" '
          .. 'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
          .. 'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
        return pandoc.RawBlock('html', html)
      end
    end
  end
end
