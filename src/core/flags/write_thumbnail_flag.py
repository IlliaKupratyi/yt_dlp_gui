from src.core.flags.base_flag import BaseFlag

"""
Write thumbnail image to disk
"""
class WriteThumbnailFlag(BaseFlag):
    name = "write-thumbnail"

    def __init__(self) -> None:
        super().__init__()
