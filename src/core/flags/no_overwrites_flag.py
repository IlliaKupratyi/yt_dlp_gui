from src.core.flags.base_flag import BaseFlag


class NoOverwritesFlag(BaseFlag):
    name = "no-overwrites"
    short_name = "w"

    def __init__(self):
        super().__init__()
