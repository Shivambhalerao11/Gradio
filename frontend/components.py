"""
frontend/components.py
----------------------
Reusable HTML fragment factories for recurring UI pieces.
Returns strings only — no gr.* component construction here.
"""

from __future__ import annotations


def header_logo_html() -> str:
    """The robot logo + title + subtitle block in the header."""
    return """
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
"""


def config_panel_header_html() -> str:
    """Left-panel section header for Slack Configuration."""
    return """
<div class="panel-header">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
         stroke="#4F8BFF" stroke-width="2" stroke-linecap="round"
         stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
    Slack Configuration
</div>
"""


def chat_panel_header_html(channel: str) -> str:
    """Center-panel section header showing the active channel."""
    return f"""
<div class="panel-header" style="justify-content:space-between;">
    <div style="display:flex;align-items:center;gap:10px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
             stroke="#6C5CE7" stroke-width="2" stroke-linecap="round"
             stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        <span>
            Slack Channel Interface&nbsp;
            <span style="color:#4F8BFF;font-weight:700;">{channel}</span>
        </span>
    </div>
    <span style="
        font-size:11.5px;background:rgba(255,255,255,.06);
        padding:4px 10px;border-radius:6px;color:#94A3B8;white-space:nowrap;">
        User: @User
    </span>
</div>
"""


def logs_panel_header_html() -> str:
    """Right-panel section header for Live Event Logs (title only)."""
    return """
<div class="panel-header" style="flex:1;margin-bottom:0;border-bottom:none;padding-bottom:0;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
         stroke="#2ECC71" stroke-width="2" stroke-linecap="round"
         stroke-linejoin="round">
        <polyline points="4 17 10 11 14 15 20 9"/>
        <polyline points="14 9 20 9 20 15"/>
    </svg>
    Live Event Logs
</div>
"""


def divider_html() -> str:
    """A subtle horizontal rule used inside panels."""
    return '<div style="height:1px;background:rgba(255,255,255,.06);margin:10px 0 12px;"></div>'


def spacer_html(height: int = 20) -> str:
    """Vertical spacer of arbitrary pixel height."""
    return f'<div style="height:{height}px;"></div>'


def users_stat_html() -> str:
    """Static HTML for the 'Connected Users' stat card (not reactive)."""
    return """
<div class="stat-header">
  <span>Connected Users</span>
  <div class="stat-icon" style="background:rgba(108,92,231,.15);color:#6C5CE7;">👥</div>
</div>
<div class="stat-val">14</div>
<div class="stat-desc">● 4 active in #ai-test</div>
"""


def latency_stat_html() -> str:
    """Static HTML for the 'API Latency' stat card (not reactive)."""
    return """
<div class="stat-header">
  <span>API Latency</span>
  <div class="stat-icon" style="background:rgba(46,204,113,.15);color:#2ECC71;">⚡</div>
</div>
<div class="stat-val">38 ms</div>
<div class="stat-desc">⚡ Optimal performance</div>
"""
