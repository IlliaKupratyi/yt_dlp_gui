import sys
from pathlib import Path

WINDOWS_INVALID_CHARS_IN_NAME = set('<>|:*?"\0')


def is_valid_path_type(path_type: str) -> bool:
    if not path_type:
        return False

    if not isinstance(path_type, str):
        return False

    if path_type in ("home", "temp"):
        return True
    return all(c not in WINDOWS_INVALID_CHARS_IN_NAME for c in path_type)


def validate_path(path: str, allow_empty: bool = False) -> str:
    if not isinstance(path, str):
        raise TypeError(f"Path must be str, got {type(path).__name__}")

    if not allow_empty and not path.strip():
        raise ValueError("Path cannot be empty or whitespace")

    path = path.strip()

    try:
        p = Path(path)
    except Exception:
        raise ValueError(f"Invalid path format: '{path}'")

    if "\0" in path:
        raise ValueError("Path cannot contain null byte (\\0)")

    if sys.platform == "win32":
        drive = p.drive
        if drive:
            if len(drive) != 2 or not drive[0].isalpha() or drive[1] != ":":
                raise ValueError(f"Invalid drive format: '{drive}'. Expected 'X:' (e.g., 'C:')")

            if not drive[0].isascii():
                raise ValueError(f"Drive letter must be ASCII: '{drive[0]}'")

    components = []
    if p.drive:
        components.append(p.drive)
    components.extend(p.parts[1:] if sys.platform == "win32" else p.parts)

    for component in components:
        if not component:
            continue

        if sys.platform == "win32":
            if ":" in component and component != p.drive:
                raise ValueError(
                    f"Colon ':' not allowed in path component: '{component}' (only allowed in drive like 'C:')")

            if component != p.drive:
                for char in component:
                    if char in WINDOWS_INVALID_CHARS_IN_NAME:
                        raise ValueError(f"Invalid character '{char}' in path component: '{component}'")

        if not component:
            raise ValueError("Path component cannot be empty")

    if sys.platform == "win32" and len(str(p)) > 260:
        raise ValueError(f"Path exceeds Windows MAX_PATH limit (260 chars): {len(str(p))} chars")

    if sys.platform == "win32" and (path.endswith(" ") or path.endswith(".")):
        raise ValueError("Path cannot end with space or period on Windows")

    return str(p).replace("\\", "/")


def parse_paths_string(paths_str: str) -> list[tuple[str, str]]:
    if not isinstance(paths_str, str):
        raise TypeError("paths_str must be a string")

    pairs = [p.strip() for p in paths_str.split(",") if p.strip()]
    if not pairs:
        raise ValueError("No valid path entries found")

    result = []
    for pair in pairs:
        if ":" not in pair:
            raise ValueError(f"Invalid path entry: '{pair}'. Expected format: TYPE:PATH")

        type_part, path_part = pair.split(":", 1)

        if not is_valid_path_type(type_part):
            raise ValueError(
                f"Invalid path type: '{type_part}'. Must be 'home', 'temp', or alphanumeric without : * ? \" < > |")

        validate_path(path_part)

        result.append((type_part, path_part))

    return result


def resolve_home_path(base_dir: str) -> str:
    if not base_dir:
        raise ValueError("Base directory cannot be empty")

    validated_base = validate_path(base_dir)

    path = Path(validated_base)
    path.mkdir(parents=True, exist_ok=True)

    return str(path.resolve())