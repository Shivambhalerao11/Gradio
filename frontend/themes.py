"""
frontend/themes.py
------------------
Gradio theme definition for Slack Bot Studio.
Only theming — no CSS, no JS, no layout.
"""

from __future__ import annotations

import gradio as gr

DARK_THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.blue,
    secondary_hue=gr.themes.colors.purple,
    neutral_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
).set(
    body_background_fill="#0B1020",
    body_text_color="#F8FAFC",
    block_background_fill="#141B2D",
    block_border_color="rgba(255,255,255,0.08)",
    block_label_text_color="#94A3B8",
    input_background_fill="#0F172A",
    input_border_color="rgba(255,255,255,0.10)",
    input_placeholder_color="#475569",
    button_primary_background_fill="linear-gradient(135deg,#4F8BFF,#6C5CE7)",
    button_primary_text_color="#FFFFFF",
    button_secondary_background_fill="rgba(255,255,255,0.05)",
    button_secondary_text_color="#94A3B8",
    border_color_primary="rgba(255,255,255,0.08)",
)
