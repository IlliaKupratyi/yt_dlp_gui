from src.core.flags.base_flag import BaseFlag


class WriteLinkFlag(BaseFlag):
    name = "write-link"
    short_name = ""

    def __init__(self) -> None:
        super().__init__()
