"""
Languages of the subtitles to download
"""
from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.base_flag import BaseFlag


class SubLangsFlag(BaseFlag):
    """Class foe sub langs flag"""
    name: str = "sub-langs"
    short_name: str = ""

    def __init__(self, languages : list[str]):
        languages_str = ", ".join(languages)
        super().__init__(languages_str)

        from src.core.flags.write_subs_flag import WriteSubsFlag
        self.requires = [WriteSubsFlag]

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise FlagValidatorError("Error with " + self.name + "Sub languages must be a string")

    def to_args(self) -> list[str]:
        return ["--" + self.name, self.value]
