"""
backend/handlers.py
-------------------
Gradio event-handler functions.

Each handler:
  - Receives raw Gradio component values as inputs
  - Delegates all business logic to services / state modules
  - Returns plain Python values back to Gradio outputs

No UI construction here.  Handlers are the only layer that is
allowed to touch both the Gradio contract (tuples) and backend services.
"""

from __future__ import annotations

from typing import Any

from .config import DEFAULT_WORKSPACE, DEFAULT_CHANNEL
from .services import (
    service_connect,
    service_disconnect,
    service_generate_reply,
    service_append_chat_logs,
)
from .state import (
    build_badge_html,
    build_status_card_html,
    build_messages_stat,
    build_uploads_stat,
)
from .logger import build_log_entry
from .validation import validate_message
from utils.file_utils import save_upload as _save_upload
from .config import ASSETS_DIR, CAT_IMAGE_PATH


def _handle_upload(img_input) -> str | None:
    """Wrap save_upload with project-specific paths."""
    if img_input is None:
        return None
    return _save_upload(img_input, assets_dir=ASSETS_DIR, fallback_path=CAT_IMAGE_PATH)


# ── Connection handlers ───────────────────────────────────────────────────────

def handle_connect(
    bot_token: str,
    app_token: str,
    workspace: str,
    channel:   str,
    logs_html: str,
) -> tuple[str, str, bool, str]:
    """
    Gradio handler for the Connect button.

    Returns:
        (badge_html, logs_html, is_connected, status_card_html)
    """
    workspace = (workspace or DEFAULT_WORKSPACE).strip()
    channel   = (channel   or DEFAULT_CHANNEL).strip()

    success, new_logs, error_msg = service_connect(
        bot_token, app_token, workspace, channel, logs_html
    )

    if not success:
        return (
            build_badge_html(connected=False),
            new_logs,
            False,
            build_status_card_html(
                connected=False,
                message=f"❌ Connection Failed: {error_msg}",
            ),
        )

    return (
        build_badge_html(connected=True),
        new_logs,
        True,
        build_status_card_html(connected=True, workspace=workspace, channel=channel),
    )


def handle_disconnect(logs_html: str) -> tuple[str, str, bool, str]:
    """
    Gradio handler for the Disconnect button.

    Returns:
        (badge_html, logs_html, is_connected, status_card_html)
    """
    new_logs = service_disconnect(logs_html)
    return (
        build_badge_html(connected=False),
        new_logs,
        False,
        build_status_card_html(connected=False),
    )


# ── Chat handlers ─────────────────────────────────────────────────────────────

def handle_send_message(
    user_msg:     str,
    img_input:    Any,
    history:      list,
    logs_html:    str,
    msg_count:    int,
    upload_count: int,
    is_connected: bool,
) -> tuple[list, str, int, int, str]:
    """
    Gradio handler for Send button / Enter key.

    Returns:
        (history, logs_html, msg_count, upload_count, cleared_input)
    """
    if not validate_message(user_msg, img_input):
        return history, logs_html, msg_count, upload_count, ""

    if not is_connected:
        err = build_log_entry("ERROR", "Cannot send: Slack bot is disconnected.")
        return history, logs_html + err, msg_count, upload_count, ""

    # ── Process image upload ──────────────────────────────────────────────────
    img_path: str | None = None
    if img_input is not None:
        img_path = _handle_upload(img_input)
        upload_count += 1

    msg_count += 1

    # ── Build new user message(s) for Gradio 6 Chatbot ───────────────────────
    # Gradio 6 requires {"role", "content"} dicts.
    # Text + file → two separate entries (Gradio 6 does not support combined).
    new_user_msgs: list[dict] = []
    if (user_msg or "").strip():
        new_user_msgs.append({"role": "user", "content": user_msg.strip()})
    if img_path:
        new_user_msgs.append({"role": "user", "content": {"path": img_path}})

    # ── Generate bot reply ────────────────────────────────────────────────────
    bot_content = service_generate_reply(
        user_msg=(user_msg or "").strip(),
        has_image=img_path is not None,
    )

    # ── Update logs ───────────────────────────────────────────────────────────
    new_logs = service_append_chat_logs(logs_html)

    new_history = history + new_user_msgs + [
        {"role": "assistant", "content": bot_content}
    ]

    return new_history, new_logs, msg_count, upload_count, ""


def handle_clear_chat(logs_html: str) -> tuple[list, str]:
    """Gradio handler for the Clear Chat button."""
    new_logs = logs_html + build_log_entry("EVENT", "Chat panel cleared by user.")
    return [], new_logs


def handle_clear_logs() -> str:
    """Gradio handler for the Clear Logs button."""
    return build_log_entry("CONNECT", "Event log cleared.")


# ── Stats handler ─────────────────────────────────────────────────────────────

def handle_update_stats(msg_count: int, upload_count: int) -> tuple[str, str]:
    """Return refreshed (messages_stat_html, uploads_stat_html)."""
    return build_messages_stat(msg_count), build_uploads_stat(upload_count)
