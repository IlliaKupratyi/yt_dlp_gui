import argparse

from src.core.flags.base import BaseFlag


class SubLangsFlag(BaseFlag):
    name: str = "sub-langs"
    short_name: str = ""

    def __init__(self, languages : list[str]):
        languages_str = ", ".join(languages)
        super().__init__(value=languages_str, required=False)

    def _validate(self) -> None:
        pass

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]