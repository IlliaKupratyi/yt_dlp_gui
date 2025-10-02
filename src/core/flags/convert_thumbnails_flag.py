from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag


class ConvertThumbnailsFlag(BaseFlag):
    name = "convert-thumbnails"
    supported_formats = ["png", "jpg", "webp"]

    def __init__(self, value: str = "webp"):
        super().__init__(value)

        from src.core.flags.write_thumbnail_flag import WriteThumbnailFlag
        self.requires = [WriteThumbnailFlag]

        self._validate()

    def _validate(self) -> None:
        if not isinstance(self.value, str) or self.value not in self.supported_formats:
            raise FlagValidatorError("Error with " + self.name + "Not supported format for thumbnail conversion!")

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]