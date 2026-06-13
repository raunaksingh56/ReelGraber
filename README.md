<div align="center">

# 🎬 ReelGraber

### Download Instagram Reels straight from Telegram — in the highest quality, with a live progress bar.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-21.x-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://github.com/python-telegram-bot/python-telegram-bot)
[![yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-red?style=for-the-badge)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## ✨ What is ReelGraber?

**ReelGraber** is a self-hosted Telegram bot that lets you (or anyone you share it with) download **Instagram Reels, Posts, and IGTV videos** in their **highest available quality** — just by sending a link.

No ads, no sketchy third-party websites, no watermarks. Just paste a link and watch a live progress bar do its thing. 🚀

---

## 🔥 Features

- 📥 **Highest-quality downloads** — automatically picks the best video + audio streams and merges them with `yt-dlp`
- 📊 **Live animated progress bar** — see real-time download progress right inside your Telegram chat
- ⚡ **Fast & lightweight** — built on `python-telegram-bot` v21 with fully async handling
- 🧠 **Smart link detection** — automatically finds Instagram links inside any message, even with extra text
- 🛡️ **Graceful error handling** — clear, friendly messages for private posts, broken links, or rate limits (no ugly crashes)
- 🧹 **Auto cleanup** — downloaded files are deleted from the server right after they're sent to you
- 🔐 **Token kept private** — your bot token lives in a local `.env` file, never in the code

---

## 🖥️ Preview

```
You:  https://www.instagram.com/reel/CxxxxxxxxxAB/

Bot:  🔍 Fetching reel info...

Bot:  ⬇️ Downloading Reel...
      [██████████░░░░░░░░] 54.2%

Bot:  ✅ Download complete! [████████████████████] 100.0%
      📤 Uploading to Telegram...

Bot:  🎬 Here's your Reel in the best available quality!
      — ReelGraber
```

---

## 🛠️ Tech Stack

| Component | Purpose |
|---|---|
| [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) | Telegram Bot API wrapper (async) |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Robust, actively-maintained media downloader |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Loads secrets from `.env` |

---

## 📱 Running on Termux (Android)

ReelGraber runs natively on [Termux](https://termux.dev/) — no PC needed.

### 1. Install Termux packages

```bash
pkg update && pkg upgrade -y
pkg install -y python git ffmpeg
```

> `ffmpeg` is optional but recommended — without it, ReelGraber still works by automatically downloading a pre-merged file instead of merging separate video/audio streams.

### 2. Clone & set up the project

```bash
git clone https://github.com/raunaksingh56/ReelGraber.git
cd ReelGraber
pip install -r requirements.txt
```

### 3. Configure your bot token

```bash
cp .env.example .env
nano .env   # paste your BOT_TOKEN, then save with CTRL+O, exit with CTRL+X
```

### 4. Run it

```bash
python main.py
```

### 5. (Optional) Keep it running in the background

Android may kill background processes to save battery. To prevent that:

```bash
termux-wake-lock      # stops Android from sleeping the CPU
```

To keep the bot running after closing the Termux session, use a terminal multiplexer:

```bash
pkg install -y tmux
tmux new -s reelgraber
python main.py
# Detach with CTRL+B then D — the bot keeps running in the background
# Reattach later with: tmux attach -t reelgraber
```

---

## 🚀 Getting Started (Desktop / Server)

### 1. Clone the repository

```bash
git clone https://github.com/raunaksingh56/ReelGraber.git
cd ReelGraber
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your bot on Telegram

1. Open Telegram and search for **[@BotFather](https://t.me/BotFather)**
2. Send `/newbot` and follow the steps
3. Copy the **bot token** it gives you

### 5. Configure your environment

```bash
cp .env.example .env
```

Then open `.env` and paste your token:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

### 6. Run the bot

```bash
python main.py
```

You should see:

```
🚀 ReelGraber is up and running...
```

Now open Telegram, find your bot, send `/start`, and drop in a Reel link! 🎉

---

## 📁 Project Structure

```
ReelGraber/
├── main.py             # Bot entry point — handles commands & messages
├── downloader.py        # yt-dlp wrapper for fetching reels in best quality
├── progress_bar.py       # Renders the live progress bar
├── config.py            # Loads configuration from .env
├── requirements.txt      # Python dependencies
├── .env.example          # Template for your environment variables
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🍪 Handling Login-Required Reels

Instagram increasingly requires a **logged-in session** for `yt-dlp` to fetch reel media — without it you may see errors like *"Couldn't download this Reel"* even for valid public links.

To fix this, export your Instagram cookies and let ReelGraber use them:

1. Install a browser extension like **[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)** (Chrome/Edge) or the Firefox equivalent.
2. Log in to **instagram.com** in your browser.
3. Use the extension to export cookies for `instagram.com` as a `cookies.txt` file.
4. Place that file in the project root (same folder as `main.py`).
5. (Optional) If you named it something else or put it elsewhere, set the path in `.env`:

```env
COOKIES_FILE=cookies.txt
```

ReelGraber automatically picks up `cookies.txt` if it exists — no other changes needed.

> ⚠️ Treat `cookies.txt` like a password — it's already in `.gitignore` so it won't be committed. Never share it or upload it anywhere public.

---

## ⚠️ Notes & Limitations

- Telegram bots can only upload files up to **~50 MB**. Extremely long/high-bitrate reels may exceed this limit.
- Private posts/accounts cannot be downloaded — this respects Instagram's access controls.
- This project is intended for **personal use** to save content you have the right to access. Please respect content creators' rights and Instagram's Terms of Service.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### Made with ❤️ by [raunaksingh56](https://github.com/raunaksingh56)

⭐ If you found this useful, consider giving it a star!

</div>
