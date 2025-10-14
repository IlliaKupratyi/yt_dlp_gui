"""
An abstract base class for all flags
"""
from abc import ABC
from typing import Optional, Any

from src.core.exceptions.exception import FlagValidatorError

class BaseFlag(ABC):
    """
    An abstract base class for all flags
    """
    name: str = "" # flag name
    short_name: Optional[str] = "" # flag shor name
    deprecated: bool = False # is the flag obsolete
    requires: list[type['BaseFlag']] = []
    conflicts: list[type['BaseFlag']] = []

    def __init__(self, value: Any = None):
        self.value = value

    def _validate(self) -> None:
        """Validating the flag value. Called during initialization"""

    def to_args(self) -> list[str]:
        """Formatting into CLI arguments"""
        return ["--" + self.name]

    def is_valid(self) -> bool:
        """Checks that the flag is valid (does not throw exceptions)"""
        try:
            self._validate()
            return True
        except FlagValidatorError:
            return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_args()})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return bool(self.value == other.value)

    def clone(self) -> "BaseFlag":
        """Creates a copy of the flag"""
        return self.__class__(self.value)
