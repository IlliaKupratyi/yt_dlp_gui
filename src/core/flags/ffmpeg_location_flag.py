from src.core.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag
from src.utils.path_validator import validate_absolute_path


class FfmpegLocationFlag(BaseFlag):
    name = "ffmpeg-location"
    short_name = ""

    def __init__(self, value: str = ""):
        super().__init__(value)
        self._validate()

    def _validate(self) -> None:
        try:
            validate_absolute_path(self.value)
        except ValueError:
            raise FlagValidatorError()

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]