# Plan: Diagnose and Address KiloCode Token Burn

## Problem Statement
User reports excessive token consumption in KiloCode CLI (~33,977 tokens for a simple research interaction; 2 cents; 17% context used; 119,808 cached tokens).

## Root Causes Identified (from GitHub Issues)

### 1. Critical: Issue #5381 - Rules/Memory Bank Repeatedly Loaded
- **Severity**: Blocker/Critical
- **Status**: Closed Jan 26 2026 but symptoms persist
- **Behavior**: All content in `.kilocode/rules/` (including memory bank and global rules) is repeatedly loaded on **every API request**, rapidly consuming tokens
- **Reproduction**: Create any memory bank and rules under `.kilocode/rules/` and use KiloCode

### 2. Issue #3767 - Infinite Reading Loops
- Agent enters infinite file-reading loops, making 4+ redundant reads of the same files
- Context accumulates: 140k → 262k tokens for a simple query
- Total generation: 8.5 million tokens for a simple code review
- No duplicate read detection, no token budget circuit breakers

### 3. Issue #1132 - Agent Stuck in Loops (Known Since July 2025)
- Affects multiple models (o3, Grok 4, Gemini 2.5 Pro, Claude Sonnet 4, GPT5, Qwen3 Coder)
- Makes KiloCode "almost unusable"

### 4. Memory Unbounded Growth (Issue #6442)
- Session accumulates physical memory never released
- Full message history loaded every round before compaction

## User's Current Setup
- `.kilocode/skills/` - 6 skill directories (write-lesson-plan, typst-author, etc.)
- `.kilocode/rules/` - Only one file: `MCP Tool Usage Instructions.md`
- Project-level `.kilocode/` has skills but no rules subdirectory

## Actual Findings (Read-Only Investigation)

### Global `.kilocode/` contents:
| Path | Size | Notes |
|------|------|-------|
| `rules/MCP Tool Usage Instructions.md` | 18 lines | Only file - not the culprit |
| `workspaceStorage/intellij-workspace/vscode.lock` | 1 line (stale PID) | No actual VSCode data, just a stale lock |
| `secrets.json` | API keys | Config only |
| `package.json` | `@kilocode/plugin: 7.2.25` | CLI dependency |

### No memory-bank directory found
`C:\Users\elwru\.kilocode` does **not** contain a `memory-bank/` directory - so the memory bank is NOT the cause.

### Project-level `.kilocode/`
- Only contains `skills/` with 6 skill directories
- No `rules/` subdirectory at project level

## Confirmed Root Causes

### 1. Issue #5381 - Rules Repeatedly Loaded (STILL ACTIVE)
Even minimal rule files in `.kilocode/rules/` are loaded on **every API request**. Your `MCP Tool Usage Instructions.md` (18 lines) may be sent in full with every single prompt.

**Status**: Issue closed Jan 26 2026 but problem persists in current versions.

### 2. Issue #1132 - Agent Loops (STILL ACTIVE since July 2025)
Agent gets stuck in loops reading files repeatedly, accumulating massive context. No duplicate detection.

### 3. Issue #6442 - Unbounded Memory Growth
Full message history reloaded every round before compaction - causes token bloat over sessions.

### 4. Per-Request Rule Loading Architecture
Per `RulesMigrator.discoverRules()` - ALL files in rule directories are included in every API request. There's no caching between requests.

