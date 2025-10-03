from src.core.flags.base_flag import BaseFlag

"""
Ignore download and postprocessing errors.
The download will be considered successful
even if the postprocessing fails
"""
class IgnoreErrorsFlag(BaseFlag):
    name = "ignore-errors"
    short_name = "i"

    def __init__(self) -> None:
        super().__init__()
