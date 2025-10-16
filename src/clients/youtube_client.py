from googleapiclient.discovery import build


class YouTubeClient:
    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.youtube_client = build("youtube", "v3", developerKey=api_key)

    def get_video_list(self, video_id: str) -> dict[str, str]:
        try:
            request = self.youtube_client.videos().list(part="contentDetails,snippet", id=video_id)
            response = request.execute()

            if not response["items"]:
                raise ValueError("No video found")

            youtube_video: dict[str, str] = {}

            if 'snippet' in response["items"][0]:
                if 'title' in response["items"][0]["snippet"]:
                    youtube_video['title'] = response["items"][0]["snippet"]["title"]

                if ('thumbnails' in response["items"][0]["snippet"] and
                    'default' in response["items"][0]["snippet"]["thumbnails"]):
                    youtube_video['thumbnail'] = response["items"][0]["snippet"]["thumbnails"]["default"]["url"]

            if ('contentDetails' in response["items"][0] and
                    'duration' in response["items"][0]["contentDetails"]):
                youtube_video['duration'] = response["items"][0]["contentDetails"]["duration"]

            return youtube_video

        except Exception as e:
            print(e)
            return {}