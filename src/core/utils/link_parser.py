"""
Util for process links
"""
import re
from urllib.parse import urlparse


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
