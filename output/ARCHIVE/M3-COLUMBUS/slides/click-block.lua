-- click-block.lua
-- Converts each paragraph inside a {.block} div into a reveal.js fragment,
-- so content appears one click at a time.
-- Usage: pandoc --lua-filter=click-block.lua ...

if FORMAT:match('revealjs') then

  function Div(el)
    for _, cls in ipairs(el.attr.classes) do
      if cls == "block" then
        local new_content = {}
        for _, block in ipairs(el.content) do
          if block.t == "Para" then
            table.insert(new_content, pandoc.Div(
              block.content,
              {class = "fragment"}
            ))
          else
            table.insert(new_content, block)
          end
        end
        el.content = new_content
        return el
      end
    end
    return el
  end

end
