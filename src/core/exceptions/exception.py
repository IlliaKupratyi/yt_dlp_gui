"""
Custom exceptions
"""

class YTDLRuntimeException(Exception):
    """An error occurred while executing yt-dlp"""

class FlagValidatorError(Exception):
    """Flag validation error"""

class YTDLRuntimeError(Exception):
    """Yt-dlp error"""
