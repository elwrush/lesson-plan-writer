-- audio-controls.lua
-- Converts ::: {.audio-controls} divs into <audio controls> elements.
-- Usage: ::: {.audio-controls} path/to/file.mp3 :::

local function extract_path(div)
  local path = ""
  for _, block in ipairs(div.content) do
    if block.t == "Para" then
      for _, inline in ipairs(block.content) do
        if inline.t == "Str" then
          path = path .. inline.text
        elseif inline.t == "Space" then
          path = path .. " "
        end
      end
    end
  end
  return path:match("^%s*(.-)%s*$")
end

function Div(el)
  if el.classes:find("audio-controls", 1) then
    local src = extract_path(el)
    if src and src ~= "" then
      local html = '<audio controls src="' .. src .. '"></audio>'
      return pandoc.RawBlock("html", html)
    end
  end
  return nil
end

return {
  { Div = Div },
}
