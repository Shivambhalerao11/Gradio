"""
app.py — Slack Bot Studio entry point.

Responsibilities (and ONLY these):
  1. Bootstrap directories and assets
  2. Load configuration
  3. Resolve avatar paths
  4. Build the Gradio demo via frontend.ui
  5. Launch

Run:  python app.py
Open: http://localhost:7860
"""

from __future__ import annotations

# ── 1. Bootstrap directories ──────────────────────────────────────────────────
# Must happen before any project import that touches the file system.
from utils.file_utils import ensure_directories

ensure_directories(
    "frontend/assets/images",
    "frontend/assets/icons",
    "frontend/assets/css",
    "frontend/assets/js",
    "data",
)

# ── 2. Load configuration ─────────────────────────────────────────────────────
from backend.config import (
    APP_TITLE,
    APP_HOST,
    APP_PORT,
    APP_SHARE,
    CAT_IMAGE_PATH,
    BOT_AVATAR_PATH,
    USER_AVATAR_PATH,
)

# ── 3. Generate missing assets ────────────────────────────────────────────────
import os
from PIL import Image

if not os.path.exists(CAT_IMAGE_PATH) or not os.path.exists(BOT_AVATAR_PATH):
    try:
        from create_assets import generate_all
        generate_all()
    except Exception:
        # Ultimate fallback — solid-colour placeholder so the app still starts
        os.makedirs(os.path.dirname(CAT_IMAGE_PATH), exist_ok=True)
        Image.new("RGB", (400, 300), color=(30, 41, 59)).save(CAT_IMAGE_PATH)

# ── 4. Resolve avatar paths ───────────────────────────────────────────────────
from utils.helpers import resolve_avatar_paths

avatars = resolve_avatar_paths(USER_AVATAR_PATH, BOT_AVATAR_PATH)

# ── 5. Build the Gradio demo ──────────────────────────────────────────────────
from frontend.ui     import build_demo
from frontend.themes import DARK_THEME
from frontend.styles import CUSTOM_CSS, LOG_AUTOSCROLL_JS

demo = build_demo(avatars)

# ── 6. Launch ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n🚀  {APP_TITLE} is running at  http://localhost:{APP_PORT}\n")
    demo.launch(
        server_name=APP_HOST,
        server_port=APP_PORT,
        share=APP_SHARE,
        show_error=True,
        theme=DARK_THEME,
        css=CUSTOM_CSS,
        js=LOG_AUTOSCROLL_JS,
    )
