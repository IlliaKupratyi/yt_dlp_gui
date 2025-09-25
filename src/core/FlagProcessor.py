from src.core.config.flag_config import REQUIRED_FLAGS
from src.core.flags.base_flag import BaseFlag

class FlagProcessor:

    def __init__(self):
        self.flags: list[BaseFlag] = []

    def add_flag(self, flag : BaseFlag):
        if flag in self.flags:
            return

        for conflict in flag.conflicts:
            if conflict.name == flag.name:
                return

        for require in flag.requires:
            if require not in self.flags:
                self.flags.append(require())

        self.flags.append(flag)

    def get_flags(self) -> list[BaseFlag]:
        for flag in REQUIRED_FLAGS:
            if flag in self.flags:
                self.flags.append(flag())

        return self.flags