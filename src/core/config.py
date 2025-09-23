import os
import sys

"""
Global config
"""
class Config:
    YT_DLP_PATH: str = "yt-dlp.exe" if sys.platform == "win32" else "yt-dlp"
    TIMEOUT: int = 300
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
