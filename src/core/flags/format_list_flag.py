from src.core.flags.base_flag import BaseFlag

"""
List available formats of each video
"""
class FormatListFlag(BaseFlag):
    name = "list-formats"
    short_name = "F"

    def __init__(self) -> None:
        super().__init__()
