from src.core.exception import FlagValidatorError
from src.core.flags.base import BaseFlag


class ConvertThumbnailsFlag(BaseFlag):
    name = "convert-thumbnails"
    supported_formats = ["png", "jpg", "webp"]

    def __init__(self, value: str = "webp"):
        super().__init__(value, False)

    def _validate(self) -> None:
        if self.value not in self.supported_formats:
            raise FlagValidatorError("Not supported format for thumbnail conversion!")

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]
