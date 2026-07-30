"""
frontend/ui.py
--------------
Top-level UI assembler.

Responsibilities:
  1. Create the gr.Blocks container
  2. Call layout.build_layout() to place all components
  3. Wire every event binding (connect callbacks to handlers)
  4. Return the finished demo object to app.py

No business logic here.  No HTML string construction here.
"""

from __future__ import annotations

import gradio as gr

from backend.config  import APP_TITLE
from backend.handlers import (
    handle_connect,
    handle_disconnect,
    handle_send_message,
    handle_clear_chat,
    handle_clear_logs,
    handle_update_stats,
)

from .layout import build_layout
from .themes import DARK_THEME
from .styles import CUSTOM_CSS, LOG_AUTOSCROLL_JS


def build_demo(avatars: tuple) -> gr.Blocks:
    """
    Construct and return the complete Gradio Blocks application.

    Args:
        avatars: (user_avatar_path | None, bot_avatar_path | None)

    Returns:
        A fully-wired gr.Blocks instance ready for launch().
    """
    with gr.Blocks(
        title=f"{APP_TITLE} · Gradio",
        analytics_enabled=False,
    ) as demo:
        c = build_layout(avatars)

        # ── Connect ───────────────────────────────────────────────────────────
        c["connect_btn"].click(
            fn=handle_connect,
            inputs=[c["bot_token"], c["app_token"], c["workspace"], c["channel"], c["event_logs"]],
            outputs=[c["status_badge"], c["event_logs"], c["is_connected"], c["status_card"]],
        )

        # ── Disconnect ────────────────────────────────────────────────────────
        c["disconnect_btn"].click(
            fn=handle_disconnect,
            inputs=[c["event_logs"]],
            outputs=[c["status_badge"], c["event_logs"], c["is_connected"], c["status_card"]],
        )

        # ── Send message — button ─────────────────────────────────────────────
        _send_inputs  = [c["chat_input"], c["img_upload"], c["chatbot"], c["event_logs"],
                         c["msg_count"], c["upload_count"], c["is_connected"]]
        _send_outputs = [c["chatbot"], c["event_logs"], c["msg_count"], c["upload_count"], c["chat_input"]]

        c["send_btn"].click(
            fn=handle_send_message,
            inputs=_send_inputs,
            outputs=_send_outputs,
        ).then(
            fn=handle_update_stats,
            inputs=[c["msg_count"], c["upload_count"]],
            outputs=[c["msg_stat"], c["upload_stat"]],
        )

        # ── Send message — Enter key ──────────────────────────────────────────
        c["chat_input"].submit(
            fn=handle_send_message,
            inputs=_send_inputs,
            outputs=_send_outputs,
        ).then(
            fn=handle_update_stats,
            inputs=[c["msg_count"], c["upload_count"]],
            outputs=[c["msg_stat"], c["upload_stat"]],
        )

        # ── Clear chat ────────────────────────────────────────────────────────
        c["clear_chat_btn"].click(
            fn=handle_clear_chat,
            inputs=[c["event_logs"]],
            outputs=[c["chatbot"], c["event_logs"]],
        )

        # ── Clear logs ────────────────────────────────────────────────────────
        c["clear_logs_btn"].click(
            fn=handle_clear_logs,
            outputs=[c["event_logs"]],
        )

    return demo
