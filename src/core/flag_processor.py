from src.core.config.flag_config import REQUIRED_FLAGS
from src.core.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag

import logging

logger = logging.getLogger("yt_dlp_gui")

"""
A processor that manages and validates command-line flags.
Adds required flags and prevents conflicting flags.
Flags are stored as instances; dependencies are defined as classes.
"""
class FlagProcessor:
    def __init__(self):
        self.flags: list[BaseFlag] = []
        logger.info("FlagProcessor initialized")

    """
    Add a flag to the processor, with resolution of dependencies and conflicts.
    """
    def add_flag(self, flag : BaseFlag):
        if flag in self.flags:
            return

        for conflict_class in flag.conflicts:
            if any(isinstance(existing, conflict_class) for existing in self.flags):
                logger.info("FlagProcessor. Flag " + flag.name + " already exists")
                return

        self._add_required_flags(flag)

        self.flags.append(flag)

        logger.info("FlagProcessor. Flag " + flag.name + " added")

    def remove_flag(self, flag : BaseFlag):
        self.flags.remove(flag)

        for required_flag in flag.requires:
            if required_flag() in self.flags:
                self.flags.remove(required_flag())

        self._add_required_flags(flag)
        logger.info("FlagProcessor. Flag " + flag.name + " removed")

    """
    Return all flags, ensuring that all REQUIRED_FLAGS are included.
    """
    def get_flags(self) -> list[BaseFlag]:
        for required_class in REQUIRED_FLAGS:
            if not any(isinstance(flag, required_class) for flag in self.flags):
                try:
                    self.flags.append(required_class())
                except FlagValidatorError as e:
                    logger.error("FlagProcessor. Error with validating flag" + str(e))

        return self.flags

    def clear_flags(self):
        logger.info("FlagProcessor. Flags cleared")
        self.flags = []

    def _add_required_flags(self, flag: BaseFlag):
        for required_class in flag.requires:
            if not any(isinstance(existing, required_class) for existing in self.flags):
                self.flags.append(required_class())
                logger.info("FlagProcessor. Required flag " + flag.name + " added")