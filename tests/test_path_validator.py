import sys
import os

from src.utils.path_validator import is_valid_path_type, validate_path, parse_paths_string, resolve_home_path


def test_is_valid_path_type():
    assert is_valid_path_type("home")
    assert is_valid_path_type("temp")
    assert is_valid_path_type("audio")
    assert is_valid_path_type("my_video_2025")
    assert not is_valid_path_type("video?")  # ? restricted
    assert not is_valid_path_type("")  # empty
    assert not is_valid_path_type(123)   # not string


def test_validate_path_valid():
    if sys.platform == "win32":
        validate_path("C:\\Users\\user")  # Windows
        validate_path("data/video")
    else:
        validate_path("/home/user")  # Linux
        validate_path("my folder")


def test_validate_path_invalid_windows():
    if sys.platform == "win32":
        try:
            validate_path("C:\\temp\\file?name.mp4")
            assert False, "Should raise ValueError"
        except ValueError:
            pass

        try:
            validate_path("C:/invalid|name")
            assert False, "Should raise ValueError"
        except ValueError:
            pass


def test_parse_paths_string():
    result = parse_paths_string("home:/,temp:/tmp,audio:/music")
    assert result == [('home', '/'), ('temp', '/tmp'), ('audio', '/music')]

    try:
        parse_paths_string("audio:")
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        parse_paths_string("video?/path")
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_resolve_home_path():
    base = "data"
    resolved = resolve_home_path(base)
    assert os.path.isabs(resolved)
    assert os.path.exists(resolved)