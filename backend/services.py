"""
backend/services.py
-------------------
Business-logic services for Slack Bot Studio.

Each service is a pure function (or thin class) that performs one
well-defined operation.  No Gradio imports.  No UI code.
"""

from __future__ import annotations

import datetime

from .config import (
    DEFAULT_WORKSPACE,
    DEFAULT_CHANNEL,
    DEMO_BOT_ID,
    DEMO_BOT_NAME,
    DEMO_USER_NAME,
    DEMO_CHANNEL,
)
from .logger import build_log_entry
from .validation import validate_tokens


# ── Connection service ────────────────────────────────────────────────────────

def service_connect(
    bot_token: str,
    app_token: str,
    workspace: str,
    channel: str,
    logs_html: str,
) -> tuple[bool, str, str]:
    """
    Validate tokens and simulate a Slack Socket Mode connection.

    Returns:
        (success, updated_logs_html, error_message)
    """
    bot_token = (bot_token or "").strip()
    app_token = (app_token or "").strip()
    workspace = (workspace or DEFAULT_WORKSPACE).strip()
    channel   = (channel   or DEFAULT_CHANNEL).strip()

    error = validate_tokens(bot_token, app_token)
    if error:
        err_log = build_log_entry("ERROR", f"Connection refused: {error}")
        return False, logs_html + err_log, error

    masked = bot_token[:10] + "..." if len(bot_token) > 10 else "***"
    new_logs = (
        logs_html
        + build_log_entry("CONNECT", f"Authenticating Bot Token <code>{masked}</code>")
        + build_log_entry("API",     f"POST slack.com/api/auth.test &rarr; 200 OK (team: {workspace})")
        + build_log_entry("CONNECT", "Socket Mode WebSocket connection established")
        + build_log_entry("SUCCESS", f"Bot active in <b>{channel}</b> on <b>{workspace}</b>")
    )
    return True, new_logs, ""


def service_disconnect(logs_html: str) -> str:
    """Simulate a graceful Socket Mode disconnect. Returns updated logs."""
    return logs_html + build_log_entry(
        "CONNECT", "Socket Mode connection closed by user request."
    )


# ── Chat service ──────────────────────────────────────────────────────────────

def service_generate_reply(user_msg: str, has_image: bool) -> str:
    """
    Generate the bot's reply text.

    Args:
        user_msg:  The user's text message (may be empty for image-only sends).
        has_image: Whether an image was attached to this message.

    Returns:
        Markdown-formatted bot reply string.
    """
    now = datetime.datetime.now().strftime("%I:%M %p")

    if has_image:
        return (
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

    return (
        f"Hi **{DEMO_USER_NAME}**! You mentioned me and said: `{user_msg}`\n\n"
        f"I am connected via **Gradio Slack Bot Studio** and ready to run your ML "
        f"models or custom Python functions directly inside {DEMO_CHANNEL}."
    )


def service_append_chat_logs(logs_html: str) -> str:
    """Append the two standard event log entries that follow every message."""
    return (
        logs_html
        + build_log_entry(
            "EVENT",
            f"<code>app_mention</code> in <b>{DEMO_CHANNEL}</b> "
            f"from <b>{DEMO_USER_NAME}</b>",
        )
        + build_log_entry(
            "API",
            "POST slack.com/api/chat.postMessage &rarr; 200 OK (38 ms)",
        )
    )
