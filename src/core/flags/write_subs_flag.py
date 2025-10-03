from src.core.flags.base_flag import BaseFlag

"""
Write subtitle file
"""
class WriteSubsFlag(BaseFlag):
    name = "write-subs"
    short_name = ""

    def __init__(self) -> None:
        super().__init__()
