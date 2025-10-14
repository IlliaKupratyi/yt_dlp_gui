"""
Write thumbnail image to disk
"""
from src.core.flags.base_flag import BaseFlag


class WriteThumbnailFlag(BaseFlag):
    """Class for write-thumbnail flag"""
    name = "write-thumbnail"

    def __init__(self) -> None:
        super().__init__()
