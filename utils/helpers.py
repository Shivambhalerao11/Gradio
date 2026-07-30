"""
utils/helpers.py
----------------
Miscellaneous helpers that do not belong to a more specific module.
"""

from __future__ import annotations

import os


def resolve_avatar_paths(
    user_path: str,
    bot_path: str,
) -> tuple[str | None, str | None]:
    """
    Return (user_avatar, bot_avatar) paths, replacing missing files with None.
    Gradio accepts None as "use default avatar".
    """
    return (
        user_path if os.path.exists(user_path) else None,
        bot_path  if os.path.exists(bot_path)  else None,
    )
