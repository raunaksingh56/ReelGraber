"""
Small helper used to show a live "Uploading..." progress bar.

Wraps a file on disk so that every time python-telegram-bot/httpx reads a
chunk of it (while streaming the upload to Telegram's servers), we get a
callback with the percentage uploaded so far.
"""

import os
from typing import Callable


class ProgressFile:
    """
    A read-only, file-like wrapper around a path on disk.

    Each call to .read() forwards to the underlying file and reports
    cumulative progress via `callback(percent)`, where percent is a
    float from 0.0 to 100.0.
    """

    def __init__(self, path: str, callback: Callable[[float], None]):
        self._file = open(path, "rb")
        self._total = os.path.getsize(path)
        self._read_bytes = 0
        self._callback = callback

    def read(self, size: int = -1) -> bytes:
        chunk = self._file.read(size)
        self._read_bytes += len(chunk)
        if self._total:
            percent = min(100.0, self._read_bytes / self._total * 100)
            try:
                self._callback(percent)
            except Exception:
                # Progress reporting must never break the upload itself.
                pass
        return chunk

    def __getattr__(self, item):
        # Delegate anything we don't explicitly handle (seek, tell, name,
        # etc.) to the underlying file object so this still quacks like a
        # normal file for httpx/python-telegram-bot.
        return getattr(self._file, item)

    def close(self) -> None:
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
        
