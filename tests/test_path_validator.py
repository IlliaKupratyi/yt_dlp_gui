import sys

from src.core.utils.path_validator import validate_absolute_path

def test_path_validator() -> None:
    if sys.platform == 'win32':
        _test_windows_path_validator()
    else:
        _test_linux_path_validator()

def _test_windows_path_validator() -> None:
    validate_absolute_path(r"C:\Users\John\file.txt")
    validate_absolute_path("C:/Users/John/file.txt")
    validate_absolute_path("C:/Users/John")
    try:
        validate_absolute_path(r"C:\file?.txt")  # ? invalid
    except ValueError:
        pass
    try:
        validate_absolute_path(r"C:\CON")  # reserved name
    except ValueError:
        pass
    try:
        validate_absolute_path(r"C:\folder.")  # ends with .
    except ValueError:
        pass

def _test_linux_path_validator() -> None:
    validate_absolute_path("/home/user/file.txt")
    validate_absolute_path("/tmp/a*b?")
    try:
        validate_absolute_path("/home/user/file\0.txt")  # null byte
    except ValueError:
        pass
