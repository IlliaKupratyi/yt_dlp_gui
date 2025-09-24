from abc import ABC, abstractmethod
from typing import Optional, Any

"""
An abstract base class for all flags
Each flag is responsible for:
- its own validation
- formatting into CLI arguments
- compatibility with other flags
"""

class BaseFlag(ABC):
    name: str = "" # flag name
    short_name: Optional[str] = "" # flag shor name
    required: bool = False # is this flag mandatory
    deprecated: bool = False # is the flag obsolete

    def __init__(self, value: Any = None, required: bool = False):
        self.value = value
        self.required = required

    """Validating the flag value. Called during initialization"""
    @abstractmethod
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
        except Exception:
            return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_args()})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

    """Creates a copy of the flag"""
    def clone(self):
        return self.__class__(self.value, self.required)