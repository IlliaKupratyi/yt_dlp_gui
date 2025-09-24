from src.core.flags.base import BaseFlag


class WriteThumbnailFlag(BaseFlag):
    name = "write-thumbnail"

    def __init__(self):
        super().__init__()

    def _validate(self) -> None:
        pass

    def to_string(self) -> list[str]:
        return ["--" + self.name]