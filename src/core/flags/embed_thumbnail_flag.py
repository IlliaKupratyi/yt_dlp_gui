from src.core.flags.base_flag import BaseFlag

"""
Embed thumbnail in the video as cover art
"""
class EmbedThumbnailFlag(BaseFlag):
    name = "embed-thumbnail"
    short_name = ""

    def __init__(self) -> None:
        super().__init__()
