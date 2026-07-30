"""
create_assets.py
----------------
One-time asset generation script.
Run:  python create_assets.py

Generates all required images and SVG icons into frontend/assets/.
This script is also called automatically by app.py on first launch
if any assets are missing.
"""

from __future__ import annotations

import os

from backend.config   import ASSETS_DIR, ICONS_DIR, CAT_IMAGE_PATH, BOT_AVATAR_PATH, USER_AVATAR_PATH
from utils.file_utils import ensure_directories
from utils.image_utils import (
    create_cat_image,
    create_bot_avatar,
    create_user_avatar,
    SLACK_SVG,
)


def generate_all() -> None:
    ensure_directories(ASSETS_DIR, ICONS_DIR)

    # 1. Cat image
    create_cat_image().save(CAT_IMAGE_PATH)
    print(f"Saved {CAT_IMAGE_PATH}")

    # 2. Bot avatar
    create_bot_avatar().save(BOT_AVATAR_PATH)
    print(f"Saved {BOT_AVATAR_PATH}")

    # 3. User avatar
    create_user_avatar().save(USER_AVATAR_PATH)
    print(f"Saved {USER_AVATAR_PATH}")

    # 4. Slack SVG
    slack_path = os.path.join(ICONS_DIR, "slack.svg")
    with open(slack_path, "w", encoding="utf-8") as fh:
        fh.write(SLACK_SVG)
    print(f"Saved {slack_path}")


if __name__ == "__main__":
    generate_all()
