from abc import ABC
from typing import Optional, Any

from src.core.exceptions.exception import FlagValidatorError

"""
An abstract base class for all flags
"""
class BaseFlag(ABC):
    name: str = "" # flag name
    short_name: Optional[str] = "" # flag shor name
    deprecated: bool = False # is the flag obsolete
    requires: list[type['BaseFlag']] = []
    conflicts: list[type['BaseFlag']] = []

    def __init__(self, value: Any = None):
        self.value = value

    """Validating the flag value. Called during initialization"""
    def _validate(self) -> None:
        pass

    """Formatting into CLI arguments"""
    def to_args(self) -> list[str]:
        return ["--" + self.name]

    """Checks that the flag is valid (does not throw exceptions)"""
    def is_valid(self) -> bool:
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

    """Creates a copy of the flag"""
    def clone(self) -> "BaseFlag":
        return self.__class__(self.value)