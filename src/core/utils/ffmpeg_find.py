import imageio_ffmpeg # type: ignore

from src.core.utils.path_validator import validate_absolute_path

"""Return valid absolute path to ffmpeg executable, or empty string if not found."""
def find_ffmpeg_path() -> str:
    path = imageio_ffmpeg.get_ffmpeg_exe()
    try:
        validate_absolute_path(path)
    except ValueError:
        return ""

    if isinstance(path, str):
        return path

    return ""