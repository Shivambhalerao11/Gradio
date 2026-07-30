"""
config.py — Central configuration for Slack Bot Studio.
All tuneable constants and environment-variable-driven secrets live here.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Load .env if present; silently ignored if missing.

# ---------------------------------------------------------------------------
# App meta
# ---------------------------------------------------------------------------
APP_TITLE = "Slack Bot Studio"
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "7860"))
APP_SHARE = os.getenv("APP_SHARE", "false").lower() == "true"

# ---------------------------------------------------------------------------
# Default form values — pulled from env-vars so no secrets live in code
# ---------------------------------------------------------------------------
DEFAULT_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
DEFAULT_APP_TOKEN = os.getenv("SLACK_APP_TOKEN", "")
DEFAULT_WORKSPACE = os.getenv("SLACK_WORKSPACE", "ai-workplace")
DEFAULT_CHANNEL = os.getenv("SLACK_CHANNEL", "#ai-test")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ASSETS_DIR = "assets"
ICONS_DIR = "icons"
CAT_IMAGE_PATH = os.path.join(ASSETS_DIR, "cat_image.jpg")
BOT_AVATAR_PATH = os.path.join(ICONS_DIR, "bot_avatar.png")
USER_AVATAR_PATH = os.path.join(ICONS_DIR, "user_avatar.png")

# ---------------------------------------------------------------------------
# Simulated demo identity (purely cosmetic / demo purposes)
# ---------------------------------------------------------------------------
DEMO_BOT_ID = "B0BHJTV"
DEMO_BOT_NAME = "@AI Bot"
DEMO_USER_NAME = "@User"
DEMO_CHANNEL = "#ai-test"
