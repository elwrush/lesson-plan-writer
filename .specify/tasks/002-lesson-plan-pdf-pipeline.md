## Backlog

- [x] parse_frontmatter(): YAML parsing with REQUIRED_META validation
- [x] Template hash-verification via .template-lock.json
- [x] Pandoc invocation with lesson-tables.lua filter
- [x] Typst compilation from generated .typ to .pdf
- [x] Output linting (page count, text presence, forbidden text absence)
- [x] tests/test_build_lesson_pdf.py frontmatter + lint tests
- [ ] Post-build PDF content verification (extract text, verify stage names/aims/vocab)
- [ ] Pre-build markdown structure check (blank lines before bullet lists, stage heading format, timing sums)
- [ ] lesson-tables.lua Para capture test: verify all Para types preserved (not just Time/Aim)
- [ ] Cross-platform path resolution in build scripts (%USERPROFILE% → $HOME fallback)
- [ ] SHAPE Literal coverage check: compare against lesson-plan-skill shapes A-G
- [ ] tests/test_lesson_tables_lua.py: Para capture + blank line trap tests
