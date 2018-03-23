"""Exceptions that may be raised during handling of IRC commands"""


class NotVoicedError(Exception):
    """Raised when user call a command but is not voiced"""
    pass
