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

def presets_to_dict(presets: list[str]) -> list[dict[str, str]]:
    result_dict: list[dict[str, str]] = []
    for preset in presets:
        result_dict.append({"id": preset.lower(), "value": preset})

    return result_dict

def formats_to_dict(formats: list[dict[str, str]]) -> list[dict[str, str]]:
    result_dict: list[dict[str, str]] = []
    for format_value in formats:
        result_dict.append({"id": format_value["id"], "value": format_value["ext"] + " " + format_value["resolution"]})

    return result_dict

def filter_by_unique_values(items: list[dict[str, str]]) -> list[dict[str, str]]:
        seen_values = set()
        unique_items = []
        for item in items:
            value = item.get("value")
            if value not in seen_values:
                seen_values.add(value)
                unique_items.append(item)
        return unique_items