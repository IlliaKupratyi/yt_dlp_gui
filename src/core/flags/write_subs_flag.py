from src.core.flags.base import BaseFlag


class WriteSubsFlag(BaseFlag):
    name = "write-subs"
    short_name = ""

    def __init__(self):
        super().__init__(value = "", required=False)

    def _validate(self) -> None:
        pass