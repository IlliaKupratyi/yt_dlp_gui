import os
import sys

"""
Global config
"""
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
YT_DLP_PATH: str = "yt-dlp.exe" if sys.platform == "win32" else "yt-dlp"
TIMEOUT: int = 300
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
