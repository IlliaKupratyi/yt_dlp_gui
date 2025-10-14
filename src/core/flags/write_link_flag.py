"""
Write an internet shortcut file, depending
on the current platform
"""
from src.core.flags.base_flag import BaseFlag


class WriteLinkFlag(BaseFlag):
    """Class foe write-link flag"""
    name = "write-link"
    short_name = ""

    def __init__(self) -> None:
        super().__init__()
