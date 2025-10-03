from src.core.utils.console_output_util import has_error


def test_has_error_detects_error():
    lines = ["Downloading...", "ERROR: Invalid URL"]
    assert has_error(lines) is True

def test_has_error_no_error():
    lines = ["Downloading...", "100% complete"]
    assert has_error(lines) is False

def test_has_error_empty_input():
    assert has_error([]) is False