-- audio-player.lua
-- Converts [audio: path/to/file.mp3] in Markdown into <audio controls> HTML element.
-- Also needs slide-helper.lua in the same directory.

local function is_audio_marker(text)
  return text:match("^%[audio:%s*(.+)]$")
end

function Str(el)
  local path = is_audio_marker(el.text)
  if not path then
    return nil
  end

  local src = path:gsub("^%s*(.-)%s*$", "%1")
  local html = '<audio controls src="' .. src .. '"></audio>'

  return pandoc.RawInline("html", html)
end

return {
  { Str = Str },
}
