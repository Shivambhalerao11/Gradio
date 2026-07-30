"""
callbacks.py — All Gradio event-handler functions for Slack Bot Studio.

Every function here is pure Python; no Gradio imports required so they are
independently unit-testable.
"""

import datetime
from typing import Any

from config import (
    DEFAULT_WORKSPACE,
    DEFAULT_CHANNEL,
    DEMO_BOT_ID,
    DEMO_BOT_NAME,
    DEMO_USER_NAME,
    DEMO_CHANNEL,
    CAT_IMAGE_PATH,
)
from utils import build_log_entry, save_upload, build_messages_stat, build_uploads_stat

# ---------------------------------------------------------------------------
# Connection callbacks
# ---------------------------------------------------------------------------

def connect_slack(
    bot_token: str,
    app_token: str,
    workspace: str,
    channel: str,
    logs_html: str,
) -> tuple[str, str, bool, str]:
    """
    Returns:
        (status_badge_html, updated_logs_html, is_connected, status_card_html)
    """
    bot_token = (bot_token or "").strip()
    app_token = (app_token or "").strip()
    workspace = (workspace or DEFAULT_WORKSPACE).strip()
    channel   = (channel or DEFAULT_CHANNEL).strip()

    if not bot_token or not app_token:
        err = build_log_entry("ERROR", "Connection refused: Bot Token and App Token are required.")
        return (
            _badge_html(connected=False),
            logs_html + err,
            False,
            _status_card_html(
                connected=False,
                message="❌ Connection Failed: token fields cannot be empty.",
            ),
        )

    masked_token = bot_token[:10] + "..." if len(bot_token) > 10 else "***"
    new_logs = (
        logs_html
        + build_log_entry("CONNECT", f"Authenticating Bot Token <code>{masked_token}</code>")
        + build_log_entry("API",     f"POST slack.com/api/auth.test &rarr; 200 OK (team: {workspace})")
        + build_log_entry("CONNECT", "Socket Mode WebSocket connection established")
        + build_log_entry("SUCCESS", f"Bot active in <b>{channel}</b> on <b>{workspace}</b>")
    )

    return (
        _badge_html(connected=True),
        new_logs,
        True,
        _status_card_html(
            connected=True,
            workspace=workspace,
            channel=channel,
        ),
    )


def disconnect_slack(logs_html: str) -> tuple[str, str, bool, str]:
    """
    Returns:
        (status_badge_html, updated_logs_html, is_connected, status_card_html)
    """
    new_logs = logs_html + build_log_entry(
        "CONNECT", "Socket Mode connection closed by user request."
    )
    return (
        _badge_html(connected=False),
        new_logs,
        False,
        _status_card_html(connected=False),
    )


# ---------------------------------------------------------------------------
# Chat callbacks
# ---------------------------------------------------------------------------

