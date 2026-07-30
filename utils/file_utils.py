"""
utils/file_utils.py
-------------------
File system helpers: directory bootstrap, asset generation trigger,
and upload persistence.
"""

from __future__ import annotations

import os
import time


def ensure_directories(*paths: str) -> None:
    """Create one or more directories (and parents) if they do not exist."""
    for path in paths:
        os.makedirs(path, exist_ok=True)


def save_upload(img_input, assets_dir: str, fallback_path: str) -> str:
    """
    Persist an uploaded image to disk and return its path.

    Accepts:
        - A filepath string (returned as-is if it exists)
        - A PIL.Image.Image instance
        - A numpy ndarray (from gr.Image type="numpy")

    Returns:
        Path to the saved file, or ``fallback_path`` on any failure.
    """
    from PIL import Image  # local import — PIL only needed at call time

    ensure_directories(assets_dir)
    dest = os.path.join(assets_dir, f"upload_{int(time.time())}.jpg")

    try:
        if isinstance(img_input, str):
            return img_input if os.path.exists(img_input) else fallback_path

        if isinstance(img_input, Image.Image):
            img_input.convert("RGB").save(dest)
            return dest

        # numpy array
        try:
            import numpy as np
            if isinstance(img_input, np.ndarray):
                Image.fromarray(img_input).convert("RGB").save(dest)
                return dest
        except ImportError:
            pass

    except Exception:
        pass

    return fallback_path
