"""
frontend/styles.py
------------------
All custom CSS and JavaScript for Slack Bot Studio.
No Python logic — only static string constants consumed by launch().
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS: str = """
/* ── Global Reset & Font ──────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container {
    background-color: #0B1020 !important;
    color: #F8FAFC !important;
}

.gradio-container {
    max-width: 1440px !important;
    margin: 0 auto !important;
    padding: 20px !important;
}

/* ── Header Card ─────────────────────────────────────────────── */
.header-card {
    background: rgba(20,27,45,0.8) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    padding: 20px 28px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

/* ── Status Badge ─────────────────────────────────────────────── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.status-connected {
    background: rgba(46,204,113,0.12);
    color: #2ECC71;
    border: 1px solid rgba(46,204,113,0.35);
    box-shadow: 0 0 14px rgba(46,204,113,0.18);
}

.status-disconnected {
    background: rgba(255,94,87,0.12);
    color: #FF5E57;
    border: 1px solid rgba(255,94,87,0.35);
    box-shadow: none;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.status-connected .status-dot {
    background: #2ECC71;
    box-shadow: 0 0 8px #2ECC71;
    animation: pulse-dot 2s ease-in-out infinite;
}

.status-disconnected .status-dot {
    background: #FF5E57;
}

@keyframes pulse-dot {
    0%, 100% { transform: scale(0.9); opacity: 0.9; }
    50%       { transform: scale(1.2); opacity: 1; }
}

/* ── Panel Cards ─────────────────────────────────────────────── */
.panel-card {
    background: rgba(20,27,45,0.75) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25) !important;
    transition: border-color 0.3s ease !important;
}

.panel-header {
    font-size: 17px !important;
    font-weight: 600 !important;
    color: #F8FAFC !important;
    margin-bottom: 14px !important;
    padding-bottom: 12px !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}

/* ── Form Controls ───────────────────────────────────────────── */
input[type="text"],
input[type="password"],
textarea {
    background: #0F172A !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    color: #F8FAFC !important;
    font-size: 13px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

input[type="text"]:focus,
input[type="password"]:focus,
textarea:focus {
    border-color: #4F8BFF !important;
    box-shadow: 0 0 0 3px rgba(79,139,255,0.18) !important;
    outline: none !important;
}

/* ── Buttons ─────────────────────────────────────────────────── */
.btn-primary button {
    background: linear-gradient(135deg,#4F8BFF 0%,#6C5CE7 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 18px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(79,139,255,0.28) !important;
    cursor: pointer !important;
}

.btn-primary button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(79,139,255,0.4) !important;
}

.btn-primary button:active { transform: translateY(0) !important; }

.btn-danger button {
    background: rgba(255,94,87,0.12) !important;
    color: #FF5E57 !important;
    border: 1px solid rgba(255,94,87,0.35) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 18px !important;
    transition: background 0.2s ease, border-color 0.2s ease !important;
    cursor: pointer !important;
}

.btn-danger button:hover {
    background: rgba(255,94,87,0.25) !important;
    border-color: #FF5E57 !important;
}

.btn-secondary button {
    background: rgba(255,255,255,0.05) !important;
    color: #94A3B8 !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: background 0.2s ease, color 0.2s ease !important;
}

.btn-secondary button:hover {
    background: rgba(255,255,255,0.10) !important;
    color: #F8FAFC !important;
}

/* ── Chatbot ─────────────────────────────────────────────────── */
#chatbot-panel {
    background: #0F172A !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
}

#chatbot-panel .user > div,
#chatbot-panel [data-testid="user"] > div {
    background: #1E293B !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 16px 16px 4px 16px !important;
    color: #F8FAFC !important;
}

#chatbot-panel .bot > div,
#chatbot-panel [data-testid="bot"] > div {
    background: #141B2D !important;
    border-left: 3px solid #4F8BFF !important;
    border-radius: 4px 16px 16px 16px !important;
    color: #E2E8F0 !important;
}

/* ── Log Terminal ────────────────────────────────────────────── */
#log-terminal-wrap {
    background: #070A14 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 12px 14px !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 11.5px !important;
    min-height: 420px !important;
    max-height: 480px !important;
    overflow-y: auto !important;
    line-height: 1.65 !important;
    scroll-behavior: smooth !important;
}

.log-entry {
    margin-bottom: 7px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    word-break: break-word;
    animation: fade-in-up 0.25s ease both;
}

@keyframes fade-in-up {
    from { opacity: 0; transform: translateY(4px); }
    to   { opacity: 1; transform: translateY(0); }
}

.log-time { color: #475569; font-size: 10px; }

.log-badge {
    display: inline-block;
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 9.5px;
    font-weight: 700;
    margin: 0 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    vertical-align: middle;
}

.badge-info    { background: rgba(79,139,255,0.18);  color: #4F8BFF; }
.badge-api     { background: rgba(108,92,231,0.18);  color: #A29BFE; }
.badge-success { background: rgba(46,204,113,0.18);  color: #2ECC71; }
.badge-event   { background: rgba(255,183,3,0.18);   color: #FFB703; }
.badge-error   { background: rgba(255,94,87,0.18);   color: #FF5E57; }

/* ── Stat Cards ──────────────────────────────────────────────── */
.stat-card {
    background: rgba(20,27,45,0.75) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    transition: transform 0.3s cubic-bezier(0.4,0,0.2,1),
                border-color 0.3s ease,
                box-shadow 0.3s ease !important;
    cursor: default;
}

.stat-card:hover {
    transform: translateY(-5px) !important;
    border-color: rgba(79,139,255,0.3) !important;
    box-shadow: 0 14px 28px -8px rgba(79,139,255,0.25) !important;
}

.stat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #94A3B8;
    font-size: 12.5px;
    font-weight: 500;
    margin-bottom: 10px;
}

.stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    flex-shrink: 0;
}

.stat-val {
    font-size: 30px !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    letter-spacing: -0.5px;
    line-height: 1;
}

.stat-desc {
    font-size: 11.5px;
    color: #2ECC71;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.stat-desc.warn  { color: #FFB703; }
.stat-desc.error { color: #FF5E57; }
.stat-desc.muted { color: #64748B; }

/* ── Accordion / Upload ──────────────────────────────────────── */
.gr-accordion {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    margin-top: 10px !important;
}

/* ── Scrollbar ───────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track  { background: rgba(15,23,42,0.4); }
::-webkit-scrollbar-thumb  { background: rgba(255,255,255,0.12); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(79,139,255,0.45); }

/* ── Misc Gradio overrides ───────────────────────────────────── */
.gr-box, .gr-form, .gr-panel { background: transparent !important; border: none !important; }
label > span { color: #94A3B8 !important; font-weight: 500 !important; font-size: 12.5px !important; }
.gr-button { font-family: 'Inter', system-ui, sans-serif !important; }
footer { display: none !important; }
"""

# ---------------------------------------------------------------------------
# JavaScript — injected via js= in launch()
# ---------------------------------------------------------------------------
LOG_AUTOSCROLL_JS: str = """
(function() {
    function scrollLogs() {
        var el = document.getElementById('log-terminal-wrap');
        if (el) { el.scrollTop = el.scrollHeight; }
    }
    var obs = new MutationObserver(scrollLogs);
    function attach() {
        var el = document.getElementById('log-terminal-wrap');
        if (el) {
            obs.observe(el, { childList: true, subtree: true, characterData: true });
            scrollLogs();
        } else {
            setTimeout(attach, 600);
        }
    }
    attach();
})();
"""
