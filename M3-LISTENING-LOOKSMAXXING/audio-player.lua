--- Converts ::: {.audio-player} divs into <audio controls> elements.
--- The first line inside the div is the src path.
function Div(el)
  if el.classes:find("audio-player") then
    local src = ""
    for _, block in ipairs(el.content) do
      if block.t == "Para" then
        src = pandoc.utils.stringify(block)
        break
      end
    end
    if src ~= "" then
      local html = '<audio controls src="' .. src .. '" style="width:100%"></audio>'
      return pandoc.RawBlock("html", html)
    end
  end
  return nil
end
