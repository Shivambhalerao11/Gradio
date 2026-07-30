"""
backend/models.py
-----------------
Typed data structures (dataclasses / TypedDicts) used across the backend.
No Gradio imports. No UI code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AppState:
    """Mutable runtime state passed through Gradio State components."""
    is_connected:  bool = True
    msg_count:     int  = 0
    upload_count:  int  = 0


@dataclass
class ChatMessage:
    """A single normalised chat message."""
    role:    str        # "user" | "assistant"
    content: Any        # str | {"path": "..."} for files


@dataclass
class ConnectionResult:
    """Return value from connect / disconnect operations."""
    badge_html:       str
    logs_html:        str
    is_connected:     bool
    status_card_html: str


@dataclass
class SendMessageResult:
    """Return value from the send-message handler."""
    history:      list[dict]
    logs_html:    str
    msg_count:    int
    upload_count: int
    cleared_input: str = ""
