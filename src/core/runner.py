import subprocess
from typing import Optional, Callable, Any

from src.core.config.config import YT_DLP_PATH
from src.core.flags.base_flag import BaseFlag

import logging

logger = logging.getLogger("yt_dlp_gui")

"""
Manages execution of yt-dlp via subprocess
"""
class YTDLPRunner:
    def __init__(self, yt_dlp_path: str | None = None):
        self.yt_dlp_path: str = yt_dlp_path or YT_DLP_PATH
        self.flags: list[BaseFlag] = []
        logger.info("YTDLPRunner initialized")

    """
    Add a flag object to the command configuration.
    """
    def add_flag(self, flag: list[BaseFlag]) -> "YTDLPRunner":
        for f in flag:
            if not isinstance(f, BaseFlag):
                logger.error("YTDLPRunner error. Flag must be of type BaseFlag")
                raise TypeError("flag must be of type BaseFlag")

        self.flags.extend(flag)
        return self

    """
    Construct the complete command line as a list of strings for subprocess.Popen.
    """
    def build_command(self, url: str) -> list[str]:
        if not url:
            logger.error("YTDLPRunner error. Empty url")
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

        logger.info("YTDLPRunner. Starting subprocess with command: " + " ".join(cmd) + "\n ***** \n ***** \n ***** \n ")

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
            logger.error("YTDLPRunner error. Stdout is empty")
            raise RuntimeError("Stdout cannot be None")

        return_code = process.wait() # Wait for process completion

        return {
            "return_code": return_code,
            "stdout": stdout_lines,
            "cmd": cmd,
        }