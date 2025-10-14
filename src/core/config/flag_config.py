"""
Flag config
"""
from src.core.flags.base_flag import BaseFlag
from src.core.flags.output_paths_flag import OutputPathsFlag

REQUIRED_FLAGS: list[type[BaseFlag]] = [OutputPathsFlag] # Flags, which must be in cmd
AVAILABLE_PRINT_VALUES=["id", "title"]
AVAILABLE_THUMBNAILS_FORMATS=["jpg", "png", "webp"]
AVAILABLE_PRESETS=["MP3", "AAC", "MP4", "MKV"]
