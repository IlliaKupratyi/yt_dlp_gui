from src.core.flags.base_flag import BaseFlag

"""
Write an internet shortcut file, depending
on the current platform
"""
class WriteLinkFlag(BaseFlag):
    name = "write-link"
    short_name = ""

    def __init__(self) -> None:
        super().__init__()
