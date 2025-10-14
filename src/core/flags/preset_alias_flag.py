"""
Applies a predefined set of options
"""
from typing import List

from src.core.config.flag_config import AVAILABLE_PRESETS
from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag


class PresetAliasFlag(BaseFlag):
    """Class foe preset alias"""
    name = "preset-alias"
    short_name = "t"

    def __init__(self, value: str = "mp4"):
        super().__init__(value)
        self._validate()
        from src.core.flags.format_flag import FormatFlag
        self.conflicts = [FormatFlag]

    def _validate(self) -> None:
        if not isinstance(self.value, str) or self.value.upper() not in AVAILABLE_PRESETS:
            raise FlagValidatorError("Error with " + self.name + "Invalid preset alias")

    def to_args(self) -> List[str]:
        return ["--" + self.name, self.value]
