"""
utils.py — Shared helper utilities for Slack Bot Studio.
"""

import os
import time
import datetime
from PIL import Image

from config import ASSETS_DIR, CAT_IMAGE_PATH


# ---------------------------------------------------------------------------
# Log entry builder
# ---------------------------------------------------------------------------
_BADGE_MAP: dict[str, str] = {
    "CONNECT":  "badge-info",
    "API":      "badge-api",
    "SUCCESS":  "badge-success",
    "EVENT":    "badge-event",
    "ERROR":    "badge-error",
}


def build_log_entry(category: str, message: str) -> str:
    """Return an HTML string for a single log line with timestamp and badge."""
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    badge_cls = _BADGE_MAP.get(category.upper(), "badge-info")
    return (
        f'<div class="log-entry">'
        f'<span class="log-time">[{ts}]</span> '
        f'<span class="log-badge {badge_cls}">{category.upper()}</span> '
        f'{message}'
        f'</div>\n'
    )


# ---------------------------------------------------------------------------
# Initial log state (built fresh at import-time so timestamps are accurate)
# ---------------------------------------------------------------------------
def build_initial_logs() -> str:
    """Generate the startup log entries with current timestamps."""
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    lines = [
        build_log_entry("CONNECT", "Initializing Slack Socket Mode client…"),
        build_log_entry("API",     "auth.test &rarr; 200 OK (team: ai-workplace, bot_id: B0BHJTV)"),
        build_log_entry("SUCCESS", "Connected to Slack Workspace <b>ai-workplace</b>"),
        build_log_entry("EVENT",   "Subscribed to <b>#ai-test</b> for <b>@AI Bot</b> mentions"),
    ]
    return "".join(lines)


# ---------------------------------------------------------------------------
# Image persistence helper
# ---------------------------------------------------------------------------
def save_upload(img_input) -> str:
    """
    Accept a filepath string or a PIL Image / numpy array from gr.Image.
    Saves it under assets/ with a timestamped filename.
    Returns the saved filepath, or CAT_IMAGE_PATH on failure.
    """
    os.makedirs(ASSETS_DIR, exist_ok=True)
    dest = os.path.join(ASSETS_DIR, f"upload_{int(time.time())}.jpg")

    try:
        if isinstance(img_input, str):
            # Already a filepath — just return it directly
            if os.path.exists(img_input):
                return img_input
            return CAT_IMAGE_PATH

        if isinstance(img_input, Image.Image):
            img_input.convert("RGB").save(dest)
            return dest

        # Numpy array from gr.Image(type="numpy")
        import numpy as np
        if isinstance(img_input, np.ndarray):
            Image.fromarray(img_input).convert("RGB").save(dest)
            return dest

    except Exception:
        pass

    return CAT_IMAGE_PATH


# ---------------------------------------------------------------------------
# Stat card HTML builders (kept here so they're easy to update in one place)
# ---------------------------------------------------------------------------
def build_messages_stat(count: int) -> str:
    return f"""
<div class="stat-header">
  <span>Messages Processed</span>
  <div class="stat-icon" style="background:rgba(79,139,255,.15);color:#4F8BFF;">💬</div>
</div>
<div class="stat-val">{count}</div>
<div class="stat-desc">▲ +12% from last hour</div>
"""


def build_uploads_stat(count: int) -> str:
    return f"""
<div class="stat-header">
  <span>Uploads</span>
  <div class="stat-icon" style="background:rgba(255,183,3,.15);color:#FFB703;">📁</div>
</div>
<div class="stat-val">{count}</div>
<div class="stat-desc">▲ +3 images today</div>
"""
