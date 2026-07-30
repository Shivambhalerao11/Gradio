"""
utils/constants.py
------------------
Project-wide constants that are not environment-dependent.
"""

from __future__ import annotations

# Supported image extensions for upload validation
SUPPORTED_IMAGE_EXTENSIONS: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".gif", ".webp")

# Maximum upload file size in bytes (10 MB)
MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024

# Timestamp format used throughout the app
TIMESTAMP_FORMAT: str = "%H:%M:%S"
DISPLAY_TIME_FORMAT: str = "%I:%M %p"
