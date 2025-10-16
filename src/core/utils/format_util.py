"""
Format util
"""

from isodate import parse_duration as parse_iso_duration


def formats_parse_output(output_formats: list[str]) -> list[dict[str, str]]:
    """Parses a string returned by yt-dlp. Returns a dictionary."""
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

def presets_to_dict(presets: list[str]) -> list[dict[str, str]]:
    """Convert a list of preset names to a list of {id, value} dicts."""
    result_dict: list[dict[str, str]] = []
    for preset in presets:
        result_dict.append({"id": preset.lower(), "value": preset})

    return result_dict

def formats_to_dict(formats: list[dict[str, str]]) -> list[dict[str, str]]:
    """Convert raw format dicts to {id, value} dicts for UI display."""
    result_dict: list[dict[str, str]] = []
    for format_value in formats:
        result_dict.append({"id": format_value["id"], "value": format_value["ext"] + " " + format_value["resolution"]})

    return result_dict

def filter_by_unique_values(items: list[dict[str, str]]) -> list[dict[str, str]]:
    """Remove items with duplicate 'value' fields, keeping first occurrence."""
    seen_values = set()
    unique_items = []
    for item in items:
        value = item.get("value")
        if value not in seen_values:
            seen_values.add(value)
            unique_items.append(item)
    return unique_items

def format_duration(duration: str) -> str:
    """Convert ISO 8601 duration to 'hh:mm:ss' or 'mm:ss'."""
    try:
        td = parse_iso_duration(duration)
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    except Exception:
        return "0:00"