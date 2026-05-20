"""
Pytest configuration for slide structure tests.

Supports --html CLI argument to target a specific slideshow HTML file.
Without --html, tests auto-detect the most recently modified slideshow.
"""


def pytest_addoption(parser):
    parser.addoption(
        "--slideshow-html",
        action="store",
        default=None,
        help="Path to a specific slideshow index.html (overrides auto-detect)",
    )


def pytest_configure(config):
    """Inject the --slideshow-html value into the test module before test collection."""
    val = config.getoption("--slideshow-html", default=None)
    if val:
        import test_slide_structure as tss

        tss._CLI_HTML_OVERRIDE = val
