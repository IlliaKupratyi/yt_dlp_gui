from src.core.flags.base import BaseFlag


class NoOverwritesFlag(BaseFlag):
    name = "no-overwrites"
    short_name = "w"

    def __init__(self):
        super().__init__()

    def _validate(self) -> None:
        pass