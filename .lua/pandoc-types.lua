-- pandoc-types.lua
-- LuaCATS type definitions for the Pandoc Lua API.
-- Used by lua-language-server (LuaLS) for diagnostics and autocomplete.
-- Reference: https://pandoc.org/lua-filters.html

-- ── Globals set by pandoc ──────────────────────────────────────────────

--- @type string  Output format (e.g. 'html5', 'latex', 'revealjs')
FORMAT = nil

--- @type table   Pandoc version as numerically-indexed table
PANDOC_VERSION = nil

--- @type table   pandoc-types API version
PANDOC_API_VERSION = nil

--- @type table   Reader options
PANDOC_READER_OPTIONS = nil

--- @type table   Writer options (read-only for filters)
PANDOC_WRITER_OPTIONS = nil

--- @type string  Path to the running Lua filter script
PANDOC_SCRIPT_FILE = nil

--- @type table   Shared pandoc state (read-only)
PANDOC_STATE = nil

--- @type table   LPeg module
lpeg = nil

--- @type table   RE module
re = nil

-- ── Text module ────────────────────────────────────────────────────────

--- @class pandoc_text
--- @field upper fun(s: string): string
--- @field lower fun(s: string): string
--- @field reverse fun(s: string): string
--- @field len fun(s: string): integer
--- @field sub fun(s: string, i: integer, j?: integer): string

-- ── Attr (attributes type) ─────────────────────────────────────────────

--- @class pandoc_attr
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

-- ── Inline elements ────────────────────────────────────────────────────

--- @class pandoc_inline
--- @field tag string
--- @field t string

--- @class pandoc_str : pandoc_inline
--- @field text string

--- @class pandoc_span : pandoc_inline
--- @field attr pandoc_attr
--- @field content pandoc_inline[]
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

--- @class pandoc_strong : pandoc_inline
--- @field content pandoc_inline[]

--- @class pandoc_emph : pandoc_inline
--- @field content pandoc_inline[]

--- @class pandoc_image : pandoc_inline
--- @field attr pandoc_attr
--- @field caption pandoc_inline[]
--- @field src string
--- @field title string
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

--- @class pandoc_link : pandoc_inline
--- @field attr pandoc_attr
--- @field content pandoc_inline[]
--- @field target string
--- @field title string
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

--- @class pandoc_code : pandoc_inline
--- @field attr pandoc_attr
--- @field text string
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

--- @class pandoc_cite : pandoc_inline
--- @field content pandoc_inline[]
--- @field citations table[]

--- @class pandoc_math : pandoc_inline
--- @field mathtype string  "InlineMath" | "DisplayMath"
--- @field text string

--- @class pandoc_rawinline : pandoc_inline
--- @field format string
--- @field text string

--- @class pandoc_smallcaps : pandoc_inline
--- @field content pandoc_inline[]

--- @class pandoc_quoted : pandoc_inline
--- @field quotetype string  "SingleQuote" | "DoubleQuote"
--- @field content pandoc_inline[]

--- @class pandoc_space : pandoc_inline
--- @class pandoc_softbreak : pandoc_inline
--- @class pandoc_linebreak : pandoc_inline

--- @class pandoc_subscript : pandoc_inline
--- @field content pandoc_inline[]

--- @class pandoc_superscript : pandoc_inline
--- @field content pandoc_inline[]

--- @class pandoc_strikeout : pandoc_inline
--- @field content pandoc_inline[]

-- ── Block elements ─────────────────────────────────────────────────────

--- @class pandoc_block
--- @field tag string
--- @field t string

--- @class pandoc_div : pandoc_block
--- @field attr pandoc_attr
--- @field content pandoc_block[]
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>
--- @field walk fun(self: pandoc_div, filter: table): pandoc_div

--- @class pandoc_para : pandoc_block
--- @field content pandoc_inline[]
--- @field tag string
--- @field t string
--- NOTE: Para does NOT have attr/attributes/classes/identifier

--- @class pandoc_plain : pandoc_block
--- @field content pandoc_inline[]
--- @field tag string
--- @field t string
--- NOTE: Plain does NOT have attr/attributes/classes/identifier

--- @class pandoc_header : pandoc_block
--- @field level integer
--- @field content pandoc_inline[]
--- @field attr pandoc_attr
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

--- @class pandoc_blockquote : pandoc_block
--- @field content pandoc_block[]

