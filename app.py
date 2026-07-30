"""
app.py — Slack Bot Studio: entry-point and Gradio UI layout.

Run:  python app.py
Open: http://localhost:7860
"""

from __future__ import annotations

import os
from PIL import Image

# ── Bootstrap: ensure required directories and assets exist ──────────────────
os.makedirs("assets", exist_ok=True)
os.makedirs("icons",  exist_ok=True)

from config import (
    APP_TITLE, APP_HOST, APP_PORT, APP_SHARE,
    CAT_IMAGE_PATH, BOT_AVATAR_PATH, USER_AVATAR_PATH,
    DEFAULT_BOT_TOKEN, DEFAULT_APP_TOKEN, DEFAULT_WORKSPACE, DEFAULT_CHANNEL,
    DEMO_CHANNEL,
)

# Generate assets if they are missing
if not os.path.exists(CAT_IMAGE_PATH) or not os.path.exists(BOT_AVATAR_PATH):
    try:
        import create_assets  # noqa: F401 — side-effects only
    except Exception:
        img = Image.new("RGB", (400, 300), color=(30, 41, 59))
        img.save(CAT_IMAGE_PATH)

import gradio as gr

from theme import DARK_THEME, CUSTOM_CSS, LOG_AUTOSCROLL_JS
from callbacks import (
    connect_slack,
    disconnect_slack,
    send_message,
    clear_chat,
    clear_logs,
    update_stats,
    _badge_html,
    _status_card_html,
)
from utils import build_initial_logs, build_messages_stat, build_uploads_stat

# ── Initial demo state ───────────────────────────────────────────────────────
_INITIAL_MSG_COUNT    = 128
_INITIAL_UPLOAD_COUNT = 12

# Gradio 6 Chatbot: content must be str, {"path": "..."} for files,
# or a GradioComponent. Text + file = two separate messages.
INITIAL_CHAT: list[dict] = [
    {"role": "user",      "content": "@AI Bot make a similar gradio app"},
    {"role": "assistant", "content": (
        "Hi **@User**! You mentioned me and said: "
        "`@AI Bot make a similar gradio app`\n\n"
        "I can help you build custom Gradio applications and integrate "
        "them directly into your Slack workspace!"
    )},
    {"role": "user",      "content": "@AI Bot make similar Gradio App"},
    {"role": "user",      "content": {"path": CAT_IMAGE_PATH}},
    {"role": "assistant", "content": (
        "**AI Bot** APP · 5:10 PM\n\n"
        "Generating Gradio app based on the image…\n\n"
        "```python\nimport gradio as gr\n\n"
        "def respond(message, history):\n"
        "    return f\"Echo: {message}\"\n\n"
        "demo = gr.ChatInterface(fn=respond, title=\"Slack AI Bot\")\n"
        "demo.launch()\n```"
    )},
]

# ── Avatar paths ──────────────────────────────────────────────────────────────
_avatars = (
    USER_AVATAR_PATH if os.path.exists(USER_AVATAR_PATH) else None,
    BOT_AVATAR_PATH  if os.path.exists(BOT_AVATAR_PATH)  else None,
)

