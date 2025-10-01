from typing import List

from src.core.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag


class PresetAliasFlag(BaseFlag):
    name = "preset-alias"
    short_name = "t"
    presets = ["mp3", "aac", "mp4", "mkv"]

    def __init__(self, value: str = "mp4"):
        super().__init__(value)
        self._validate()
        from src.core.flags.format_flag import FormatFlag
        self.conflicts = [FormatFlag]

    def _validate(self) -> None:
        if not isinstance(self.value, str) or self.value not in self.presets:
            print(self.value)
            raise FlagValidatorError("Invalid preset alias")

    def to_args(self) -> List[str]:
        return ["--" + self.name, self.value]