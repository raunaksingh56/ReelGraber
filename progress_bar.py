"""
Small helper to render a clean, unique-looking text progress bar
that works inside Telegram messages (no images needed).
"""


def make_progress_bar(percent: float, length: int = 18) -> str:
    """
    Render a progress bar like: [█████████░░░░░░░░░] 52.3%

    percent: 0-100
    length: total number of characters in the bar
    """
    percent = max(0.0, min(100.0, percent))
    filled = int(length * percent / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"`[{bar}]` *{percent:5.1f}%*"
