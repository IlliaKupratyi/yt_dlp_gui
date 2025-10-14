"""
List available subtitles of each video
"""
from src.core.flags.base_flag import BaseFlag


class ListSubsFlag(BaseFlag):
    """Class foe list subtitles"""
    name = 'list-subs'
    short_name = ''

    def __init__(self) -> None:
        super().__init__()