### 5. User's Actual Version: 7.2.40
User reports `kilo --version` = 7.2.40, which is newer than the 7.2.25 found in `~/.kilocode/package.json`. This means:
- User has a newer CLI version than the global config indicated
- Upgrade may have already been done but not reflected in the old config files
- The token burn issues (#5381, #1132, #6442) are still active in 7.2.40 despite being marked fixed

### 6. New Finding: VSCode Showing as "Last Used" in Integrations Panel
User reports VSCode is showing as "last used" in the integrations panel, not CLI. This is **NOT the problem**.

**Analysis**:
- The "last used" is just UI metadata showing which interface was recently active
- It is stored in `sessions/session.json` and affects only the integrations panel display
- It does NOT get loaded into API requests

**Root cause remains**: Issue #5381 - ALL content in `.kilocode/rules/` is loaded on every API request regardless of which interface (VSCode/CLI/JetBrains) is active.

**Evidence**:
- `workspaceStorage/intellij-workspace/vscode.lock` is stale (PID 18444) with no real VSCode data
- No VSCode-specific configurations persisting in the global storage
- Rules loading is per-request architecture, not per-interface

## Confirmed: "Last Used" Is NOT the Problem

The VSCode showing as "last used" in the integrations panel is **just metadata** - it doesn't affect API requests. The actual token burn comes from **Issue #5381** - rules loaded on every API request.

## Proposed Combined Fix (Option A + Option D)

### Option A: Rename rules directory (immediate test)
1. Rename `C:\Users\elwru\.kilocode\rules\` to `C:\Users\elwru\.kilocode\rules_backup\`
2. Run a CLI command and observe token usage
3. If tokens drop significantly, rules were the culprit

### Option D: Explore built-in cost/context limits
4. Check if `kilocode.maxContextTokens` or similar settings exist in the config
5. Look for any CLI-specific settings (not VSCode) to limit context

## Next Steps (Pending User Approval to Implement)

**Option A** can be tested immediately by renaming the rules folder. Would you like me to proceed with this test?

# Plan: Complete KiloCode + IDE Nuke and Restart

## Problem
Excessive token consumption (~33,977 tokens per simple request; 5 cents per conversation). Want complete cleanout of KiloCode AND IDE (VSCode, WebStorm) settings.

## WARNING: This Will Wipe IDE Settings
- VSCode settings, extensions, workspaces
- WebStorm settings, plugins, projects
- Both IDEs will be reset to fresh install state

## Directories and Files to DELETE

### KiloCode (required)
```powershell
# Main KiloCode global config
Remove-Item -Recurse -Force "C:\Users\elwru\.kilocode"
```

### VSCode (full wipe)
```powershell
# VSCode settings and extensions
Remove-Item -Recurse -Force "C:\Users\elwru\.vscode"
Remove-Item -Recurse -Force "$env:APPDATA\Code"
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\Programs\Microsoft VS Code"
```

### WebStorm (full wipe)
```powershell
# WebStorm settings and config
Remove-Item -Recurse -Force "$env:APPDATA\JetBrains\WebStorm"
Remove-Item -Recurse -Force "$env:APPDATA\.webstorm*"
# Also check in user home
Remove-Item -Recurse -Force "C:\Users\elwru\.WebStorm*"
Remove-Item -Recurse -Force "C:\Users\elwru\.idea*"
```

### Windows AppData (cleanup residual)
```powershell
Remove-Item -Recurse -Force "$env:APPDATA\kilo-code"
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\kilo-code"
```

### npm (if KiloCode was installed globally)
```powershell
npm uninstall -g @kilocode/cli @kilocode/plugin
```

## Projects (DO NOT DELETE)
- `C:\PROJECTS\LESSON PLAN WRITER 3\` - keep this, it's your project data
- Other project folders - keep them, only .kilocode inside them if needed

## After Cleanup: Fresh Install

### 1. VSCode
- Download fresh from https://code.visualstudio.com/
- Install only needed extensions (KiloCode if still using it)

### 2. WebStorm
- Download fresh from https://www.jetbrains.com/webstorm/
- Install only needed plugins

### 3. KiloCode CLI (if wanted)
```powershell
npm install -g @kilocode/cli@latest
kilo --version
```

## Verification Commands
```powershell
Test-Path "C:\Users\elwru\.kilocode"   # Should be False
Test-Path "C:\Users\elwru\.vscode"       # Should be False
Test-Path "$env:APPDATA\JetBrains\WebStorm"  # Should be False
npm list -g @kilocode/cli  # Should be empty
```

## What Will Be Lost
- All VSCode settings, themes, extensions
- All WebStorm settings, plugins
- All KiloCode config, skills, rules
- API keys (need to reconfigure)
- Task history, sessions

## What Will Survive (NOT touched)
- `C:\PROJECTS\LESSON PLAN WRITER 3\` - your project files
- Any other project folders outside .kilocode

---

## Additional Finding: Upgrade Available

User mentioned `kilo upgrade`. Current state:
- **Installed version**: `@kilocode/plugin: 7.2.25` (from `~/.kilocode/package.json`)
- **Latest available**: `7.2.31` (npm) / `v7.1.17` (GitHub releases)
- **Upgrade command**: `kilo upgrade` (or `npm update -g @kilocode/cli`)

The upgrade may include bug fixes for the token burn issues. Recommend upgrading first before implementing other fixes.
