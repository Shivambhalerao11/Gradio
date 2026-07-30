"""
backend/state.py
----------------
HTML fragment builders for reactive UI state pieces (badge, status card,
stat cards).  These produce HTML strings consumed by gr.HTML components.

No Gradio component construction here — only string output.
"""

from __future__ import annotations

from .config import DEMO_BOT_NAME, DEMO_BOT_ID


# ── Connection status badge ───────────────────────────────────────────────────

def build_badge_html(connected: bool) -> str:
    """Return the header status badge HTML."""
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


# ── Connection status card ────────────────────────────────────────────────────

def build_status_card_html(
    connected: bool,
    workspace: str = "",
    channel:   str = "",
    message:   str = "",
) -> str:
    """Return the left-panel connection status card HTML."""
    if connected:
        return (
            '<div style="background:rgba(46,204,113,.08);'
            'border:1px solid rgba(46,204,113,.25);'
            'padding:14px;border-radius:12px;font-size:13px;">'
            '<div style="color:#2ECC71;font-weight:600;margin-bottom:8px;">'
            '● Active Socket Listener</div>'
            f'<div style="color:#94A3B8;margin-bottom:4px;">'
            f'Workspace: <b style="color:#F8FAFC">{workspace}</b></div>'
            f'<div style="color:#94A3B8;margin-bottom:4px;">'
            f'Channel: <b style="color:#4F8BFF">{channel}</b></div>'
            f'<div style="color:#94A3B8;">'
            f'Bot Identity: <b style="color:#A29BFE">'
            f'{DEMO_BOT_NAME} ({DEMO_BOT_ID})</b></div>'
            '</div>'
        )

    body = message or (
        "Click <b>Connect Slack</b> to re-establish the WebSocket connection."
    )
    return (
        '<div style="background:rgba(255,94,87,.08);'
        'border:1px solid rgba(255,94,87,.25);'
        'padding:14px;border-radius:12px;font-size:13px;">'
        '<div style="color:#FF5E57;font-weight:600;margin-bottom:6px;">'
        '● Bot Offline</div>'
        f'<div style="color:#94A3B8;">{body}</div>'
        '</div>'
    )


# ── Statistics cards ──────────────────────────────────────────────────────────

def build_messages_stat(count: int) -> str:
    """Return HTML for the 'Messages Processed' stat card body."""
    return (
        '<div class="stat-header">'
        '<span>Messages Processed</span>'
        '<div class="stat-icon" style="background:rgba(79,139,255,.15);color:#4F8BFF;">💬</div>'
        '</div>'
        f'<div class="stat-val">{count}</div>'
        '<div class="stat-desc">▲ +12% from last hour</div>'
    )


def build_uploads_stat(count: int) -> str:
    """Return HTML for the 'Uploads' stat card body."""
    return (
        '<div class="stat-header">'
        '<span>Uploads</span>'
        '<div class="stat-icon" style="background:rgba(255,183,3,.15);color:#FFB703;">📁</div>'
        '</div>'
        f'<div class="stat-val">{count}</div>'
        '<div class="stat-desc">▲ +3 images today</div>'
    )
