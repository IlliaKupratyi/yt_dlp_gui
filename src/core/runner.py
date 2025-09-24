import subprocess
from typing import Optional, Callable, Any

from src.core.config import YT_DLP_PATH
from src.core.flags.base import BaseFlag

"""
Manages execution of yt-dlp via subprocess
"""
class YTDLPRunner:

    """
    Initialize the runner with an optional custom path to yt-dlp executable.

    If no path is provided, uses the default from Config.YT_DLP_PATH,
    which automatically selects 'yt-dlp.exe' on Windows or 'yt-dlp' on Unix-like systems.
    """
    def __init__(self, yt_dlp_path: str | None = None):
        self.yt_dlp_path: str = yt_dlp_path or YT_DLP_PATH
        self.flags: list[BaseFlag] = []

    """
    Add a flag object to the command configuration.
    """
    def add_flag(self, flag: BaseFlag) -> "YTDLPRunner":
        if not isinstance(flag, BaseFlag):
            raise TypeError("flag must be of type BaseFlag")

        self.flags.append(flag)
        return self

    """
    Construct the complete command line as a list of strings for subprocess.Popen.
    """
    def build_command(self, url: str) -> list[str]:
        if not url:
            raise ValueError("url cannot be empty")

        cmd: list[str] = [self.yt_dlp_path]

        for flag in self.flags:
            cmd.extend(flag.to_args())

        cmd.append(url)

        return cmd

    """
    Execute yt-dlp with the configured flags and stream output in real time.
    """
    def run(self, url: str, on_output: Optional[Callable[[str], None]] = None) -> dict[str, Any]:
        cmd = self.build_command(url) # Build the command
        stdout_lines: list[str] = []

        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   stdin=subprocess.DEVNULL,
                                   universal_newlines=True,
                                   bufsize=1,
                                   encoding="utf-8",
                                   errors="replace") # Launch yt-dlp as a subprocess
        if process.stdout is not None:
            for line in process.stdout: # Stream stdout line-by-line
                line = line.rstrip('\r\n')
                stdout_lines.append(line)
                if on_output:
                    on_output(line) # Invoke on_output callback for each line
        else:
            raise RuntimeError("Stdout cannot be None")

        return_code = process.wait() # Wait for process completion

        return {
            "return_code": return_code,
            "stdout": stdout_lines,
            "cmd": cmd,
        }