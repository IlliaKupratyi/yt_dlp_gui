from src.core.flags.base_flag import BaseFlag
from src.core.flags.output_paths_flag import OutputPathsFlag

REQUIRED_FLAGS: list[type[BaseFlag]] = [OutputPathsFlag]