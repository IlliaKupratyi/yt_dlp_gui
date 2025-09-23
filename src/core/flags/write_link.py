from src.core.flags.base import BaseFlag


class WriteLinkFlag(BaseFlag):
    name = "write-link"
    short_name = ""

    def __init__(self) -> None:
        super().__init__()

    def _validate(self) -> None:
        pass