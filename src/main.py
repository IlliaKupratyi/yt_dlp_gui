from src.core.controller.app_controller import AppController
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
from src.utils.ffmpeg_find import find_ffmpeg_path


def main():
    app_controller = AppController()
    app_controller.setup_video_properties("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    app_controller.add_flag(OutputPathsFlag(DATA_DIR))
    app_controller.add_flag(PresetAliasFlag("mp4"))
    app_controller.add_flag(WriteLinkFlag())
    app_controller.add_flag(WriteSubsFlag())
    app_controller.add_flag(SubLangsFlag(["en, ja"]))
    app_controller.add_flag(NoOverwritesFlag())
    app_controller.add_flag(IgnoreErrorsFlag())
    app_controller.add_flag(ConvertThumbnailsFlag("jpg"))
    app_controller.add_flag(WriteThumbnailFlag())
    app_controller.add_flag(FfmpegLocationFlag(find_ffmpeg_path()))
    app_controller.add_flag(EmbedThumbnailFlag())


    def print_line(line):
        print(f"{line}")

    app_controller.start_downloading(print_line)

if __name__ == '__main__':
    main()
