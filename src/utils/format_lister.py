from src.core.flags.format_list_flag import FormatListFlag
from src.core.runner import YTDLPRunner

"""
Util for listing available formats via yt-dlp -F.
"""
class FormatLister:
    def __init__(self, yt_dlp_path: str = "yt-dlp"):
        self.runner = YTDLPRunner(yt_dlp_path)
        self.output_formats: list[str] = []

    """Returns a list of formats as structured dictionaries."""
    def get_formats(self, url: str) -> list[dict[str, str]]:

        def collect_line(line: str) -> None:
            self.output_formats.append(line)
        self.runner.add_flag([FormatListFlag()])
        result = self.runner.run(url, on_output=collect_line)
        if result['return_code'] != 1:
            raise RuntimeError(f"yt-dlp failed: {' '.join(result['stderr'])}")

        return self._parse_output()

    """Parses a string returned by yt-dlp. Returns a dictionary."""
    def _parse_output(self) -> list[dict[str, str]]:
        formats: list[dict[str, str]] = []
        in_table = False
        for line in self.output_formats:
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