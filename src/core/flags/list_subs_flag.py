from src.core.flags.base_flag import BaseFlag

"""
List available subtitles of each video
"""
class ListSubsFlag(BaseFlag):
    name = 'list-subs'
    short_name = ''

    def __init__(self) -> None:
        super().__init__()
