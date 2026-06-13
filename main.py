"""
ReelGraber — Telegram bot that downloads Instagram Reels in the highest
available quality, with a live, animated progress bar.

Author: raunaksingh56
"""

import asyncio
import logging
import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.request import HTTPXRequest

from config import BOT_TOKEN, COOKIES_FILE, DOWNLOAD_DIR, MAX_FILE_SIZE_MB
from downloader import DownloadError, ReelDownloader, extract_url
from progress_bar import make_progress_bar

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("ReelGraber")

downloader = ReelDownloader(DOWNLOAD_DIR, cookies_file=COOKIES_FILE)

WELCOME_MESSAGE = (
    "🎬 *Welcome to ReelGraber!*\n\n"
    "Send me any Instagram *Reel*, *Post*, or *IGTV* link and I'll grab it "
    "for you in the *highest quality* available — fast and clean.\n\n"
    "📌 *How to use:*\n"
    "1️⃣ Copy a link from Instagram\n"
    "2️⃣ Paste it here\n"
    "3️⃣ Watch the live progress bar 🚀\n\n"
    "_Made with ❤️ by_ @raunaksingh56"
)

HELP_MESSAGE = (
    "🤖 *ReelGraber Help*\n\n"
    "Just send me an Instagram link, for example:\n"
    "`https://www.instagram.com/reel/XXXXXXXXXXX/`\n\n"
    "*Commands:*\n"
    "/start — Show the welcome message\n"
    "/help — Show this help message"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode=ParseMode.MARKDOWN)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    url = extract_url(text)

    if not url:
        await update.message.reply_text(
            "⚠️ I couldn't find a valid Instagram link in your message.\n\n"
            "Send something like:\n`https://www.instagram.com/reel/XXXXXXXXXXX/`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    status_msg = await update.message.reply_text(
        "🔍 *Fetching reel info...*", parse_mode=ParseMode.MARKDOWN
    )

    # Shared state updated by yt-dlp's progress hook (runs in a worker thread)
    progress_state = {
        "percent": 0.0,
        "stage": "starting",
        "done": False,
        "error": None,
        "raw_error": None,
        "filepath": None,
    }

    def progress_hook(d: dict) -> None:
        status = d.get("status")
        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                progress_state["percent"] = downloaded / total * 100
            progress_state["stage"] = "downloading"
        elif status == "finished":
            progress_state["percent"] = 100.0
            progress_state["stage"] = "processing"

    loop = asyncio.get_running_loop()

    async def run_download() -> None:
        try:
            filepath = await loop.run_in_executor(
                None, downloader.download, url, progress_hook
            )
            progress_state["filepath"] = filepath
        except DownloadError as exc:
            progress_state["error"] = exc.message
            progress_state["raw_error"] = exc.raw_error
        except Exception as exc:  # noqa: BLE001 - catch-all safety net
            progress_state["error"] = "An unexpected error occurred."
            progress_state["raw_error"] = str(exc)
        finally:
            progress_state["done"] = True

    download_task = asyncio.create_task(run_download())

    # Live-update the status message while the download runs
    last_rendered = ""
    while not progress_state["done"]:
        bar = make_progress_bar(progress_state["percent"])
        stage = progress_state["stage"]
        emoji = "⚙️" if stage == "processing" else "⬇️"
        label = "Processing video..." if stage == "processing" else "Downloading Reel..."
        rendered = f"{emoji} *{label}*\n\n{bar}"

        if rendered != last_rendered:
            try:
                await status_msg.edit_text(rendered, parse_mode=ParseMode.MARKDOWN)
                last_rendered = rendered
            except Exception:
                pass  # ignore "message not modified" / rate-limit edits

        await asyncio.sleep(1.2)

    await download_task

    # --- Handle download errors gracefully ---
    if progress_state["error"]:
        logger.error(
            "Download failed for %s | shown: %s | raw: %s",
            url,
            progress_state["error"],
            progress_state["raw_error"],
        )
        await status_msg.edit_text(
            f"❌ *Couldn't download this Reel.*\n\n{progress_state['error']}\n\n"
            "If this keeps happening, double-check the link or try again later.",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    filepath = progress_state["filepath"]
    if not filepath or not os.path.exists(filepath):
        await status_msg.edit_text(
            "❌ Something went wrong — the downloaded file could not be found.",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    size_mb = os.path.getsize(filepath) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        await status_msg.edit_text(
            f"⚠️ Downloaded successfully ({size_mb:.1f} MB), but it's larger "
            f"than Telegram's {MAX_FILE_SIZE_MB} MB upload limit for bots.",
            parse_mode=ParseMode.MARKDOWN,
        )
        os.remove(filepath)
        return

    await status_msg.edit_text(
        f"✅ *Download complete!* {make_progress_bar(100)}\n\n📤 Uploading to Telegram...",
        parse_mode=ParseMode.MARKDOWN,
    )

    try:
        with open(filepath, "rb") as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="🎬 Here's your Reel in the best available quality!\n\n— *ReelGraber*",
                parse_mode=ParseMode.MARKDOWN,
                supports_streaming=True,
                # Uploading video can take much longer than the default
                # ~5s HTTP timeout, especially on slower mobile connections
                # (e.g. Termux on cellular data). Give it plenty of room.
                read_timeout=120,
                write_timeout=180,
                connect_timeout=60,
                pool_timeout=60,
            )
        await status_msg.delete()
    except Exception as exc:  # noqa: BLE001
        logger.error("Upload failed for %s: %s", url, exc, exc_info=True)
        await status_msg.edit_text(
            f"❌ The video downloaded fine, but I couldn't send it back to you.\n\n"
            f"Reason: `{type(exc).__name__}: {exc}`\n\n"
            "This is often a network timeout — please try again.",
            parse_mode=ParseMode.MARKDOWN,
        )
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not set. Create a .env file (see .env.example) "
            "and add your Telegram bot token."
        )

    # Default timeouts (~5s) are too short for video uploads/downloads,
    # especially on mobile connections (e.g. Termux on cellular data).
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=60.0,
        write_timeout=120.0,
        pool_timeout=60.0,
    )
    # getUpdates long-polling needs its own (longer) read timeout.
    get_updates_request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=40.0,
        pool_timeout=60.0,
    )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .get_updates_request(get_updates_request)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🚀 ReelGraber is up and running...")
    logger.info("Downloads will be stored in: %s", DOWNLOAD_DIR)
    if os.path.exists(COOKIES_FILE):
        logger.info("Using cookies file: %s", COOKIES_FILE)
    else:
        logger.info("No cookies.txt found — running without Instagram login.")

    try:
        # drop_pending_updates avoids replaying a backlog of old messages
        # (common after restarting the bot manually on Termux).
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("👋 ReelGraber stopped by user.")


if __name__ == "__main__":
    main()
                
