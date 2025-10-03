from src.core.flags.base_flag import BaseFlag

"""
Do not overwrite any files
"""
class NoOverwritesFlag(BaseFlag):
    name = "no-overwrites"
    short_name = "w"

    def __init__(self) -> None:
        super().__init__()
