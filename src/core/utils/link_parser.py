import re
from urllib.parse import urlparse

"""
Validates and cleans a YouTube URL.
"""
def validate_youtube_url(url: str) -> str | None:
    if not url or not isinstance(url, str):
        return None

    url = url.split('&', 1)[0]

    if not re.match(r'^https?://', url):
        # Пробуем добавить схему, если её нет
        if url.startswith(('youtube.com/', 'www.youtube.com/', 'youtu.be/')):
            url = 'https://' + url
        else:
            return None

    try:
        parsed = urlparse(url)
    except Exception:
        return None

    netloc = parsed.netloc.lower().replace('www.', '')
    if netloc not in ('youtube.com', 'youtu.be'):
        return None

    return url