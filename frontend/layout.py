"""
frontend/layout.py
------------------
Assembles every Gradio component into the full page layout.

Rules:
  ✓ Only gr.* component creation and layout (Rows, Columns, HTML, etc.)
  ✓ No business logic
  ✓ No direct import from backend.services or backend.handlers
  ✓ Returns component references needed for event binding in ui.py
"""

from __future__ import annotations

import gradio as gr

from backend.config   import DEFAULT_BOT_TOKEN, DEFAULT_APP_TOKEN, DEFAULT_WORKSPACE, DEFAULT_CHANNEL, DEMO_CHANNEL
from backend.state    import build_badge_html, build_status_card_html, build_messages_stat, build_uploads_stat
from backend.logger   import build_initial_logs
from backend.chatbot  import build_initial_chat_history
from backend.config   import INITIAL_MSG_COUNT, INITIAL_UPLOAD_COUNT

from .components import (
    header_logo_html,
    config_panel_header_html,
    chat_panel_header_html,
    logs_panel_header_html,
    divider_html,
    spacer_html,
    users_stat_html,
    latency_stat_html,
)


def build_layout(avatars: tuple) -> dict:
    """
    Declare all Gradio components inside the active gr.Blocks context.

    Args:
        avatars: (user_avatar_path_or_None, bot_avatar_path_or_None)

    Returns:
        A dict of named component references consumed by ui.py for
        event binding.
    """
    components: dict = {}

    # ── Persistent state ──────────────────────────────────────────────────────
    components["is_connected"]  = gr.State(value=True)
    components["msg_count"]     = gr.State(value=INITIAL_MSG_COUNT)
    components["upload_count"]  = gr.State(value=INITIAL_UPLOAD_COUNT)

    # ═════════════════════════════════════════════════════════════════════════
    # HEADER
    # ═════════════════════════════════════════════════════════════════════════
    with gr.Row(elem_classes=["header-card"]):
        with gr.Column(scale=8, min_width=0):
            gr.HTML(header_logo_html())
        with gr.Column(scale=2, min_width=180):
            components["status_badge"] = gr.HTML(
                value=build_badge_html(connected=True),
                elem_id="status-badge-container",
            )

    # ═════════════════════════════════════════════════════════════════════════
    # THREE-COLUMN DASHBOARD
    # ═════════════════════════════════════════════════════════════════════════
    with gr.Row(equal_height=False):

        # ── LEFT: Slack Configuration ─────────────────────────────────────────
        with gr.Column(scale=3, min_width=0, elem_classes=["panel-card"]):
            gr.HTML(config_panel_header_html())

            components["bot_token"] = gr.Textbox(
                label="Bot Token",
                value=DEFAULT_BOT_TOKEN,
                type="password",
                placeholder="xoxb-your-bot-token",
            )
            components["app_token"] = gr.Textbox(
                label="App Token",
                value=DEFAULT_APP_TOKEN,
                type="password",
                placeholder="xapp-your-app-token",
            )
            components["workspace"] = gr.Textbox(
                label="Workspace Name",
                value=DEFAULT_WORKSPACE,
                placeholder="e.g. ai-workplace",
            )
            components["channel"] = gr.Textbox(
                label="Channel",
                value=DEFAULT_CHANNEL,
                placeholder="e.g. #ai-test",
            )

            with gr.Row():
                components["connect_btn"]    = gr.Button("Connect Slack", elem_classes=["btn-primary"],  scale=1)
                components["disconnect_btn"] = gr.Button("Disconnect",    elem_classes=["btn-danger"],   scale=1)

            components["status_card"] = gr.HTML(
                value=build_status_card_html(
                    connected=True,
                    workspace=DEFAULT_WORKSPACE,
                    channel=DEFAULT_CHANNEL,
                )
            )

        # ── CENTER: Chat Interface ────────────────────────────────────────────
        with gr.Column(scale=6, min_width=0, elem_classes=["panel-card"]):
            gr.HTML(chat_panel_header_html(DEMO_CHANNEL))

            components["chatbot"] = gr.Chatbot(
                value=build_initial_chat_history(),
                elem_id="chatbot-panel",
                layout="bubble",
                avatar_images=avatars,
                show_label=False,
                height=460,
                render_markdown=True,
                autoscroll=True,
                sanitize_html=False,
            )

            with gr.Accordion("📎 Attach Image / Visual Input", open=False):
                components["img_upload"] = gr.Image(
                    label="Upload image",
                    type="filepath",
                    height=180,
                )

            with gr.Row():
                components["chat_input"] = gr.Textbox(
                    placeholder=f"Message {DEMO_CHANNEL}  (type @AI Bot to prompt)…",
                    show_label=False,
                    scale=7,
                    container=False,
                    lines=1,
                    max_lines=4,
                    autofocus=True,
                )
                components["send_btn"] = gr.Button(
                    "Send ↑", elem_classes=["btn-primary"], scale=2, min_width=80
                )

            components["clear_chat_btn"] = gr.Button(
                "Clear Chat", elem_classes=["btn-secondary"]
            )

        # ── RIGHT: Live Event Logs ────────────────────────────────────────────
        with gr.Column(scale=3, min_width=0, elem_classes=["panel-card"]):
            with gr.Row():
                gr.HTML(logs_panel_header_html())
                components["clear_logs_btn"] = gr.Button(
                    "Clear",
                    elem_classes=["btn-secondary"],
                    size="sm",
                    scale=0,
                    min_width=60,
                )

            gr.HTML(divider_html())

            components["event_logs"] = gr.HTML(
                value=build_initial_logs(),
                elem_id="log-terminal-wrap",
            )

    # ═════════════════════════════════════════════════════════════════════════
    # STATISTICS CARDS
    # ═════════════════════════════════════════════════════════════════════════
    gr.HTML(spacer_html(20))

    with gr.Row():
        with gr.Column(elem_classes=["stat-card"]):
            components["msg_stat"] = gr.HTML(build_messages_stat(INITIAL_MSG_COUNT))

        with gr.Column(elem_classes=["stat-card"]):
            gr.HTML(users_stat_html())

        with gr.Column(elem_classes=["stat-card"]):
            gr.HTML(latency_stat_html())

        with gr.Column(elem_classes=["stat-card"]):
            components["upload_stat"] = gr.HTML(build_uploads_stat(INITIAL_UPLOAD_COUNT))

    return components
