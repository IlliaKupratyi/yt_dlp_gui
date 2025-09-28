
"""
Util for listing available formats via yt-dlp -F.
"""

"""Parses a string returned by yt-dlp. Returns a dictionary."""
def formats_parse_output(output_formats: list[str]) -> list[dict[str, str]]:
    formats: list[dict[str, str]] = []
    in_table = False
    for line in output_formats:
        if line.startswith("ID"):
            in_table = True
            continue
        if not in_table or not line.strip():
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        if not parts[0].isdigit():
            continue
        formats.append({
            "id": parts[0],
            "ext": parts[1],
            "resolution": parts[2] if parts[2] != "audio" else "audio only",
            "tbr": parts[7] if  parts[2] == "audio" else "" if len(parts) < 6 else parts[6],
            "format_note": " ".join(parts[7:]) if len(parts) > 7 else "",
        })
    return formats