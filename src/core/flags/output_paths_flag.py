from typing import List

from src.core.config import DATA_DIR
from src.core.exception import FlagValidatorError
from src.core.flags.base import BaseFlag
from src.utils.path_validator import parse_paths_string

"""Represents yt-dlp's --paths/-P flag for custom download directories."""
class OutputPathsFlag(BaseFlag):
    name = "paths"
    short_name = "P"

    def __init__(self, value: str = DATA_DIR):
        super().__init__(value=value, required=True)

    """Validates the --paths string format using the path parser."""
    def _validate(self) -> None:
        try:
            parse_paths_string(self.value)
        except (ValueError, TypeError) as e:
            raise FlagValidatorError(f"Invalid --paths value: {str(e)}") from e

    """Returns the flag as a CLI argument list: ['--paths', value]."""
    def to_args(self) -> List[str]:
        return ["--" + self.name, self.value]