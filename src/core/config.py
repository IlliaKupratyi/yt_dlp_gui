import os
import sys

"""
Global config
"""
class Config:
    YT_DLP_PATH: str = "yt-dlp.exe" if sys.platform == "win32" else "yt-dlp"
    TIMEOUT: int = 300
    WORK_DIR = os.path.expanduser("~")