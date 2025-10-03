from src.core.config.flag_config import AVAILABLE_PRINT_VALUES
from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag


class PrintFlag(BaseFlag):
    name: str = "print"
    short_name = "O"

    def __init__(self, value: str):
        super().__init__(value)

    def _validate(self) -> None:
        if not self.value or not isinstance(self.value, str) or self.value not in AVAILABLE_PRINT_VALUES:
            raise FlagValidatorError("Error with " + self.name + ". Wrong value")

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]