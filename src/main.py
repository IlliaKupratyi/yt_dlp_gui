from src.core.flag_processor import FlagProcessor
from src.core.config.config import DATA_DIR
from src.core.flags.convert_thumbnails_flag import ConvertThumbnailsFlag
from src.core.flags.embed_thumbnail_flag import EmbedThumbnailFlag

from src.core.flags.ffmpeg_location_flag import FfmpegLocationFlag
from src.core.flags.ignore_errors_flag import IgnoreErrorsFlag
from src.core.flags.no_overwrites_flag import NoOverwritesFlag
from src.core.flags.output_paths_flag import OutputPathsFlag
from src.core.flags.preset_alias_flag import PresetAliasFlag
from src.core.flags.sub_langs_flag import SubLangsFlag
from src.core.flags.write_link_flag import WriteLinkFlag
from src.core.flags.write_subs_flag import WriteSubsFlag
from src.core.flags.write_thumbnail_flag import WriteThumbnailFlag
from src.core.runner import YTDLPRunner
from src.utils.ffmpeg_find import find_ffmpeg_path


def main():
    flag_processor = FlagProcessor()
    runner = YTDLPRunner()

    flag_processor.add_flag(OutputPathsFlag(DATA_DIR))
    flag_processor.add_flag(PresetAliasFlag("mp4"))
    flag_processor.add_flag(WriteLinkFlag())
    flag_processor.add_flag(WriteSubsFlag())
    flag_processor.add_flag(SubLangsFlag(["en, ja"]))
    flag_processor.add_flag(NoOverwritesFlag())
    flag_processor.add_flag(IgnoreErrorsFlag())
    flag_processor.add_flag(ConvertThumbnailsFlag("jpg"))
    flag_processor.add_flag(WriteThumbnailFlag())
    flag_processor.add_flag(FfmpegLocationFlag(find_ffmpeg_path()))
    flag_processor.add_flag(EmbedThumbnailFlag())

    runner.add_flag(flag_processor.get_flags())

    def print_line(line):
        print(f"{line}")

    result = runner.run(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
               on_output=print_line)

    print(f"Finished with code {result['return_code']}")

if __name__ == '__main__':
    main()
