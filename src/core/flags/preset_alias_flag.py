from typing import List

from src.core.exception import FlagValidatorError
from src.core.flags.base import BaseFlag


class PresetAliasFlag(BaseFlag):
    name = "preset-alias"
    short_name = "t"

    def __init__(self, value: str = "mp4"):
        super().__init__(value=value, required=False)
        self.presets = ["mp3", "aac", "mp4", "mkv"]
        self._validate()


    def _validate(self) -> None:
        if self.value not in self.presets:
            raise FlagValidatorError("Invalid preset alias")

    def to_args(self) -> List[str]:
        return ["--" + self.name, self.value]