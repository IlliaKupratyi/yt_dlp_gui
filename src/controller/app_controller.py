import threading
from typing import Optional, Callable
import logging

from src.core.dataclass.subtitle import Subtitles
from src.core.exceptions.exception import YTDLRuntimeError
from src.core.service.flag_processor import FlagProcessor
from src.core.flags.base_flag import BaseFlag
from src.core.flags.format_list_flag import FormatListFlag
from src.core.flags.list_subs_flag import ListSubsFlag
from src.core.service.runner import YTDLPRunner
from src.core.utils.console_output_util import has_error
from src.core.utils.format_util import formats_parse_output
from src.core.utils.subtitles_lister import subtitles_parse_output

logger = logging.getLogger("yt_dlp_gui")

class AppController:
    def __init__(self):
        self.runner = YTDLPRunner()
        self.flag_processor = FlagProcessor()
        self.url: str = ""
        self.subtitles: Optional[Subtitles] = None
        self.formats: list[dict[str, str]] = []
        self.is_running: bool = False
        self.download_thread: Optional[threading.Thread] = None
        logger.info("AppController initialized")

    def setup_video_properties(self, url: str, on_output: Optional[Callable[[str], None]] = None):
        if not url:
            logger.error("AppController error. No url provided")
            raise ValueError('Url cannot be empty')
        self.url = url

        propertiesRunner = YTDLPRunner()

        output_lines: list[str] = []

        def collect_line(line: str) -> None:
            logger.info("YT-DLP. " + line)
            output_lines.append(line)
            if on_output:
                on_output(line)

        logger.info("AppController. Start getting video properties.")

        try:
            propertiesRunner.add_flag([ListSubsFlag(), FormatListFlag()])
            propertiesRunner.run(url, on_output=collect_line)

            if has_error(output_lines):
                error_msg = next(
                    (line for line in output_lines if "ERROR:" in line),
                    "Unknown error occurred"
                )
                logger.error("AppController error. When setup video properties, subprocess error: " + error_msg)
                raise RuntimeError(f"yt-dlp error: {error_msg}")

            self.subtitles = subtitles_parse_output(output_lines)
            self.formats = formats_parse_output(output_lines)

        except Exception as e:
            logger.error("AppController error. When setup video properties, subprocess error: " + str(e))
            self.subtitles = None
            self.formats = []
            raise YTDLRuntimeError(e)

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

    def start_downloading(self,
                          on_output: Optional[Callable[[str], None]] = None,
                          on_complete: Optional[Callable[[dict], None]] = None) -> Optional[threading.Thread]:
        self.runner.add_flag(self.get_flags())

        if self.is_running:
            return None

        def download_task():
            result = None
            try:
                result = self.runner.run(url=self.url, on_output=on_output)
            except Exception as e:
                logger.error("AppController error. When downloading video properties: " + str(e))
                result = {"return_code": -1, "error": str(e)}
            finally:
                self.is_running = False
                if result and on_complete:
                    on_complete(result)

        logger.info("AppController. Start downloading video.")

        self.download_thread = threading.Thread(target=download_task, daemon=True)
        self.download_thread.start()
        return self.download_thread