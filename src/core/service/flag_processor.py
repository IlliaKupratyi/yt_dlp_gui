"""
A processor that manages and validates command-line flags.
Adds required flags and prevents conflicting flags.
Flags are stored as instances; dependencies are defined as classes.
"""
import logging

from src.core.config.flag_config import REQUIRED_FLAGS
from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag

logger = logging.getLogger("yt_dlp_gui")


class FlagProcessor:
    """Processor class that manages and validates command-line flags."""
    def __init__(self) -> None:
        self.flags: list[BaseFlag] = []
        logger.info("FlagProcessor initialized")

    def add_flag(self, flag : BaseFlag) -> None:
        """Add a flag to the processor, with resolution of dependencies and conflicts."""
        if flag in self.flags:
            return

        for conflict_class in flag.conflicts:
            if any(isinstance(existing, conflict_class) for existing in self.flags):
                logger.info("FlagProcessor. Flag %s already exists",flag.name)
                return

        self._add_required_flags(flag)

        self.flags.append(flag)

        logger.info("FlagProcessor. Flag %s added",flag.name)

    def remove_flag(self, flag : BaseFlag) -> None:
        """Remove a flag and its required flags (if not used elsewhere)."""
        self.flags.remove(flag)

        for required_flag in flag.requires:
            if required_flag() in self.flags:
                self.flags.remove(required_flag())

        self._add_required_flags(flag)
        logger.info("FlagProcessor. Flag %s removed", flag.name)

    def get_flags(self) -> list[BaseFlag]:
        """Return all flags, ensuring that all REQUIRED_FLAGS are included."""
        for required_class in REQUIRED_FLAGS:
            if not any(isinstance(flag, required_class) for flag in self.flags):
                try:
                    self.flags.append(required_class())
                except FlagValidatorError as e:
                    logger.error("FlagProcessor. Error with validating flag %s", str(e))

        return self.flags

    def clear_flags(self) -> None:
        """Clear all flags."""
        logger.info("FlagProcessor. Flags cleared")
        self.flags = []

    def _add_required_flags(self, flag: BaseFlag) -> None:
        """Add missing required flags for the given flag."""
        for required_class in flag.requires:
            if not any(isinstance(existing, required_class) for existing in self.flags):
                self.flags.append(required_class())
                logger.info("FlagProcessor. Required flag %s added", flag.name)
