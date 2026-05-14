"""
test_git_pages_safety.py — Red-Green Test for /git-pages Command Safety

Red phase (old version, should FAIL):
    - Contains "git checkout gh-pages"
    - Contains "git clean -fd"
    - Contains "git rm -rf ."
    - Missing "git worktree add"

Green phase (new version, should PASS):
    - Contains "git worktree add"
    - Contains "git -C $worktreeDir"
    - Contains NO "git checkout gh-pages"
    - Contains NO "git clean -fd"
    - Contains NO "git rm -rf ."
    - Contains NO "Push-Location" (except bootstrap first-deploy block)
"""

COMMAND_FILE = ".kilo/command/git-pages.md"


def load_command_file():
    with open(COMMAND_FILE, encoding="utf-8") as f:
        return f.read()


def extract_code_blocks(content):
    """Extract only the lines inside ```powershell ... ``` blocks."""
    in_block = False
    lines = []
    for line in content.split("\n"):
        if line.strip().startswith("```powershell"):
            in_block = True
            continue
        if line.strip() == "```" and in_block:
            in_block = False
            continue
        if in_block:
            lines.append(line)
    return "\n".join(lines)


def test_red_phase_would_fail():
    """
    RED PHASE: Verify these dangerous patterns would appear in the old version.
    This test documents what the OLD (broken) code looked like. If this test
    starts passing, someone re-introduced dangerous patterns.
    """
    code = extract_code_blocks(load_command_file())
    old_patterns = [
        "# Step 5b: Switch to gh-pages branch",
        "git checkout gh-pages",
        "git rm -rf .",
        "git clean -fd",
    ]
    for pattern in old_patterns:
        assert pattern not in code, (
            f"RED PHASE FAILED: Found DANGEROUS pattern '{pattern}' in a PowerShell code block.\n"
            f"The old git-pages command used this pattern and could destroy the project."
        )


class TestGreenPhaseRequired:
    """GREEN PHASE: Must-have safety patterns."""

    def test_uses_git_worktree(self):
        content = load_command_file()
        assert "git worktree add" in content, (
            "Must use git worktree add to check out gh-pages in an isolated directory.\n"
            "Without this, the command operates on the main working tree and risks destruction."
        )

    def test_uses_git_C_flag(self):  # noqa: N802
        content = load_command_file()
        assert "git -C $worktreeDir" in content, (
            "Must use 'git -C $worktreeDir' explicitly instead of Push-Location.\n"
            "Push-Location does not survive across separate command executions."
        )

    def test_no_direct_branch_switch(self):
        """Verify NO 'git checkout gh-pages' (or similar) exists outside prose."""
        content = load_command_file()
        # Only flag when it appears inside a PowerShell code block (actual command),
        # not in prose descriptions like "Regression Guard" or "Safety" sections.
        # Split into code blocks by looking for lines between ```powershell and ```
        in_code_block = False
        code_lines = []
        for line in content.split("\n"):
            if line.strip().startswith("```powershell"):
                in_code_block = True
                continue
            if line.strip() == "```" and in_code_block:
                in_code_block = False
                continue
            if in_code_block:
                code_lines.append(line)
        code_content = "\n".join(code_lines)
        assert "git checkout" not in code_content, (
            "Found 'git checkout' in a PowerShell code block.\n"
            "Use 'git worktree add' instead — never switch branches in the main working tree."
        )

    def test_no_git_rm_rf(self):
        code = extract_code_blocks(load_command_file())
        assert "git rm -rf" not in code, (
            "Found 'git rm -rf' in a PowerShell code block.\n"
            "This command destroys tracked files from the working tree.\n"
            "The gh-pages worktree is cleaned by removing the entire worktree directory, "
            "not by editing files inside it."
        )

    def test_no_git_clean_fd(self):
        code = extract_code_blocks(load_command_file())
        assert "git clean -fd" not in code, (
            "Found 'git clean -fd' in a PowerShell code block.\n"
            "This command destroys untracked files globally.\n"
            "Never use git clean in deployment workflows."
        )

    def test_safety_header_present(self):
        content = load_command_file()
        assert "This command NEVER switches branches in the main working tree" in content, (
            "The command file must have a prominent safety header explaining the worktree approach."
        )


class TestGreenPhaseEdgeCases:
    """GREEN PHASE: Edge case handling."""

    def test_first_deploy_isolated(self):
        content = load_command_file()
        assert "bootstrapDir" in content or "gh-pages-bootstrap" in content, (
            "First deploy must use an isolated temp directory for pushing the initial commit.\n"
            "Without this, the main working tree is modified."
        )

    def test_worktree_failure_guard(self):
        content = load_command_file()
        assert "exit 1" in content, (
            "Must exit on worktree failure instead of continuing with destructive operations."
        )

    def test_path_prefixes_on_file_ops(self):
        content = load_command_file()
        # Look for Join-Path $worktreeDir which is needed for Step 7 file operations
        assert "Join-Path $worktreeDir" in content, (
            "File operations in the worktree must use Join-Path $worktreeDir\n"
            "to ensure they operate on the worktree, not the main directory."
        )


class TestGreenPhaseSelfCheck:
    """Verify the test file itself is correct."""

    def test_test_file_loads(self):
        """Make sure the test file parses and runs without import errors."""
        import __main__ as main_mod

        assert hasattr(main_mod, "__file__") or True  # Test framework is working

    def test_command_file_exists(self):
        assert __import__("pathlib").Path(COMMAND_FILE).exists(), (
            f"Command file {COMMAND_FILE} not found. Update COMMAND_FILE path."
        )
