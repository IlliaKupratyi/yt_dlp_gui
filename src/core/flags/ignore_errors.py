from src.core.flags.base import BaseFlag


class IgnoreErrorsFlag(BaseFlag):
    name = "ignore-errors"
    short_name = "i"

    def __init__(self):
        super().__init__()

    def _validate(self) -> None:
        pass