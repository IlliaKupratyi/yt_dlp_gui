from src.core.flags.base import BaseFlag

class FormatListFlag(BaseFlag):
    name = "list-formats"
    short_name = "F"

    def __init__(self):
        super().__init__(value="", required=False)

    def _validate(self) -> None:
        pass