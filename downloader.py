"""
Core downloading logic for ReelGraber.

Uses yt-dlp under the hood, which is the most reliable and actively
maintained tool for pulling media from Instagram (and many other sites).

This module is written to work the same way on Linux, macOS, and Termux
(Android) — no platform-specific code paths are required, but it adapts
its download format automatically based on whether ffmpeg is available,
since ffmpeg is an optional system package on Termux.
"""

import logging
import os
import re
import shutil

import yt_dlp

logger = logging.getLogger("ReelGraber.downloader")

# Matches Instagram reel / post / IGTV / story links and captures
# the post "type" (reel, p, tv, stories) and its shortcode/id separately,
# so we can rebuild a clean canonical URL without tracking junk like
# "?igsh=...." which can otherwise confuse the extractor.
INSTAGRAM_REGEX = re.compile(
    r"https?://(?:www\.)?instagram\.com/"
    r"(reel|reels|p|tv|stories)/"
    r"([A-Za-z0-9_-]+)"
)

# Detected once at import time. If ffmpeg/ffprobe aren't on PATH (common on
# a fresh Termux install until the user runs `pkg install ffmpeg`), we fall
# back to a single pre-muxed format instead of asking yt-dlp to merge
# separate video/audio streams (which would otherwise fail).
FFMPEG_AVAILABLE = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

if not FFMPEG_AVAILABLE:
    logger.warning(
        "ffmpeg/ffprobe not found on PATH. Falling back to pre-muxed formats. "
        "For the best quality, install ffmpeg "
        "(Termux: 'pkg install ffmpeg', Debian/Ubuntu: 'apt install ffmpeg')."
    )


def extract_url(text: str) -> str | None:
    """
    Extract the first valid Instagram link found inside a message and
    return a CLEAN canonical URL (no query strings, no tracking params).

    e.g. "https://www.instagram.com/reel/DZezV3zzHuD/?igsh=xxxx==" ->
         "https://www.instagram.com/reel/DZezV3zzHuD/"
    """
    if not text:
        return None

    match = INSTAGRAM_REGEX.search(text)
    if not match:
        return None

    post_type, shortcode = match.group(1), match.group(2)
    # "reels" -> "reel" for the canonical URL form
    if post_type == "reels":
        post_type = "reel"

    return f"https://www.instagram.com/{post_type}/{shortcode}/"


class DownloadError(Exception):
    """Raised when a reel cannot be downloaded, with a user-friendly reason."""

    def __init__(self, message: str, raw_error: str = ""):
        super().__init__(message)
        self.message = message
        self.raw_error = raw_error


class ReelDownloader:
    """Wraps yt-dlp to download Instagram reels at the highest available quality."""

    def __init__(self, download_dir: str = "downloads", cookies_file: str | None = None):
        self.download_dir = download_dir
        # Optional path to a Netscape-format cookies.txt exported from a
        # logged-in Instagram session. Instagram frequently requires this
        # for yt-dlp to fetch reel media reliably (anti-scraping measures).
        self.cookies_file = cookies_file
        os.makedirs(self.download_dir, exist_ok=True)

    def download(self, url: str, progress_hook=None) -> str:
        """
        Download the given Instagram URL.

        Returns the local file path of the downloaded video.
        Raises DownloadError with a user-friendly message on failure.
        """
        if FFMPEG_AVAILABLE:
            # Best video + best audio, merged into a single mp4 by ffmpeg.
            fmt = "bv*+ba/best"
        else:
            # No ffmpeg available -> request a single file that already
            # contains both video and audio (Instagram almost always
            # offers an mp4 like this, so quality loss is minimal/none).
            fmt = "best[ext=mp4]/best"

        ydl_opts = {
            "format": fmt,
            "outtmpl": os.path.join(self.download_dir, "%(id)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "retries": 5,
            "fragment_retries": 5,
            "socket_timeout": 30,
            # A real-browser User-Agent helps avoid some Instagram blocks
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            },
        }

        if FFMPEG_AVAILABLE:
            ydl_opts["merge_output_format"] = "mp4"

        if self.cookies_file and os.path.exists(self.cookies_file):
            ydl_opts["cookiefile"] = self.cookies_file

        if progress_hook:
            ydl_opts["progress_hooks"] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
        except yt_dlp.utils.DownloadError as exc:
            raise DownloadError(self._friendly_message(str(exc)), raw_error=str(exc)) from exc
        except Exception as exc:  # noqa: BLE001
            raise DownloadError(
                "An unexpected error occurred while downloading this Reel.",
                raw_error=str(exc),
            ) from exc

        if not info:
            raise DownloadError(
                "Instagram returned no data for this link. It may have been deleted.",
            )

        # yt-dlp can return a "playlist"-style dict for some Instagram posts
        # (e.g. carousels). Grab the first real video entry if so.
        if "entries" in info:
            entries = [e for e in info["entries"] if e]
            if not entries:
                raise DownloadError("This post doesn't contain any downloadable video.")
            info = entries[0]

        filename = self._resolve_filepath(info)

        if not filename or not os.path.exists(filename):
            raise DownloadError(
                "The download finished, but the file could not be located on disk.",
            )

        return filename

    @staticmethod
    def _resolve_filepath(info: dict) -> str | None:
        """
        Work out the final on-disk path of the downloaded/merged file.

        Prefer yt-dlp's own bookkeeping (info["requested_downloads"]),
        which reflects the *actual* file written to disk (e.g. after
        ffmpeg merges streams into .mp4), rather than re-deriving a
        filename ourselves which can drift from reality.
        """
        requested = info.get("requested_downloads") or []
        for entry in requested:
            path = entry.get("filepath") or entry.get("_filename")
            if path and os.path.exists(path):
                return path

        # Fallbacks for older yt-dlp versions or unusual extractors.
        for key in ("filepath", "_filename"):
            path = info.get(key)
            if path and os.path.exists(path):
                return path

        return None

    @staticmethod
    def _friendly_message(raw_error: str) -> str:
        """Translate common yt-dlp error strings into friendly messages."""
        lower = raw_error.lower()

        if "ffmpeg" in lower or "ffprobe" in lower:
            return (
                "ffmpeg is required to process this video but wasn't found. "
                "Install it with `pkg install ffmpeg` (Termux) or "
                "`apt install ffmpeg` (Linux), then try again."
            )
        if "login required" in lower or "rate-limit" in lower or "rate limit" in lower:
            return (
                "Instagram is asking for a login to view this content. "
                "The bot owner needs to add a cookies.txt file (see README "
                "'Handling login-required reels')."
            )
        if "private" in lower:
            return "This account or post is private and can't be downloaded."
        if "unsupported url" in lower or "no video formats" in lower:
            return "This link doesn't point to a downloadable video."
        if "unable to extract" in lower:
            return (
                "Instagram changed something and yt-dlp couldn't read this page. "
                "Try updating yt-dlp (`pip install -U yt-dlp`)."
            )
        if "404" in lower or "not found" in lower:
            return "This post doesn't exist or has been deleted."
        if "timed out" in lower or "timeout" in lower:
            return "The request to Instagram timed out. Please try again."

        return "Instagram blocked or rejected this request."
