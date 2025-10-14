"""
Embed thumbnail in the video as cover art
"""
from src.core.flags.base_flag import BaseFlag

class EmbedThumbnailFlag(BaseFlag):
    """Class foe embed thumbnail flag"""
    name = "embed-thumbnail"
    short_name = ""

    def __init__(self) -> None:
        super().__init__()
