-- lesson-tables.lua
-- Pandoc Lua filter: transforms ## Stage N: headings in the body into a Typst table.
-- Stages are written as standard Markdown in the body. This filter reads them from
-- the AST and generates a Typst #table() with colored headers.
-- Materials stay in YAML (simple string array) — the template renders them with $for(materials)$.

local function escape_typst(text)
  text = text:gsub("\\", "\\\\")
  text = text:gsub("#", "\\#")
  text = text:gsub("_", "\\_")
  text = text:gsub("%[", "\\[")
  text = text:gsub("%]", "\\]")
  text = text:gsub("{", "\\{")
  text = text:gsub("}", "\\}")
  text = text:gsub("~", "\\~")
  text = text:gsub("`", "\\`")
  return text
end

function Pandoc(doc)
  -- ── Collect stage groups from body ──
  local stage_groups = {}
  local current_group = nil
  local stage_heading_indices = {}  -- indices of blocks to remove later

  for i, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level == 2 then
      local text = pandoc.utils.stringify(block.content)
      local stage_num, stage_name = text:match("^Stage%s+(%d+):%s*(.+)$")
      if stage_num then
        current_group = {
          num = stage_num,
          name = stage_name,
          time = "",
          interaction = "",
          aim = "",
          procedure = {},
        }
        table.insert(stage_groups, current_group)
        table.insert(stage_heading_indices, i)
      elseif current_group then
        -- Non-stage heading ends current group
        current_group = nil
      end
    elseif current_group then
      table.insert(stage_heading_indices, i)

      if block.t == "Para" then
        local text = pandoc.utils.stringify(block.content)

        -- "Time: 5 min | Interaction: T-Ss"
        local t, inter = text:match("^Time:%s*(%d+)%s*min%s*|%s*Interaction:%s*(.+)$")
        if t then
          current_group.time = t
          current_group.interaction = inter
        else
          -- "Aim: description text"
          local a = text:match("^Aim:%s*(.+)$")
          if a then
            current_group.aim = a
          end
        end

      elseif block.t == "BulletList" then
        for _, item in ipairs(block.content) do
          for _, inner in ipairs(item) do
            if inner.t == "Para" then
              table.insert(current_group.procedure, pandoc.utils.stringify(inner.content))
            elseif inner.t == "Plain" then
              table.insert(current_group.procedure, pandoc.utils.stringify(inner))
            end
          end
        end
      end
    end
  end

  if #stage_groups == 0 then
    return doc
  end

  -- ── Build Typst table ──
  local t = '#table(\n'
  t = t .. '  columns: (auto, auto, 1fr, 2fr, auto),\n'
  t = t .. '  stroke: 1pt,\n'
  t = t .. '  table.header([*Time*], [*Stage*], [*Goal*], [*Procedure*], [*Int*]),\n'
  t = t .. '  ..(\n'

  for _, row in ipairs(stage_groups) do
    t = t .. '    table.cell(colspan: 5, fill: luma(230))[\n'
    t = t .. '      *STAGE ' .. row.num .. ': ' .. escape_typst(row.name) .. '*\n'
    t = t .. '    ],\n'
    t = t .. '    [' .. row.time .. ' min],\n'
    t = t .. '    [' .. row.num .. '],\n'
    t = t .. '    [' .. escape_typst(row.aim) .. '],\n'
    t = t .. '    [\n'
    for _, item in ipairs(row.procedure) do
      t = t .. '      - ' .. escape_typst(item) .. '\n'
    end
    t = t .. '    ],\n'
    t = t .. '    [' .. row.interaction .. '],\n'
  end

  t = t .. '  ),\n)\n'

  -- ── Replace stage blocks with table ──
  local skip_set = {}
  for _, idx in ipairs(stage_heading_indices) do
    skip_set[idx] = true
  end

  local new_blocks = {}
  local table_inserted = false

  for i, block in ipairs(doc.blocks) do
    if skip_set[i] then
      if not table_inserted then
        -- Insert table before the first skipped block
        table.insert(new_blocks, pandoc.RawBlock('typst', t))
        table_inserted = true
      end
      -- Skip this block (it's in the table now)
    else
      table.insert(new_blocks, block)
    end
  end

  doc.blocks = new_blocks
  return doc
end
