from src.core.flags.base import BaseFlag


class ListSubsFlag(BaseFlag):
    name = 'list-subs'
    short_name = ''

    def __init__(self):
        super().__init__()

    def _validate(self) -> None:
        pass