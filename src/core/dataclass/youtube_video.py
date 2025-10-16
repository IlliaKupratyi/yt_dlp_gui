from dataclasses import dataclass

from src.core.dataclass.subtitle import Subtitles

@dataclass
class YouTubeVideo:
    subtitles: Subtitles
    formats: list[dict[str, str]]
    video_id: str = ""
    title: str = ""
    duration: str = ""
    thumbnail: str = ""