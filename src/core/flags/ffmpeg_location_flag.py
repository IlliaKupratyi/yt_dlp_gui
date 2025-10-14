"""
Location of the ffmpeg binary; either the path to the binary or its containing directory
"""
from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag
from src.core.utils.path_validator import validate_absolute_path


class FfmpegLocationFlag(BaseFlag):
    """Class foe ffmpeg location flag"""
    name = "ffmpeg-location"
    short_name = ""

    def __init__(self, value: str = ""):
        super().__init__(value)
        self._validate()

    def _validate(self) -> None:
        try:
            validate_absolute_path(self.value)
        except ValueError as e:
            raise FlagValidatorError("Error with " + self.name + ". Invalid path.") from e

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]
