from typing import List

from src.core.exception import FlagValidatorError
from src.core.flags.base import BaseFlag
from src.utils.path_validator import parse_paths_string


class OutputPathsFlag(BaseFlag):
    name = "paths"
    short_name = "P"

    def __init__(self, value: str = "~"):
        super().__init__(value=value, required=True)

    def _validate(self) -> None:
        try:
            parse_paths_string(self.value)
        except (ValueError, TypeError) as e:
            raise FlagValidatorError(f"Invalid --paths value: {str(e)}") from e

    def to_args(self) -> List[str]:
        pass