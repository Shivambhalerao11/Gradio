# 🤖 Slack Bot Studio — Gradio AI Dashboard

A **production-grade** developer dashboard built with **Gradio 6** following a clean **Frontend / Backend** architecture.

![Python](https://img.shields.io/badge/Python-3.10%2B-3b82f6?style=flat-square)
![Gradio](https://img.shields.io/badge/Gradio-6.x-6366F1?style=flat-square)
![Architecture](https://img.shields.io/badge/Architecture-Frontend%2FBackend-10b981?style=flat-square)
![Theme](https://img.shields.io/badge/Theme-Dark%20Glassmorphism-1e293b?style=flat-square)

---

## Architecture Overview

```
app.py                      ← Entry point only (bootstrap + launch)
│
├── frontend/               ← UI layer — NO business logic
│   ├── ui.py               ← Assembles demo, wires all event bindings
│   ├── layout.py           ← Declares every gr.* component and layout
│   ├── components.py       ← Reusable HTML fragment factories
│   ├── styles.py           ← All CSS + JavaScript (CUSTOM_CSS, LOG_AUTOSCROLL_JS)
│   ├── themes.py           ← Gradio theme definition (DARK_THEME)
│   └── assets/
│       ├── images/         ← Sample images + runtime uploads
│       ├── icons/          ← Bot/user avatars + Slack SVG
│       ├── css/            ← (reserved for external CSS files)
│       └── js/             ← (reserved for external JS files)
│
├── backend/                ← Logic layer — NO Gradio component construction
│   ├── config.py           ← All constants + env-var driven settings
│   ├── handlers.py         ← Gradio event handler functions (thin wrappers)
│   ├── services.py         ← Business logic (connect, disconnect, reply gen)
│   ├── state.py            ← Reactive HTML builders (badge, status card, stats)
│   ├── logger.py           ← Log entry HTML builder + initial log factory
│   ├── chatbot.py          ← Initial demo chat history factory
│   ├── models.py           ← Typed dataclasses (AppState, ChatMessage, …)
│   └── validation.py       ← Input validation (tokens, message content)
│
├── utils/                  ← Shared utilities — no Gradio, no business logic
│   ├── constants.py        ← App-wide constants (formats, limits)
│   ├── file_utils.py       ← Directory bootstrap + image persistence
│   ├── image_utils.py      ← PIL image generators (cat, bot/user avatars, SVG)
│   └── helpers.py          ← Miscellaneous helpers (avatar path resolution)
│
├── data/                   ← Runtime data directory (gitignored except .gitkeep)
├── create_assets.py        ← One-time asset generator script
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Separation of Concerns

| Layer | Allowed | Forbidden |
|---|---|---|
| `frontend/` | `gr.*` components, HTML strings, CSS, JS, layout | Business logic, API calls, file I/O |
| `backend/` | Logic, validation, state HTML strings | `gr.*` imports, UI construction |
| `utils/` | File helpers, image generators, constants | Gradio, backend services |
| `app.py` | Bootstrap, import, `demo.launch()` | Layout, logic, styling |

---

## Features

- **Header** — Title + live animated status badge (Connected / Disconnected)
- **Left Panel** — Slack Configuration (tokens, workspace, channel, connect/disconnect)
- **Center Panel** — Full Slack-style chat with Markdown, code blocks, image uploads
- **Right Panel** — Live Event Log terminal with colour-coded badges and auto-scroll
- **Stats Bar** — Four live metric cards (Messages, Users, Latency, Uploads)

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure secrets (optional)
cp .env.example .env
# Edit .env with your real Slack tokens

# 3. Run
python app.py
```

Open **http://localhost:7860**

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SLACK_BOT_TOKEN` | _(empty)_ | Slack bot token (`xoxb-…`) |
| `SLACK_APP_TOKEN` | _(empty)_ | Slack app token (`xapp-…`) |
| `SLACK_WORKSPACE` | `ai-workplace` | Workspace display name |
| `SLACK_CHANNEL` | `#ai-test` | Default channel |
| `APP_HOST` | `0.0.0.0` | Server bind address |
| `APP_PORT` | `7860` | Server port |
| `APP_SHARE` | `false` | Gradio public share link |

---

## Known Limitations

- Slack connection is **simulated** — no real `slack_bolt` WebSocket. Wire `backend/services.py` to `slack_bolt` for production use.
- "Connected Users" and "API Latency" cards display static demo values.
