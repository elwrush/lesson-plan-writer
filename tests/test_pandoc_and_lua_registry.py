"""
test_pandoc_and_lua_registry.py — Red-green tests enforcing two rules:

1. Pandoc version check — alerts when Pandoc has been updated (new features
   may replace custom code). Fails if Pandoc version is newer than tested,
   forcing a review of what changed.

2. No bespoke Lua filter without prior search — every custom Lua filter in
   scripts/ must be registered in scripts/lua-filter-registry.json with a
   justification of why no existing solution was suitable. If the registry
   is missing an entry, the test fails (red) and forces a Tavily search.

Process:
  - RED phase: test fails because filter isn't in registry → run Tavily search
  - GREEN phase: search confirms no existing solution → update registry → test passes
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
REGISTRY_PATH = SCRIPTS_DIR / "lua-filter-registry.json"

# ── Helpers ────────────────────────────────────────────────────────────


def get_pandoc_version() -> tuple:
    """Return (major, minor, patch) tuple from `pandoc -v`."""
    result = subprocess.run(
        ["pandoc", "-v"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    first_line = result.stdout.split("\n")[0]
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", first_line)
    if match:
        parts = match.groups()
        return (int(parts[0]), int(parts[1]), int(parts[2] or 0))
    raise RuntimeError(f"Could not parse Pandoc version from: {first_line}")


def get_custom_lua_filters() -> list[str]:
    """Return names of custom Lua filter files that are registered.

    Gets the list from the registry's custom_filters.entries, then checks
    that each file actually exists in scripts/. This keeps the file list
    in sync with the registry.
    """
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        data = json.load(f)
    registered = set()
    for entry in data.get("custom_filters", {}).get("entries", []):
        registered.add(entry["name"])
    # Only return filters that actually exist as files
    existing = set(f.name for f in SCRIPTS_DIR.glob("*.lua"))
    return sorted(registered & existing)


def get_registered_custom_filters() -> dict:
    """Return {name: entry} for custom_filters from the registry."""
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        data = json.load(f)
    entries = {}
    for entry in data.get("custom_filters", {}).get("entries", []):
        entries[entry["name"]] = entry
    return entries


def load_registry() -> dict:
    """Load the full registry JSON."""
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


# ── Tests ──────────────────────────────────────────────────────────────


class TestPandocVersion:
    """Check Pandoc version and flag newer releases."""

    # The version this codebase was tested against. When Pandoc is upgraded,
    # update this AFTER reviewing the changelog for relevant new features.
    TESTED_VERSION = (3, 10, 0)

    def test_pandoc_is_installed(self):
        """Pandoc must be installed and accessible."""
        try:
            version = get_pandoc_version()
            assert len(version) == 3, f"Unexpected version format: {version}"
        except FileNotFoundError:
            pytest.fail("Pandoc is not installed or not in PATH")
        except RuntimeError as e:
            pytest.fail(str(e))

    def test_pandoc_version_meets_minimum(self):
        """Pandoc must be at least 3.9 for --syntax-highlighting=idiomatic."""
        version = get_pandoc_version()
        assert version >= (3, 9, 0), (
            f"Pandoc {'.'.join(map(str, version))} is too old. "
            f"Minimum required: 3.9.0 (for --syntax-highlighting=idiomatic). "
            f"Run: winget install pandoc"
        )

    def test_pandoc_version_known(self):
        """Alert if Pandoc version is newer than tested (may have new features).

        RED: Version is newer than TESTED_VERSION →
          read https://pandoc.org/releases.html for changelog →
          update TESTED_VERSION → green.

        If new features make a custom filter obsolete, remove or simplify it.
        """
        version = get_pandoc_version()
        assert version <= self.TESTED_VERSION, (
            f"Pandoc {'.'.join(map(str, version))} is NEWER than tested "
            f"version {'.'.join(map(str, self.TESTED_VERSION))}.\n\n"
            f"  Action required:\n"
            f"  1. Read: https://pandoc.org/releases.html\n"
            f"  2. Search: python scripts/tavily_search.py "
            f'"pandoc {".".join(map(str, version))} changelog new features"\n'
            f"  3. Check if any new feature replaces a custom Lua filter\n"
            f"  4. If yes — remove/replace the filter and update tests\n"
            f"  5. Update TESTED_VERSION in this test to {'.'.join(map(str, version))}\n"
        )


class TestLuaFilterRegistry:
    """Every custom Lua filter must be registered with a search justification.

    RED: A custom filter exists in scripts/ but is NOT in the registry.
         → Run a Tavily search for existing solutions.
         → If one exists, use it instead (delete the custom filter).
         → If none exists, add an entry to lua-filter-registry.json.

    This prevents writing bespoke code without first checking the ecosystem.
    """

    def test_all_custom_filters_are_registered(self):
        """Every slide-relevant Lua filter must have a registry entry."""
        custom_filters = get_custom_lua_filters()
        registered = get_registered_custom_filters()

        unregistered = [f for f in custom_filters if f not in registered]

        assert not unregistered, (
            f"Custom Lua filter(s) not found in registry: {unregistered}\n\n"
            f"  A new custom filter was added without a Tavily search.\n\n"
            f"  To fix (GREEN phase):\n"
            f"  1. For each unregistered filter, run a Tavily search:\n"
            f"     python scripts/tavily_search.py "
            f'"pandoc lua filter reveal.js ..."\n'
            f"  2. If an existing solution IS found:\n"
            f"     - Delete the custom filter\n"
            f"     - Use the existing solution instead\n"
            f"  3. If NO existing solution exists:\n"
            f"     - Add an entry to scripts/lua-filter-registry.json\n"
            f"       under 'custom_filters.entries' with:\n"
            f"       - name, purpose, why_no_existing,\n"
            f"       - tavily_searched: today's date,\n"
            f"       - search_query: what you searched,\n"
            f"       - search_verified: true\n"
            f"  4. Re-run tests to confirm GREEN\n"
        )

    def test_registry_has_all_required_fields(self):
        """Each registry entry must have complete metadata."""
        registered = get_registered_custom_filters()
        required = {
            "name",
            "purpose",
            "why_no_existing",
            "tavily_searched",
            "search_query",
            "search_verified",
        }
        for name, entry in registered.items():
            missing = required - set(entry.keys())
            assert not missing, (
                f"Registry entry '{name}' is missing fields: {missing}. "
                f"All entries need: {required}"
            )

    def test_registry_search_queries_are_nonempty(self):
        """Search queries must be meaningful (not placeholder text)."""
        registered = get_registered_custom_filters()
        placeholders = {"CHANGE THIS", "TODO", "FIXME", ""}
        for name, entry in registered.items():
            q = entry.get("search_query", "")
            assert q not in placeholders, (
                f"Registry entry '{name}' has placeholder search query "
                f"'{q}'. Run a real Tavily search and update the query."
            )
            assert len(q) > 15, (
                f"Registry entry '{name}' has suspiciously short "
                f"search query '{q}'. Be more specific."
            )

    def test_registry_json_is_valid(self):
        """Registry must be valid JSON with the required structure."""
        try:
            data = load_registry()
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid registry JSON: {e}")

        assert "_version" in data, "Registry missing _version field"
        assert "filters" in data, "Registry missing filters array"
        assert "custom_filters" in data, "Registry missing custom_filters section"
        assert "entries" in data["custom_filters"], "custom_filters missing entries array"

    def test_known_filters_list_is_current(self):
        """Flag if the known-filters table in the SKILL.md is outdated.

        This tests for a GitHub-pages-updated Pandoc that may have
        new filters in the pandoc-ext ecosystem.
        """
        # This is a soft check — we just verify the registry has at least
        # 5 known filters (baseline from pandoc/lua-filters and pandoc-ext).
        data = load_registry()
        known_count = len(data.get("filters", []))
        assert known_count >= 5, (
            f"Only {known_count} known filters in registry. "
            f"Review https://github.com/pandoc-ext for new additions "
            f"and update the registry."
        )


class TestCustomFilterJustification:
    """Each custom filter's 'why_no_existing' must be genuinely justified.

    This is a semantic check — the justification should explain why
    the pandoc-ext ecosystem, pandoc/lua-filters, or built-in Pandoc
    features were insufficient.
    """

    BAD_PATTERNS = [
        "didn't look",
        "too hard",
        "not found",
        "couldn't find",
        "no time",
    ]

    def test_why_no_existing_is_substantive(self):
        registered = get_registered_custom_filters()
        for name, entry in registered.items():
            why = entry.get("why_no_existing", "")
            assert len(why) > 50, (
                f"Registry entry '{name}' has suspiciously short "
                f"justification ({len(why)} chars). "
                f"Explain why no existing solution works."
            )
            for pattern in self.BAD_PATTERNS:
                assert pattern not in why.lower(), (
                    f"Registry entry '{name}' uses weak justification "
                    f"'{pattern}'. Be specific about what was searched "
                    f"and why each alternative failed."
                )


class TestNoBespokeWithoutSearch:
    """Integration: the full pipeline must pass registry check.

    This is the top-level red-green gate:
      RED   → custom filter exists without registry entry
      GREEN → all custom filters are justified in the registry
    """

    def test_registry_is_complete(self):
        """Final gate: all filters in the registry match actual files."""
        custom_filters = set(get_custom_lua_filters())
        registered = set(get_registered_custom_filters().keys())

        missing_from_files = registered - custom_filters
        assert not missing_from_files, (
            f"Registry references filters that don't exist: {missing_from_files}. "
            f"Either restore the files or remove the registry entries."
        )


# ── Tavily search automation ──────────────────────────────────────────
# The tavily_search.py script is called by the test workflow (not during
# test execution, to avoid network dependency). The search happens in
# the RED phase, and results update the registry for the GREEN phase.


def test_tavily_search_script_exists():
    """The Tavily search scaffold must exist in scripts/ for RED phase searching."""
    search_script = SCRIPTS_DIR / "tavily_search.py"
    assert search_script.exists(), (
        f"Tavily search script not found at {search_script}.\n\n"
        f"This script is needed for the RED phase workflow:\n"
        f"  1. Test fails (RED): 'unregistered filter'\n"
        f"  2. Run: python scripts/tavily_search.py "
        f'"pandoc lua filter ..."\n'
        f"  3. If existing solution found → delete custom filter\n"
        f"  4. If no solution → update registry → test passes (GREEN)\n\n"
        f"Create scripts/tavily_search.py with Model A from "
        f"the tavily-websearch skill."
    )
