from src.core.flags.base_flag import BaseFlag

class FormatListFlag(BaseFlag):
    name = "list-formats"
    short_name = "F"

    def __init__(self):
        super().__init__()