--- @class pandoc_codeblock : pandoc_block
--- @field attr pandoc_attr
--- @field text string
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

--- @class pandoc_bulletlist : pandoc_block
--- @field content table[]

--- @class pandoc_orderedlist : pandoc_block
--- @field content table[]
--- @field listattributes table
--- @field start integer
--- @field style string
--- @field delimiter string

--- @class pandoc_definitionlist : pandoc_block
--- @field content table[]

--- @class pandoc_table : pandoc_block
--- @field attr pandoc_attr
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

--- @class pandoc_horizontalrule : pandoc_block

--- @class pandoc_lineblock : pandoc_block
--- @field content table[]

--- @class pandoc_rawblock : pandoc_block
--- @field format string
--- @field text string

--- @class pandoc_figure : pandoc_block
--- @field attr pandoc_attr
--- @field content pandoc_block[]
--- @field caption table
--- @field identifier string
--- @field classes table
--- @field attributes table<string,string>

-- ── Pandoc module functions ────────────────────────────────────────────

--- @class pandoc_module
--- @field Str fun(text: string): pandoc_str
--- @field Span fun(content: pandoc_inline[], attr?: table): pandoc_span
--- @field Strong fun(content: pandoc_inline[]): pandoc_strong
--- @field Emph fun(content: pandoc_inline[]): pandoc_emph
--- @field Image fun(caption: pandoc_inline[], src: string, title?: string, attr?: table): pandoc_image
--- @field Link fun(content: pandoc_inline[], target: string, title?: string, attr?: table): pandoc_link
--- @field Code fun(text: string, attr?: table): pandoc_code
--- @field Div fun(content: pandoc_block[], attr?: table): pandoc_div
--- @field Para fun(content: pandoc_inline[]): pandoc_para
--- @field Plain fun(content: pandoc_inline[]): pandoc_plain
--- @field Header fun(level: integer, content: pandoc_inline[], attr?: table): pandoc_header
--- @field BlockQuote fun(content: pandoc_block[]): pandoc_blockquote
--- @field CodeBlock fun(text: string, attr?: table): pandoc_codeblock
--- @field BulletList fun(content: table[]): pandoc_bulletlist
--- @field OrderedList fun(content: table[], listattributes?: table): pandoc_orderedlist
--- @field RawBlock fun(format: string, text: string): pandoc_rawblock
--- @field RawInline fun(format: string, text: string): pandoc_rawinline
--- @field HorizontalRule fun(): pandoc_horizontalrule
--- @field Space fun(): pandoc_space
--- @field SoftBreak fun(): pandoc_softbreak
--- @field LineBreak fun(): pandoc_linebreak
--- @field Note fun(content: pandoc_block[]): pandoc_block[]
--- @field SmallCaps fun(content: pandoc_inline[]): pandoc_smallcaps
--- @field Strikeout fun(content: pandoc_inline[]): pandoc_strikeout
--- @field Subscript fun(content: pandoc_inline[]): pandoc_subscript
--- @field Superscript fun(content: pandoc_inline[]): pandoc_superscript
--- @field Quoted fun(quotetype: string, content: pandoc_inline[]): pandoc_quoted
--- @field Cite fun(content: pandoc_inline[], citations: table[]): pandoc_cite
--- @field Math fun(mathtype: string, text: string): pandoc_math
--- @field LineBlock fun(content: table[]): pandoc_lineblock
--- @field DefinitionList fun(content: table[]): pandoc_definitionlist
--- @field Figure fun(content: pandoc_block[], caption: table, attr?: table): pandoc_figure
--- @field Meta fun(table: table): table
--- @field MetaMap fun(table: table): table
--- @field MetaList fun(list: table[]): table
--- @field Inlines fun(list: pandoc_inline[]): pandoc_inline[]
--- @field Blocks fun(list: pandoc_block[]): pandoc_block[]
--- @field text pandoc_text
--- @field read fun(text: string, format?: string): table
--- @field pipe fun(command: string[], args: string[], input: string): string
--- @field mediabag table
--- @field utils table
--- @field system table
--- @field walk_block fun(block: pandoc_block, filter: table): pandoc_block
--- @field walk_inline fun(inline: pandoc_inline, filter: table): pandoc_inline

--- @type pandoc_module
--- Global `pandoc` module provided by the Pandoc Lua interpreter.
-- luacheck: ignore 421  (lowercase global is intentional)
pandoc = nil