# ═══════════════════════════════════════════════════════════════════════════════
# Build Gradio Blocks UI
# NOTE: In Gradio 6, theme and css are passed to launch(), not Blocks().
# ═══════════════════════════════════════════════════════════════════════════════
with gr.Blocks(
    title=f"{APP_TITLE} · Gradio",
    analytics_enabled=False,
) as demo:

    # ── Persistent state ──────────────────────────────────────────────────────
    is_connected_state  = gr.State(value=True)
    msg_count_state     = gr.State(value=_INITIAL_MSG_COUNT)
    upload_count_state  = gr.State(value=_INITIAL_UPLOAD_COUNT)

    # ═══════════════════════════════════════════════════════════════════════════
    # 1. HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    with gr.Row(elem_classes=["header-card"]):
        with gr.Column(scale=8, min_width=0):
            gr.HTML("""
            <div style="display:flex;align-items:center;gap:16px;">
                <div style="
                    width:48px;height:48px;flex-shrink:0;
                    background:linear-gradient(135deg,#4F8BFF,#6C5CE7);
                    border-radius:14px;display:flex;align-items:center;
                    justify-content:center;font-size:26px;
                    box-shadow:0 4px 15px rgba(79,139,255,.35);">
                    🤖
                </div>
                <div>
                    <div style="
                        font-size:24px;font-weight:700;margin:0;
                        background:linear-gradient(135deg,#FFFFFF,#94A3B8);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                        Slack Bot from Gradio
                    </div>
                    <div style="font-size:13px;color:#94A3B8;margin-top:3px;">
                        Connect your Slack workspace with your Gradio AI application.
                    </div>
                </div>
            </div>
            """)

        with gr.Column(scale=2, min_width=180):
            status_badge = gr.HTML(
                value=_badge_html(connected=True),
                elem_id="status-badge-container",
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # 2. THREE-COLUMN DASHBOARD
    # ═══════════════════════════════════════════════════════════════════════════
    with gr.Row(equal_height=False):

        # ── LEFT: Slack Configuration ─────────────────────────────────────────
        with gr.Column(scale=3, min_width=0, elem_classes=["panel-card"]):
            gr.HTML("""
            <div class="panel-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                     stroke="#4F8BFF" stroke-width="2" stroke-linecap="round"
                     stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                Slack Configuration
            </div>
            """)

            bot_token_input = gr.Textbox(
                label="Bot Token",
                value=DEFAULT_BOT_TOKEN,
                type="password",
                placeholder="xoxb-your-bot-token",
            )
            app_token_input = gr.Textbox(
                label="App Token",
                value=DEFAULT_APP_TOKEN,
                type="password",
                placeholder="xapp-your-app-token",
            )
            workspace_input = gr.Textbox(
                label="Workspace Name",
                value=DEFAULT_WORKSPACE,
                placeholder="e.g. ai-workplace",
            )
            channel_input = gr.Textbox(
                label="Channel",
                value=DEFAULT_CHANNEL,
                placeholder="e.g. #ai-test",
            )

            with gr.Row():
                connect_btn    = gr.Button("Connect Slack", elem_classes=["btn-primary"],  scale=1)
                disconnect_btn = gr.Button("Disconnect",    elem_classes=["btn-danger"],   scale=1)

            status_card = gr.HTML(
                value=_status_card_html(
                    connected=True,
                    workspace=DEFAULT_WORKSPACE,
                    channel=DEFAULT_CHANNEL,
                )
            )

        # ── CENTER: Chat Interface ────────────────────────────────────────────
        with gr.Column(scale=6, min_width=0, elem_classes=["panel-card"]):
            gr.HTML(f"""
            <div class="panel-header" style="justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                         stroke="#6C5CE7" stroke-width="2" stroke-linecap="round"
                         stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                    <span>
                        Slack Channel Interface&nbsp;
                        <span style="color:#4F8BFF;font-weight:700;">{DEMO_CHANNEL}</span>
                    </span>
                </div>
                <span style="
                    font-size:11.5px;background:rgba(255,255,255,.06);
                    padding:4px 10px;border-radius:6px;color:#94A3B8;white-space:nowrap;">
                    User: @User
                </span>
            </div>
            """)

            chatbot = gr.Chatbot(
                value=INITIAL_CHAT,
                elem_id="chatbot-panel",
                layout="bubble",
                avatar_images=_avatars,
                show_label=False,
                height=460,
                render_markdown=True,
                autoscroll=True,
                sanitize_html=False,
            )

            with gr.Accordion("📎 Attach Image / Visual Input", open=False):
                img_upload = gr.Image(
                    label="Upload image",
                    type="filepath",
                    height=180,
                )

            with gr.Row():
                chat_input = gr.Textbox(
                    placeholder=f"Message {DEMO_CHANNEL}  (type @AI Bot to prompt)…",
                    show_label=False,
                    scale=7,
                    container=False,
                    lines=1,
                    max_lines=4,
                    autofocus=True,
                )
                send_btn = gr.Button("Send ↑", elem_classes=["btn-primary"], scale=2, min_width=80)

            clear_chat_btn = gr.Button("Clear Chat", elem_classes=["btn-secondary"])

        # ── RIGHT: Live Event Logs ────────────────────────────────────────────
        with gr.Column(scale=3, min_width=0, elem_classes=["panel-card"]):
            with gr.Row():
                gr.HTML("""
                <div class="panel-header" style="flex:1;margin-bottom:0;border-bottom:none;padding-bottom:0;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                         stroke="#2ECC71" stroke-width="2" stroke-linecap="round"
                         stroke-linejoin="round">
                        <polyline points="4 17 10 11 14 15 20 9"/>
                        <polyline points="14 9 20 9 20 15"/>
                    </svg>
                    Live Event Logs
                </div>
                """)
                clear_logs_btn = gr.Button(
                    "Clear",
                    elem_classes=["btn-secondary"],
                    size="sm",
                    scale=0,
                    min_width=60,
                )

            gr.HTML('<div style="height:1px;background:rgba(255,255,255,.06);margin:10px 0 12px;"></div>')

            event_logs = gr.HTML(
                value=build_initial_logs(),
                elem_id="log-terminal-wrap",
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. STATISTICS CARDS
    # ═══════════════════════════════════════════════════════════════════════════
    gr.HTML('<div style="height:20px;"></div>')

    with gr.Row():
        with gr.Column(elem_classes=["stat-card"]):
            msg_stat = gr.HTML(build_messages_stat(_INITIAL_MSG_COUNT))

        with gr.Column(elem_classes=["stat-card"]):
            gr.HTML("""
            <div class="stat-header">
              <span>Connected Users</span>
              <div class="stat-icon" style="background:rgba(108,92,231,.15);color:#6C5CE7;">👥</div>
            </div>
            <div class="stat-val">14</div>
            <div class="stat-desc">● 4 active in #ai-test</div>
            """)

        with gr.Column(elem_classes=["stat-card"]):
            gr.HTML("""
            <div class="stat-header">
              <span>API Latency</span>
              <div class="stat-icon" style="background:rgba(46,204,113,.15);color:#2ECC71;">⚡</div>
            </div>
            <div class="stat-val">38 ms</div>
            <div class="stat-desc">⚡ Optimal performance</div>
            """)

        with gr.Column(elem_classes=["stat-card"]):
            upload_stat = gr.HTML(build_uploads_stat(_INITIAL_UPLOAD_COUNT))

    # ═══════════════════════════════════════════════════════════════════════════
    # 4. EVENT BINDINGS
    # ═══════════════════════════════════════════════════════════════════════════

    # Connect
    connect_btn.click(
        fn=connect_slack,
        inputs=[bot_token_input, app_token_input, workspace_input, channel_input, event_logs],
        outputs=[status_badge, event_logs, is_connected_state, status_card],
    )

    # Disconnect
    disconnect_btn.click(
        fn=disconnect_slack,
        inputs=[event_logs],
        outputs=[status_badge, event_logs, is_connected_state, status_card],
    )

    # Send — button click
    send_btn.click(
        fn=send_message,
        inputs=[chat_input, img_upload, chatbot, event_logs,
                msg_count_state, upload_count_state, is_connected_state],
        outputs=[chatbot, event_logs, msg_count_state, upload_count_state, chat_input],
    ).then(
        fn=update_stats,
        inputs=[msg_count_state, upload_count_state],
        outputs=[msg_stat, upload_stat],
    )

    # Send — Enter key in textbox
    chat_input.submit(
        fn=send_message,
        inputs=[chat_input, img_upload, chatbot, event_logs,
                msg_count_state, upload_count_state, is_connected_state],
        outputs=[chatbot, event_logs, msg_count_state, upload_count_state, chat_input],
    ).then(
        fn=update_stats,
        inputs=[msg_count_state, upload_count_state],
        outputs=[msg_stat, upload_stat],
    )

    # Clear chat
    clear_chat_btn.click(
        fn=clear_chat,
        inputs=[event_logs],
        outputs=[chatbot, event_logs],
    )

    # Clear logs
    clear_logs_btn.click(
        fn=clear_logs,
        outputs=[event_logs],
    )


# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n🚀  {APP_TITLE} is running at  http://localhost:{APP_PORT}\n")
    demo.launch(
        server_name=APP_HOST,
        server_port=APP_PORT,
        share=APP_SHARE,
        show_error=True,
        theme=DARK_THEME,
        css=CUSTOM_CSS,
        js=LOG_AUTOSCROLL_JS,
    )
