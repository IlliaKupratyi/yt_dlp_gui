"""
Represents yt-dlp's --paths/-P flag for custom download directories.
"""
from src.core.config.config import DATA_DIR
from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag
from src.core.utils.path_validator import validate_absolute_path

class OutputPathsFlag(BaseFlag):
    """Class foe output paths"""
    name = "paths"
    short_name = "P"

    def __init__(self, value: str = DATA_DIR):
        super().__init__(value)
        self._validate()

    def _validate(self) -> None:
        """Validates the --paths string format using the path parser."""
        try:
            validate_absolute_path(self.value)
        except (ValueError, TypeError) as e:
            raise FlagValidatorError("Error with " + self.name + "Invalid --paths value: " + str(e)) from e

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]
