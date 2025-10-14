"""
Video format code
"""
from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag


class FormatFlag(BaseFlag):
    """Class foe format flag"""
    name = "format"
    shortname = "f"

    def __init__(self, value: str = "best"):
        super().__init__(value)

        from src.core.flags.preset_alias_flag import PresetAliasFlag
        self.conflicts = [PresetAliasFlag]

        self._validate()

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise FlagValidatorError("Error with " + self.name + "Format value must be a string")

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]
