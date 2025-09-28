from typing import Optional, Callable

from src.core.dataclass.subtitle import Subtitles
from src.core.flag_processor import FlagProcessor
from src.core.flags.base_flag import BaseFlag
from src.core.flags.format_list_flag import FormatListFlag
from src.core.flags.list_subs_flag import ListSubsFlag
from src.core.runner import YTDLPRunner
from src.utils.format_lister import formats_parse_output
from src.utils.subtitles_lister import subtitles_parse_output


class AppController:
    def __init__(self):
        self.runner = YTDLPRunner()
        self.flag_processor = FlagProcessor()
        self.url: str = ""
        self.subtitles: Optional[Subtitles] = None
        self.formats: list[dict[str, str]] = []

    def setup_video_properties(self, url: str):
        if not url:
            raise ValueError('Url cannot be empty')
        self.url = url

        propertiesRunner = YTDLPRunner()

        output_lines: list[str] = []

        def collect_line(line: str) -> None:
            output_lines.append(line)

        propertiesRunner.add_flag([ListSubsFlag(), FormatListFlag()])
        result = propertiesRunner.run(url, on_output=collect_line)

        if result['return_code'] != 0:
            raise RuntimeError(f"yt-dlp failed: {' '.join(result['stderr'])}")

        self.subtitles = subtitles_parse_output(output_lines)
        self.formats = formats_parse_output(output_lines)

    def get_subtitles(self) -> Subtitles:
        return self.subtitles

    def get_formats(self) -> list[dict[str, str]]:
        return self.formats

    def add_flag(self, flag: BaseFlag):
        self.flag_processor.add_flag(flag)

    def remove_flag(self, flag: BaseFlag):
        self.flag_processor.remove_flag(flag)

    def clear_flags(self):
        self.flag_processor.clear_flags()

    def get_flags(self):
        return self.flag_processor.get_flags()

    def start_downloading(self, on_output: Optional[Callable[[str], None]] = None) -> dict[str, str]:
        self.runner.add_flag(self.get_flags())
        result = self.runner.run(url=self.url, on_output=on_output)
        return result