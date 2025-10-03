from src.core.utils.link_parser import validate_youtube_url


def test_validate_youtube_url_valid():
    assert validate_youtube_url("https://youtube.com/watch?v=abc123") == "https://youtube.com/watch?v=abc123"
    assert validate_youtube_url("https://youtu.be/abc123&t=10s") == "https://youtu.be/abc123"

def test_validate_youtube_url_adds_https():
    assert validate_youtube_url("youtube.com/watch?v=abc123") == "https://youtube.com/watch?v=abc123"

def test_validate_youtube_url_invalid_domain():
    assert validate_youtube_url("https://vimeo.com/123") is None

def test_validate_youtube_url_non_string():
    assert validate_youtube_url(None) is None
    assert validate_youtube_url(123) is None  # type: ignore

def test_validate_youtube_url_empty():
    assert validate_youtube_url("") is None