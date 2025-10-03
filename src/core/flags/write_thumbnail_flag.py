from src.core.flags.base_flag import BaseFlag


class WriteThumbnailFlag(BaseFlag):
    name = "write-thumbnail"

    def __init__(self) -> None:
        super().__init__()
