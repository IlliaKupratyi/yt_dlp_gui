import imageio_ffmpeg # type: ignore

from src.utils.path_validator import validate_absolute_path


def find_ffmpeg_path() -> str:
    path = imageio_ffmpeg.get_ffmpeg_exe()
    try:
        validate_absolute_path(path)
    except ValueError:
        return ""
    return path