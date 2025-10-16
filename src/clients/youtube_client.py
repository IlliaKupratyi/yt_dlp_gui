"""
Client to make API requests to YouTube
"""
import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger("yt_dlp_gui")


class YouTubeClient:
    """Class for making API requests to YouTube"""
    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.youtube_client = build("youtube", "v3", developerKey=api_key)

    def get_video_list(self, video_id: str) -> dict[str, str]:
        """Function for getting video list from YouTube API"""
        try:
            request = self.youtube_client.videos().list(part="contentDetails,snippet", id=video_id)
            response = request.execute()

            if not response["items"]:
                raise ValueError("No video found")

            youtube_video: dict[str, str] = {}

            if 'snippet' in response["items"][0]:
                if 'title' in response["items"][0]["snippet"]:
                    youtube_video['title'] = response["items"][0]["snippet"]["title"]

                if 'thumbnails' in response["items"][0]["snippet"]:
                    if 'maxres' in response["items"][0]["snippet"]["thumbnails"]:
                        youtube_video['thumbnail'] = response["items"][0]["snippet"]["thumbnails"]["maxres"]["url"]
                    elif 'standard' in response["items"][0]["snippet"]["thumbnails"]:
                        youtube_video['thumbnail'] = response["items"][0]["snippet"]["thumbnails"]["standard"]["url"]
                    elif 'high' in response["items"][0]["snippet"]["thumbnails"]:
                        youtube_video['thumbnail'] = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
                    elif 'medium' in response["items"][0]["snippet"]["thumbnails"]:
                        youtube_video['thumbnail'] = response["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
                    elif 'default' in response["items"][0]["snippet"]["thumbnails"]:
                        youtube_video['thumbnail'] = response["items"][0]["snippet"]["thumbnails"]["default"]["url"]

            if ('contentDetails' in response["items"][0] and
                    'duration' in response["items"][0]["contentDetails"]):
                youtube_video['duration'] = response["items"][0]["contentDetails"]["duration"]

            return youtube_video

        except (HttpError, KeyError, TypeError) as e:
            logger.error("YouTubeClient error. When requesting API videos.list: %s", str(e))
            return {}
