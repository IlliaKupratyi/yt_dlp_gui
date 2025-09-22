import os
import sys

"""
Global config
"""
class Config:
    YT_DLP_PATH = "yt-dlp.exe" if sys.platform == "win32" else "yt-dlp"
    TIMEOUT = 300
    WORK_DIR = os.path.expanduser("~")