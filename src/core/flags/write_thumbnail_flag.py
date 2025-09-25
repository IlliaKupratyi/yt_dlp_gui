from src.core.flags.base_flag import BaseFlag


class WriteThumbnailFlag(BaseFlag):
    name = "write-thumbnail"

    def __init__(self):
        super().__init__()
