import sys
import os
from pathlib import Path

def validate_absolute_path(path: str) -> str:
    """
    Validates that the given string is a syntactically correct absolute path
    for the current operating system.
    """
    if not isinstance(path, str):
        raise TypeError(f"Path must be a string, got {type(path).__name__}")

    if not path.strip():
        raise ValueError("Path cannot be empty or whitespace-only")

    path = path.strip()

    if "\0" in path:
        raise ValueError("Path cannot contain null byte (\\0)")

    try:
        p = Path(path)
    except Exception as e:
        raise ValueError(f"Invalid path syntax: {e}") from e

    if not p.is_absolute():
        raise ValueError(f"Path must be absolute: '{path}'")

    if sys.platform == "win32":
        _validate_windows_path_components(p)
    else:
        _validate_posix_path_components(p)

    try:
        normalized = os.path.normpath(path)
    except Exception as e:
        raise ValueError(f"Failed to normalize path: {e}") from e

    return normalized


def _validate_windows_path_components(p: Path) -> None:
    parts = p.parts
    if p.drive:
        name_parts = parts[1:]
    else:
        name_parts = parts

    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10))
    }

    invalid_chars = set('<>:"|?*')

    for part in name_parts:
        if not part:
            continue

        for char in part:
            if char in invalid_chars:
                raise ValueError(f"Invalid character '{char}' in path component: '{part}'")

        if part.upper() in reserved_names:
            raise ValueError(f"Reserved name not allowed on Windows: '{part}'")

        if part.endswith(' ') or part.endswith('.'):
            raise ValueError(f"Path component cannot end with space or period on Windows: '{part}'")


def _validate_posix_path_components(p: Path) -> None:
    for part in p.parts:
        if not part:
            continue
        if '\0' in part:
            raise ValueError(f"Null byte in path component: '{part}'")