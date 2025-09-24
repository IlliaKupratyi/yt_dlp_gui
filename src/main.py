from src.core.config import DATA_DIR
from src.core.flags.convert_thumbnails import ConvertThumbnailsFlag
from src.core.flags.ffmpeg_location_flag import FfmpegLocationFlag
from src.core.flags.format_flag import FormatFlag
from src.core.flags.ignore_errors import IgnoreErrorsFlag
from src.core.flags.no_overwrites_flag import NoOverwritesFlag
from src.core.flags.output_paths_flag import OutputPathsFlag
from src.core.flags.preset_alias_flag import PresetAliasFlag
from src.core.flags.sub_langs_flag import SubLangsFlag
from src.core.flags.write_link import WriteLinkFlag
from src.core.flags.write_subs_flag import WriteSubsFlag
from src.core.flags.write_thumbnail import WriteThumbnailFlag
from src.core.runner import YTDLPRunner
from src.utils.ffmpeg_find import find_ffmpeg_path


def main():
    runner = YTDLPRunner()
    runner.add_flag(PresetAliasFlag("mp4"))
    runner.add_flag(FormatFlag("best"))
    runner.add_flag(OutputPathsFlag(DATA_DIR))
    runner.add_flag(WriteLinkFlag())
    runner.add_flag(WriteSubsFlag())
    runner.add_flag(SubLangsFlag(["en", "ja"]))
    runner.add_flag(NoOverwritesFlag())
    runner.add_flag(IgnoreErrorsFlag())
    runner.add_flag(ConvertThumbnailsFlag("jpg"))
    runner.add_flag(WriteThumbnailFlag())
    runner.add_flag(FfmpegLocationFlag(find_ffmpeg_path()))

    def print_line(line):
        print(f"{line}")

    result = runner.run(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
               on_output=print_line)

    print(f"Finished with code {result['return_code']}")

if __name__ == '__main__':
    main()
