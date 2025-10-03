"""Check if any line contains a known yt-dlp error indicator."""
def has_error( output_lines: list[str]) -> bool:
    error_indicators = [
        "ERROR:",
        "Unable to extract",
        "Incomplete YouTube ID",
        "Invalid URL",
        "Unsupported URL",
        "Video unavailable"
    ]
    return any(
        any(indicator in line for indicator in error_indicators)
        for line in output_lines
    )