from src.core.exception import FlagValidatorError
from src.core.flags.base import BaseFlag


class FormatFlag(BaseFlag):
    name = "format"
    shortname = "f"

    def __init__(self, value: str = "best"):
        super().__init__(value, True)
        self._validate()

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise FlagValidatorError("Format value must be a string")

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]