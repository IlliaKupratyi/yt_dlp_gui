"""
Util for process links
"""
import re
from urllib.parse import urlparse, parse_qs


def validate_youtube_url(url: str) -> str | None:
    """Validates and cleans a YouTube URL."""
    if not url or not isinstance(url, str):
        return None

    url = url.split('&', 1)[0]

    if not re.match(r'^https?://', url):
        if url.startswith(('youtube.com/', 'www.youtube.com/', 'youtu.be/')):
            url = 'https://' + url
        else:
            return None

    try:
        parsed = urlparse(url)
    except (ValueError, OSError):
        return None

    netloc = parsed.netloc.lower().replace('www.', '')
    if netloc not in ('youtube.com', 'youtu.be'):
        return None

    return url


def extract_youtube_id(url: str):
    """Extract video or playlist id from YouTube link"""
    url = url.strip()

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    if parsed.netloc not in ('www.youtube.com', 'youtube.com', 'm.youtube.com', 'youtu.be'):
        return None

    if parsed.netloc == 'youtu.be':
        video_id = parsed.path.lstrip('/')
        if video_id and re.match(r'^[a-zA-Z0-9_-]+$', video_id):
            return {'type': 'video', 'id': video_id}
        return None

    path = parsed.path.lower()

    if path == '/watch':
        video_id = query_params.get('v', [None])[0]
        if video_id and re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
            playlist_id = query_params.get('list', [None])[0]
            if playlist_id and re.match(r'^[a-zA-Z0-9_-]+$', playlist_id):
                return {'type': 'playlist', 'id': playlist_id}
            return {'type': 'video', 'id': video_id}

    elif path == '/playlist':
        playlist_id = query_params.get('list', [None])[0]
        if playlist_id and re.match(r'^[a-zA-Z0-9_-]+$', playlist_id):
            return {'type': 'playlist', 'id': playlist_id}

    elif path.startswith('/embed/'):
        video_id = path.split('/')[2]
        if video_id and re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
            return {'type': 'video', 'id': video_id}

    elif path.startswith('/v/'):
        video_id = path.split('/')[2]
        if video_id and re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
            return {'type': 'video', 'id': video_id}

    return None