from src.core.flags.base_flag import BaseFlag


class EmbedThumbnailFlag(BaseFlag):
    name = "embed-thumbnail"
    short_name = ""

    def __init__(self):
        super().__init__()
