"""
Do not overwrite any files
"""
from src.core.flags.base_flag import BaseFlag


class NoOverwritesFlag(BaseFlag):
    """Class foe no overwrite flag"""
    name = "no-overwrites"
    short_name = "w"

    def __init__(self) -> None:
        super().__init__()
