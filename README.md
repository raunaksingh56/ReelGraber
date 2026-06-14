<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12&height=200&section=header&text=ReelGraber&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Grab%20any%20Instagram%20Reel%20straight%20from%20Telegram&descAlignY=55&descSize=18" />

<img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=600&size=24&duration=3000&pause=800&color=F75C7E&center=true&vCenter=true&width=600&lines=%F0%9F%93%A5+Highest+quality+downloads;%F0%9F%93%8A+Live+animated+progress+bars;%F0%9F%93%A4+Real-time+upload+status;%E2%9A%A1+Fast%2C+async%2C+self-hosted" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-21.x-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://github.com/python-telegram-bot/python-telegram-bot)
[![yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-red?style=for-the-badge)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](LICENSE)

[![Stars](https://img.shields.io/github/stars/raunaksingh56/ReelGraber?style=for-the-badge&color=ffcb47)](https://github.com/raunaksingh56/ReelGraber/stargazers)
[![Forks](https://img.shields.io/github/forks/raunaksingh56/ReelGraber?style=for-the-badge&color=8e7cc3)](https://github.com/raunaksingh56/ReelGraber/network/members)
[![Last Commit](https://img.shields.io/github/last-commit/raunaksingh56/ReelGraber?style=for-the-badge&color=00d2ff)](https://github.com/raunaksingh56/ReelGraber/commits/main)

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## ✨ What is ReelGraber?

**ReelGraber** is a self-hosted Telegram bot that lets you (or anyone you share it with) download **Instagram Reels, Posts, and IGTV videos** in their **highest available quality** — just by sending a link.

No ads, no sketchy third-party websites, no watermarks. Just paste a link and watch the magic happen. 🚀

<br/>

## 🔥 Features

<table>
<tr>
<td width="33%" align="center">

### 📥
**Highest-quality downloads**
<br/>
Automatically picks the best video + audio streams and merges them with `yt-dlp`

</td>
<td width="33%" align="center">

### 📊
**Live progress bars**
<br/>
Real-time animated download **and** upload progress, right inside your chat

</td>
<td width="33%" align="center">

### ⚡
**Fast & async**
<br/>
Built on `python-telegram-bot` v21 with fully async, non-blocking handling

</td>
</tr>
<tr>
<td width="33%" align="center">

### 🧠
**Smart link detection**
<br/>
Finds Instagram links inside any message, even with extra text around them

</td>
<td width="33%" align="center">

### 🛡️
**Graceful errors**
<br/>
Friendly messages for private posts, broken links, or rate limits — no crashes

</td>
<td width="33%" align="center">

### 🔐
**Privacy first**
<br/>
Token lives in a local `.env` and downloads are auto-deleted after sending

</td>
</tr>
</table>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## 🖥️ Live Preview

```text
You:  https://www.instagram.com/reel/CxxxxxxxxxAB/

Bot:  🔍 Fetching reel info...

Bot:  ⬇️ Downloading Reel...
      [██████████░░░░░░░░] 54.2%

Bot:  ⚙️ Processing video...
      [████████████████████] 100.0%

Bot:  📤 Uploading to Telegram...
      [██████████████░░░░░░] 71.8%

Bot:  🎬 Here's your Reel in the best available quality!
      — ReelGraber
```

> 💡 Both the download **and** upload bars update live in the same message — no spam, just one smooth animation.

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram%20Bot%20API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
![Asyncio](https://img.shields.io/badge/asyncio-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Termux](https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=android&logoColor=green)

</div>

| Component | Purpose |
|---|---|
| [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) | Telegram Bot API wrapper (async) |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Robust, actively-maintained media downloader |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Loads secrets from `.env` |

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## 📱 Running on Termux (Android)

ReelGraber runs natively on [Termux](https://termux.dev/) — no PC needed.

<details>
<summary><b>1️⃣ Install Termux packages</b></summary>

```bash
pkg update && pkg upgrade -y
pkg install -y python git ffmpeg
```

> `ffmpeg` is optional but recommended — without it, ReelGraber still works by automatically downloading a pre-merged file instead of merging separate video/audio streams.

</details>

<details>
<summary><b>2️⃣ Clone & set up the project</b></summary>

```bash
git clone https://github.com/raunaksingh56/ReelGraber.git
cd ReelGraber
pip install -r requirements.txt
```

</details>

<details>
<summary><b>3️⃣ Configure your bot token</b></summary>

```bash
cp .env.example .env
nano .env   # paste your BOT_TOKEN, then save with CTRL+O, exit with CTRL+X
```

</details>

<details>
<summary><b>4️⃣ Run it</b></summary>

```bash
python main.py
```

</details>

<details>
<summary><b>5️⃣ (Optional) Keep it running in the background</b></summary>

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

</details>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## 🚀 Getting Started (Desktop / Server)

<details open>
<summary><b>1️⃣ Clone the repository</b></summary>

```bash
git clone https://github.com/raunaksingh56/ReelGraber.git
cd ReelGraber
```

</details>

<details>
<summary><b>2️⃣ Create a virtual environment (recommended)</b></summary>

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

</details>

<details>
<summary><b>3️⃣ Install dependencies</b></summary>

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>4️⃣ Create your bot on Telegram</b></summary>

1. Open Telegram and search for **[@BotFather](https://t.me/BotFather)**
2. Send `/newbot` and follow the steps
3. Copy the **bot token** it gives you

</details>

<details>
<summary><b>5️⃣ Configure your environment</b></summary>

```bash
cp .env.example .env
```

Then open `.env` and paste your token:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

</details>

<details>
<summary><b>6️⃣ Run the bot</b></summary>

```bash
python main.py
```

You should see:

```text
🚀 ReelGraber is up and running...
```

Now open Telegram, find your bot, send `/start`, and drop in a Reel link! 🎉

</details>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## 📁 Project Structure

```text
ReelGraber/
├── main.py             # Bot entry point — handles commands & messages
├── downloader.py       # yt-dlp wrapper for fetching reels in best quality
├── progress_bar.py     # Renders the live progress bar
├── progress_file.py    # Tracks live upload progress
├── config.py           # Loads configuration from .env
├── requirements.txt    # Python dependencies
├── .env.example        # Template for your environment variables
├── .gitignore
├── LICENSE
└── README.md
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

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

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## ⚠️ Notes & Limitations

- Telegram bots can only upload files up to **~50 MB**. Extremely long/high-bitrate reels may exceed this limit.
- Private posts/accounts cannot be downloaded — this respects Instagram's access controls.
- This project is intended for **personal use** to save content you have the right to access. Please respect content creators' rights and Instagram's Terms of Service.

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12&height=3&section=header" width="100%"/>

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<div align="center">

### Made with ❤️ by [raunaksingh56](https://github.com/raunaksingh56)

⭐ If you found this useful, consider giving it a star!

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12&height=120&section=footer" width="100%"/>

</div>
