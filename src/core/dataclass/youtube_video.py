from dataclasses import dataclass
from typing import Optional
from PIL.Image import Image

from src.core.dataclass.subtitle import Subtitles

@dataclass
class YouTubeVideo:
    subtitles: Subtitles
    formats: list[dict[str, str]]
    thumbnail: Optional[Image]
    video_id: str = ""
    title: str = ""
    duration: str = ""