# 🤖 Slack Bot Studio — Gradio AI Dashboard

A production-grade developer dashboard built with **Gradio 6** to connect Slack workspaces with Python AI / ML applications.

![Theme](https://img.shields.io/badge/Theme-Modern%20Dark%20Mode-1e293b?style=flat-square)
![Framework](https://img.shields.io/badge/Framework-Gradio%206.x-6366F1?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3b82f6?style=flat-square)
![Design](https://img.shields.io/badge/Design-Glassmorphism-8b5cf6?style=flat-square)

---

## Features

**Header**
- Title, subtitle, and a dynamic live status badge (`● Connected` / `● Disconnected`) with pulse animation.

**Left Panel — Slack Configuration**
- Bot Token and App Token fields (password-masked).
- Workspace Name and Channel inputs.
- Connect / Disconnect buttons with full log feedback.
- Interactive status card showing active Socket Listener state and bot identity.

**Center Panel — Slack Chat Interface**
- Full chat bubble UI with custom user and bot avatars.
- Supports Markdown, code blocks with syntax highlighting, and image attachments.
- Pre-loaded with realistic Slack bot interactions.
- Image upload via collapsible accordion drawer.
- Send via button click or Enter key.
- Clear Chat button.

**Right Panel — Live Event Logs**
- Real-time scrollable terminal with timestamps and color-coded category badges:
  `[CONNECT]` `[API]` `[SUCCESS]` `[EVENT]` `[ERROR]`
- Auto-scrolls to latest entry on every update.
- Clear Logs button.

**Bottom Stats Cards**
- 💬 Messages Processed — increments live as messages are sent
- 👥 Connected Users
- ⚡ API Latency
- 📁 Uploads — increments live as images are uploaded

---

## Design System

| Token | Value |
|---|---|
| Background | `#0B1020` |
| Card surface | `#141B2D` with `backdrop-filter: blur(16px)` |
| Primary accent | `#4F8BFF` |
| Secondary accent | `#6C5CE7` |
| Success | `#2ECC71` |
| Error | `#FF5E57` |
| Border radius | `20px` |
| Typography | Inter / system-ui |
| Monospace | JetBrains Mono / Fira Code |

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure secrets (optional)

```bash
cp .env.example .env
# Edit .env and fill in your real Slack tokens
```

> If `.env` is absent the app starts normally with empty token fields — suitable for demo / development.

### 3. Generate assets

```bash
python create_assets.py
```

Assets are also auto-generated on first launch if missing.

### 4. Run

```bash
python app.py
```

Open **http://localhost:7860** in your browser.

---

## Project Structure

```
Gardio/
│
├── app.py              # Entry point — Gradio Blocks layout & event bindings
├── callbacks.py        # All event handler functions (pure Python, testable)
├── config.py           # Constants & environment-variable-driven configuration
├── theme.py            # Gradio theme, CSS, and JS
├── utils.py            # Shared helpers: log builder, image saver, stat HTML
├── create_assets.py    # One-time asset generator (avatars, cat image, SVG)
│
├── assets/             # Sample and uploaded images
├── icons/              # Bot avatar, user avatar, Slack SVG
│
├── requirements.txt    # Pinned Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Excludes .env and runtime uploads
└── README.md
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SLACK_BOT_TOKEN` | _(empty)_ | Your Slack bot token (`xoxb-...`) |
| `SLACK_APP_TOKEN` | _(empty)_ | Your Slack app token (`xapp-...`) |
| `SLACK_WORKSPACE` | `ai-workplace` | Display name of your workspace |
| `SLACK_CHANNEL` | `#ai-test` | Default channel to monitor |
| `APP_HOST` | `0.0.0.0` | Server bind address |
| `APP_PORT` | `7860` | Server port |
| `APP_SHARE` | `false` | Set `true` to generate a public Gradio share link |

---

## Known Limitations

- The Slack connection is **simulated** — no real WebSocket or Slack API calls are made. This is an interactive UI demo. To add real Slack integration, use the `slack_bolt` and `slack_sdk` packages and wire them into `callbacks.py`.
- File content in the chat (uploaded images) is displayed using the Gradio `{"path": "..."}` format. In a production deployment behind a reverse proxy, ensure the `assets/` directory is served or file paths are absolute.
- The "Connected Users" and "API Latency" stat cards are static demo values.
