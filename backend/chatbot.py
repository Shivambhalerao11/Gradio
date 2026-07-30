"""
backend/chatbot.py
------------------
Factory that builds the initial Gradio 6 Chatbot history (the demo
conversation shown when the app first loads).

Kept separate so the demo data is easy to update without touching
layout or handler code.
"""

from __future__ import annotations

import os

from .config import CAT_IMAGE_PATH


def build_initial_chat_history() -> list[dict]:
    """
    Return the demo conversation pre-loaded into the Chatbot component.

    Gradio 6 format:  list of {"role": "user"|"assistant", "content": ...}
    Files use {"path": "..."} as content.
    """
    history: list[dict] = [
        {
            "role": "user",
            "content": "@AI Bot make a similar gradio app",
        },
        {
            "role": "assistant",
            "content": (
                "Hi **@User**! You mentioned me and said: "
                "`@AI Bot make a similar gradio app`\n\n"
                "I can help you build custom Gradio applications and integrate "
                "them directly into your Slack workspace!"
            ),
        },
        {
            "role": "user",
            "content": "@AI Bot make similar Gradio App",
        },
    ]

    # Only include the image message if the asset actually exists
    if os.path.exists(CAT_IMAGE_PATH):
        history.append({"role": "user", "content": {"path": CAT_IMAGE_PATH}})

    history.append(
        {
            "role": "assistant",
            "content": (
                "**AI Bot** APP · 5:10 PM\n\n"
                "Generating Gradio app based on the image…\n\n"
                "```python\nimport gradio as gr\n\n"
                "def respond(message, history):\n"
                "    return f\"Echo: {message}\"\n\n"
                "demo = gr.ChatInterface(fn=respond, title=\"Slack AI Bot\")\n"
                "demo.launch()\n```"
            ),
        }
    )

    return history
