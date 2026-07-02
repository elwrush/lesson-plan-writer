if FORMAT:match('revealjs') then
  function RawBlock(el)
    if el.format == 'html' and el.text:match('<audio ') then
      el.text = el.text:gsub('<audio ', '<audio controls style="width: 100%%; max-width: 640px; height: 52px; display: block; margin: 1em auto;" ')
      el.text = el.text:gsub(' data%-autoplay', '')
    end
    return el
  end
end
