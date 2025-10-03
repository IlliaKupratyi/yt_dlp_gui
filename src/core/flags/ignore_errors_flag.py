from src.core.flags.base_flag import BaseFlag


class IgnoreErrorsFlag(BaseFlag):
    name = "ignore-errors"
    short_name = "i"

    def __init__(self) -> None:
        super().__init__()
