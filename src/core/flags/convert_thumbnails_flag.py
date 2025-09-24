from src.core.flags.base import BaseFlag


class ConvertThumbnailsFlag(BaseFlag):
    name = "convert-thumbnails"

    def __init__(self, value: str = "webp"):
        super().__init__(value, False)

    def _validate(self) -> None:
        pass

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]
