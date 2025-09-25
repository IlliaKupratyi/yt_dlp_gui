from src.core.flags.base import BaseFlag


class EmbedThumbnailFlag(BaseFlag):
    name = "embed-thumbnail"
    short_name = ""

    def __init__(self):
        super().__init__()

    def _validate(self) -> None:
        pass
