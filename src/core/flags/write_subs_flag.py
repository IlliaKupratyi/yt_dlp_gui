"""
Write subtitle file
"""
from src.core.flags.base_flag import BaseFlag


class WriteSubsFlag(BaseFlag):
    """Class foe write-subs flag"""
    name = "write-subs"
    short_name = ""

    def __init__(self) -> None:
        super().__init__()
