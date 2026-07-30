"""
backend/config.py
-----------------
Central configuration for Slack Bot Studio.
All tuneable constants and environment-variable-driven secrets live here.
"""

from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()  # Load .env if present; silently ignored if missing.

# ── App meta ──────────────────────────────────────────────────────────────────
APP_TITLE: str = "Slack Bot Studio"
APP_HOST:  str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT:  int = int(os.getenv("APP_PORT", "7860"))
APP_SHARE: bool = os.getenv("APP_SHARE", "false").lower() == "true"

# ── Slack credentials (from env — never hard-coded) ───────────────────────────
DEFAULT_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
DEFAULT_APP_TOKEN: str = os.getenv("SLACK_APP_TOKEN", "")
DEFAULT_WORKSPACE: str = os.getenv("SLACK_WORKSPACE", "ai-workplace")
DEFAULT_CHANNEL:   str = os.getenv("SLACK_CHANNEL",   "#ai-test")

# ── File system paths ─────────────────────────────────────────────────────────
ASSETS_DIR:      str = os.path.join("frontend", "assets", "images")
ICONS_DIR:       str = os.path.join("frontend", "assets", "icons")
DATA_DIR:        str = "data"
CAT_IMAGE_PATH:  str = os.path.join(ASSETS_DIR, "cat_image.jpg")
BOT_AVATAR_PATH: str = os.path.join(ICONS_DIR,  "bot_avatar.png")
USER_AVATAR_PATH: str = os.path.join(ICONS_DIR, "user_avatar.png")

# ── Demo identity (cosmetic / demo only) ──────────────────────────────────────
DEMO_BOT_ID:   str = "B0BHJTV"
DEMO_BOT_NAME: str = "@AI Bot"
DEMO_USER_NAME: str = "@User"
DEMO_CHANNEL:  str = "#ai-test"

# ── Initial counter seeds ─────────────────────────────────────────────────────
INITIAL_MSG_COUNT:    int = 128
INITIAL_UPLOAD_COUNT: int = 12
