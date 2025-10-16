"""App Controller. Connect view and logic"""
import subprocess
import threading
from io import BytesIO
from typing import Optional, Callable
import logging
import requests
from PIL import Image
from PIL.ImageFile import ImageFile
from urllib3.exceptions import RequestError

from src.clients.youtube_client import YouTubeClient
from src.core.dataclass.subtitle import Subtitles
from src.core.dataclass.youtube_video import YouTubeVideo
from src.core.exceptions.exception import YTDLRuntimeError
from src.core.service.flag_processor import FlagProcessor
from src.core.flags.base_flag import BaseFlag
from src.core.flags.format_list_flag import FormatListFlag
from src.core.flags.list_subs_flag import ListSubsFlag
from src.core.service.runner import YTDLPRunner
from src.core.utils.console_output_util import has_error
from src.core.utils.format_util import formats_parse_output, format_duration
from src.core.utils.link_parser import extract_youtube_id
from src.core.utils.subtitles_lister import subtitles_parse_output

logger = logging.getLogger("yt_dlp_gui")

class AppController:
    """Coordinates video metadata fetching, flag management, and downloading"""
    def __init__(self, api_token: str) -> None:
        self.runner = YTDLPRunner()
        self.flag_processor = FlagProcessor()
        self.url: str = ""
        self.is_running: bool = False
        self.download_thread: Optional[threading.Thread] = None
        self.youtube_client: YouTubeClient = YouTubeClient(api_token)
        self.youtube_video: Optional[YouTubeVideo] = None
        logger.info("AppController initialized")

    def setup_video_properties(self, url: str, on_output: Optional[Callable[[str], None]] = None) -> None:
        """Fetch video metadata (formats, subtitles, title) using YouTube api and yt-dlp."""
        if not url:
            logger.error("AppController error. No url provided")
            raise ValueError('Url cannot be empty')
        self.url = url

        propertiesRunner = YTDLPRunner()

        output_lines: list[str] = []

        def collect_line(line: str) -> None:
            logger.info("YT-DLP. %s", line)
            output_lines.append(line)
            if on_output:
                on_output(line)

        logger.info("AppController. Start getting video properties.")

        try:
            url_properties = extract_youtube_id(self.url)
            youtube_video_api_properties: dict[str, str] = {}
            if url_properties['type'] == "video":
                youtube_video_api_properties = self.youtube_client.get_video_list(url_properties['id'])

            thumbnail = self._get_thumbnail_from_link(youtube_video_api_properties['thumbnail'])

            propertiesRunner.add_flag([ListSubsFlag(), FormatListFlag()])
            propertiesRunner.run(url, on_output=collect_line)

            if has_error(output_lines):
                error_msg = next(
                    (line for line in output_lines if "ERROR:" in line),
                    "Unknown error occurred"
                )
                logger.error("AppController error. When setup video properties, subprocess error: %s", error_msg)
                raise RuntimeError(f"yt-dlp error: {error_msg}")

            subtitles = subtitles_parse_output(output_lines)
            formats = formats_parse_output(output_lines)

            self.youtube_video = YouTubeVideo(video_id=url_properties['id'],
                                              subtitles=subtitles,
                                              formats=formats,
                                              title=youtube_video_api_properties.get("title"),
                                              duration=youtube_video_api_properties.get("duration"),
                                              thumbnail=thumbnail)

        except Exception as e:
            logger.error("AppController error. When setup video properties, subprocess error: %s", str(e))
            raise YTDLRuntimeError(e) from e

    def get_subtitles(self) -> Subtitles:
        """Get subtitles"""
        if self.youtube_video:
            return self.youtube_video.subtitles
        return Subtitles([], [])

    def get_formats(self) -> list[dict[str, str]]:
        """Get formats"""
        if self.youtube_video:
            return self.youtube_video.formats
        return []

    def get_title(self) -> str:
        """Get title"""
        if self.youtube_video:
            return self.youtube_video.title
        return ""

    def get_duration(self) -> str:
        """Get duration"""
        if self.youtube_video:
            return format_duration(self.youtube_video.duration)
        return ""

    def get_thumbnail(self) -> Optional[ImageFile]:
        """Get thumbnail"""
        if self.youtube_video:
            return self.youtube_video.thumbnail
        return None

    def add_flag(self, flag: BaseFlag) -> None:
        """Add flag"""
        self.flag_processor.add_flag(flag)

    def remove_flag(self, flag: BaseFlag) -> None:
        """Remove flag"""
        self.flag_processor.remove_flag(flag)

    def clear_flags(self) -> None:
        """Clear flags"""
        self.flag_processor.clear_flags()

    def get_flags(self) -> list[BaseFlag]:
        """Get flags"""
        return self.flag_processor.get_flags()

    def start_downloading(self,
                          on_output: Optional[Callable[[str], None]] = None,
                          on_complete: Optional[Callable[[dict], None]] = None) -> Optional[threading.Thread]:
        """Start video download in a background thread."""
        self.runner.add_flag(self.get_flags())

        if self.is_running:
            return None

        def download_task() -> None:
            result = None
            try:
                result = self.runner.run(url=self.url, on_output=on_output)
            except (YTDLRuntimeError, subprocess.CalledProcessError, OSError) as e:
                logger.error("AppController error. When downloading video properties: %s", str(e))
                result = {"return_code": -1, "error": str(e)}
            finally:
                self.is_running = False
                if result and on_complete:
                    on_complete(result)

        logger.info("AppController. Start downloading video.")

        self.download_thread = threading.Thread(target=download_task, daemon=True)
        self.download_thread.start()
        return self.download_thread

    @staticmethod
    def _get_thumbnail_from_link(link: str) -> Optional[ImageFile]:
        """Get thumbnail from link"""
        try:
            url = link.strip()
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            return Image.open(img_data)
        except (TypeError, ValueError, RequestError) as e:
            logger.error("AppController error. When downloading video properties: %s", str(e))
            return None
