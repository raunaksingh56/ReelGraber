"""
Configuration for ReelGraber.

All sensitive values (like your bot token) should be stored in a .env file,
NEVER hardcoded directly in this file or committed to GitHub.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Resolve paths relative to the project root (where this file lives), not the
# current working directory. This matters on Termux/mobile shells where the
# bot is often launched from a shortcut/widget with a different cwd (e.g. $HOME)
# than the project folder.
BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

# Telegram Bot token (get one from @BotFather on Telegram)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Folder where reels are temporarily downloaded before being sent.
# Relative paths are resolved against the project root.
_download_dir = os.getenv("DOWNLOAD_DIR", "downloads")
DOWNLOAD_DIR = str(BASE_DIR / _download_dir) if not os.path.isabs(_download_dir) else _download_dir

# Telegram bots can only upload files up to ~50MB (standard Bot API limit)
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))

# Optional: path to a Netscape-format cookies.txt exported from a logged-in
# Instagram session in your browser. Instagram frequently requires this for
# yt-dlp to reliably fetch reels (see README "Handling login-required reels").
_cookies_file = os.getenv("COOKIES_FILE", "cookies.txt")
COOKIES_FILE = str(BASE_DIR / _cookies_file) if not os.path.isabs(_cookies_file) else _cookies_file
