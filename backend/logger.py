"""
backend/logger.py
-----------------
Centralised HTML log-entry builder for the Live Event Logs terminal.
All log formatting logic lives here — nowhere else.
"""

from __future__ import annotations

import datetime

# Badge category → CSS class mapping
_BADGE_MAP: dict[str, str] = {
    "CONNECT": "badge-info",
    "API":     "badge-api",
    "SUCCESS": "badge-success",
    "EVENT":   "badge-event",
    "ERROR":   "badge-error",
}


def build_log_entry(category: str, message: str) -> str:
    """
    Return a single HTML log line with a live timestamp and colour-coded badge.

    Args:
        category: One of CONNECT | API | SUCCESS | EVENT | ERROR
        message:  HTML-safe message body (may contain <b>, <code> etc.)

    Returns:
        An HTML <div> string ready to append to the log terminal.
    """
    ts        = datetime.datetime.now().strftime("%H:%M:%S")
    badge_cls = _BADGE_MAP.get(category.upper(), "badge-info")
    return (
        f'<div class="log-entry">'
        f'<span class="log-time">[{ts}]</span> '
        f'<span class="log-badge {badge_cls}">{category.upper()}</span> '
        f'{message}'
        f'</div>\n'
    )


def build_initial_logs() -> str:
    """Return the four startup log entries shown when the app first loads."""
    return "".join([
        build_log_entry("CONNECT", "Initializing Slack Socket Mode client…"),
        build_log_entry("API",     "auth.test &rarr; 200 OK (team: ai-workplace, bot_id: B0BHJTV)"),
        build_log_entry("SUCCESS", "Connected to Slack Workspace <b>ai-workplace</b>"),
        build_log_entry("EVENT",   "Subscribed to <b>#ai-test</b> for <b>@AI Bot</b> mentions"),
    ])
