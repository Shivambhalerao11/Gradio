"""
backend/validation.py
---------------------
Input validation helpers.  All validation logic lives here so that
callback functions stay clean and never duplicate guard clauses.
"""

from __future__ import annotations


def validate_tokens(bot_token: str, app_token: str) -> str | None:
    """
    Validate Slack token inputs.

    Returns:
        None if valid, or an error message string if invalid.
    """
    if not (bot_token or "").strip():
        return "Bot Token is required."
    if not (app_token or "").strip():
        return "App Token is required."
    if not bot_token.strip().startswith("xoxb-"):
        return "Bot Token must start with 'xoxb-'."
    if not app_token.strip().startswith("xapp-"):
        return "App Token must start with 'xapp-'."
    return None


def validate_message(user_msg: str, img_input) -> bool:
    """Return True if there is any content to send."""
    return bool((user_msg or "").strip()) or img_input is not None
