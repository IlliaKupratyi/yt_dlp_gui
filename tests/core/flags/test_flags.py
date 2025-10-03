from unittest.mock import patch

import pytest

from src.core.exceptions.exception import FlagValidatorError
from src.core.flags.convert_thumbnails_flag import ConvertThumbnailsFlag
from src.core.flags.ffmpeg_location_flag import FfmpegLocationFlag
from src.core.flags.format_flag import FormatFlag
from src.core.flags.output_paths_flag import OutputPathsFlag
from src.core.flags.preset_alias_flag import PresetAliasFlag
from src.core.flags.print_flag import PrintFlag
from src.core.flags.sub_langs_flag import SubLangsFlag
from src.core.flags.write_subs_flag import WriteSubsFlag
from src.core.flags.write_thumbnail_flag import WriteThumbnailFlag


def test_convert_thumbnails_flag_valid():
    flag = ConvertThumbnailsFlag("png")
    assert flag.to_args() == ["--convert-thumbnails", "png"]

def test_convert_thumbnails_flag_invalid():
    with pytest.raises(FlagValidatorError):
        ConvertThumbnailsFlag("bmp")

def test_convert_thumbnails_flag_default():
    flag = ConvertThumbnailsFlag()
    assert flag.value == "webp"
    assert flag.to_args() == ["--convert-thumbnails", "webp"]

def test_convert_thumbnails_requires_write_thumbnail():
    flag = ConvertThumbnailsFlag()
    assert WriteThumbnailFlag in flag.requires

# Mock config values
MOCK_PRESETS = {"MP4", "MP3", "AAC"}
MOCK_PRINT_VALUES = {"title", "thumbnail", "id"}


# === FfmpegLocationFlag ===

def test_ffmpeg_location_valid():
    with patch("src.core.flags.ffmpeg_location_flag.validate_absolute_path"):
        flag = FfmpegLocationFlag("/usr/bin/ffmpeg")
        assert flag.to_args() == ["--ffmpeg-location", "/usr/bin/ffmpeg"]

def test_ffmpeg_location_invalid():
    with patch("src.core.flags.ffmpeg_location_flag.validate_absolute_path", side_effect=ValueError):
        with pytest.raises(FlagValidatorError):
            FfmpegLocationFlag("/invalid/path")


# === FormatFlag ===

def test_format_flag_valid():
    flag = FormatFlag("bestvideo+bestaudio")
    assert flag.to_args() == ["--format", "bestvideo+bestaudio"]

def test_format_flag_invalid_type():
    with pytest.raises(FlagValidatorError):
        FormatFlag(123)  # type: ignore


# === OutputPathsFlag ===

def test_output_paths_valid():
    with patch("src.core.flags.output_paths_flag.validate_absolute_path"):
        flag = OutputPathsFlag("/downloads")
        assert flag.to_args() == ["--paths", "/downloads"]

def test_output_paths_invalid():
    with patch("src.core.flags.output_paths_flag.validate_absolute_path", side_effect=ValueError):
        with pytest.raises(FlagValidatorError):
            OutputPathsFlag("/nonexistent")


# === PresetAliasFlag ===

@patch("src.core.flags.preset_alias_flag.AVAILABLE_PRESETS", MOCK_PRESETS)
def test_preset_alias_valid():
    flag = PresetAliasFlag("mp4")
    assert flag.to_args() == ["--preset-alias", "mp4"]
    assert flag.conflicts == [FormatFlag]

@patch("src.core.flags.preset_alias_flag.AVAILABLE_PRESETS", MOCK_PRESETS)
def test_preset_alias_invalid():
    with pytest.raises(FlagValidatorError):
        PresetAliasFlag("invalid")


# === PrintFlag ===

@patch("src.core.flags.print_flag.AVAILABLE_PRINT_VALUES", MOCK_PRINT_VALUES)
def test_print_flag_valid():
    flag = PrintFlag("title")
    assert flag.to_args() == ["--print", "title"]

@patch("src.core.flags.print_flag.AVAILABLE_PRINT_VALUES", MOCK_PRINT_VALUES)
def test_print_flag_invalid():
    with pytest.raises(FlagValidatorError):
        PrintFlag("invalid")


# === SubLangsFlag ===

def test_sub_langs_flag():
    flag = SubLangsFlag(["en", "ru"])
    assert flag.to_args() == ["--sub-langs", "en, ru"]
    assert WriteSubsFlag in flag.requires

def test_sub_langs_empty():
    flag = SubLangsFlag([])
    assert flag.to_args() == ["--sub-langs", ""]


# === Edge: validation called on init ===

def test_validation_called_on_init():
    with patch("src.core.flags.ffmpeg_location_flag.validate_absolute_path", side_effect=ValueError):
        with pytest.raises(FlagValidatorError):
            FfmpegLocationFlag("any")