def send_message(
    user_msg: str,
    img_input: Any,
    history: list,
    logs_html: str,
    msg_count: int,
    upload_count: int,
    is_connected: bool,
) -> tuple[list, str, int, int, str]:
    """
    Returns:
        (history, logs_html, msg_count, upload_count, cleared_input)

    History is a list of {"role": "user"|"assistant", "content": ...} dicts
    as required by Gradio 6 Chatbot.
    """
    user_msg = (user_msg or "").strip()

    if not user_msg and img_input is None:
        return history, logs_html, msg_count, upload_count, ""

    if not is_connected:
        err = build_log_entry("ERROR", "Cannot send: Slack bot is disconnected.")
        return history, logs_html + err, msg_count, upload_count, ""

    # ── Handle image upload ───────────────────────────────────────────────────
    img_path: str | None = None
    if img_input is not None:
        img_path = save_upload(img_input)
        upload_count += 1

    msg_count += 1

    # ── Build user content ────────────────────────────────────────────────────
    # In Gradio 6, text and file are separate messages in history
    new_messages: list[dict] = []

    if user_msg:
        new_messages.append({"role": "user", "content": user_msg})

    if img_path:
        # File content uses {"path": "..."} format in Gradio 6
        new_messages.append({"role": "user", "content": {"path": img_path}})

    # ── Generate bot reply ────────────────────────────────────────────────────
    now = datetime.datetime.now().strftime("%I:%M %p")
    if img_path:
        bot_content = (
            f"**AI Bot** APP · {now}\n\n"
            "Analyzing the uploaded image and generating a Gradio app…\n\n"
            "```python\nimport gradio as gr\n\n"
            "def analyze_image(img):\n"
            "    return \"Vision model processed input successfully!\"\n\n"
            "demo = gr.Interface(\n"
            "    fn=analyze_image,\n"
            "    inputs=gr.Image(type='pil'),\n"
            "    outputs='text',\n"
            ")\ndemo.launch()\n```"
        )
    else:
        bot_content = (
            f"Hi **{DEMO_USER_NAME}**! You mentioned me and said: `{user_msg}`\n\n"
            f"I am connected via **Gradio Slack Bot Studio** and ready to run your ML "
            f"models or custom Python functions directly inside {DEMO_CHANNEL}."
        )

    # ── Append event logs ─────────────────────────────────────────────────────
    new_logs = (
        logs_html
        + build_log_entry("EVENT", f"<code>app_mention</code> in <b>{DEMO_CHANNEL}</b> from <b>{DEMO_USER_NAME}</b>")
        + build_log_entry("API",   "POST slack.com/api/chat.postMessage &rarr; 200 OK (38 ms)")
    )

    new_history = history + new_messages + [
        {"role": "assistant", "content": bot_content},
    ]

    return new_history, new_logs, msg_count, upload_count, ""


def clear_chat(logs_html: str) -> tuple[list, str]:
    new_logs = logs_html + build_log_entry("EVENT", "Chat panel cleared by user.")
    return [], new_logs


def clear_logs() -> str:
    return build_log_entry("CONNECT", "Event log cleared.")


# ---------------------------------------------------------------------------
# Stats update helper
# ---------------------------------------------------------------------------

def update_stats(msg_count: int, upload_count: int) -> tuple[str, str]:
    """Returns (messages_stat_html, uploads_stat_html) for the bottom cards."""
    return build_messages_stat(msg_count), build_uploads_stat(upload_count)


# ---------------------------------------------------------------------------
# Private HTML builders
# ---------------------------------------------------------------------------

def _badge_html(connected: bool) -> str:
    if connected:
        return (
            '<div class="status-badge status-connected">'
            '<span class="status-dot"></span>Connected'
            '</div>'
        )
    return (
        '<div class="status-badge status-disconnected">'
        '<span class="status-dot"></span>Disconnected'
        '</div>'
    )


def _status_card_html(
    connected: bool,
    workspace: str = "",
    channel: str = "",
    message: str = "",
) -> str:
    if connected:
        return (
            '<div style="background:rgba(46,204,113,.08);border:1px solid rgba(46,204,113,.25);'
            'padding:14px;border-radius:12px;font-size:13px;">'
            '<div style="color:#2ECC71;font-weight:600;margin-bottom:8px;">● Active Socket Listener</div>'
            f'<div style="color:#94A3B8;margin-bottom:4px;">Workspace: <b style="color:#F8FAFC">{workspace}</b></div>'
            f'<div style="color:#94A3B8;margin-bottom:4px;">Channel: <b style="color:#4F8BFF">{channel}</b></div>'
            f'<div style="color:#94A3B8;">Bot Identity: <b style="color:#A29BFE">{DEMO_BOT_NAME} ({DEMO_BOT_ID})</b></div>'
            '</div>'
        )
    msg = message or "Click <b>Connect Slack</b> to re-establish the WebSocket connection."
    return (
        '<div style="background:rgba(255,94,87,.08);border:1px solid rgba(255,94,87,.25);'
        'padding:14px;border-radius:12px;font-size:13px;">'
        '<div style="color:#FF5E57;font-weight:600;margin-bottom:6px;">● Bot Offline</div>'
        f'<div style="color:#94A3B8;">{msg}</div>'
        '</div>'
    )
