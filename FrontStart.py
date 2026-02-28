import json
import os
import streamlit as st

st.set_page_config(layout="wide", page_title="AI Support Analytics", page_icon="🤖")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #080c14 !important;
    color: #e2e8f0;
    font-family: 'Space Grotesk', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 100% !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
    opacity: 0.8;
}

.metric-card:hover { border-color: rgba(255,255,255,0.15); }

.metric-label {
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 0.01em;
    color: #94a3b8;
    margin-top: 6px;
    margin-bottom: 2px;
}

.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 32px;
    font-weight: 500;
    color: #f1f5f9;
    line-height: 1;
}

.metric-sub {
    font-size: 12px;
    color: #475569;
    margin-top: 6px;
}

.panel-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.full-panel {
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 16px 18px;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    background: linear-gradient(145deg, rgba(255,255,255,0.02), rgba(255,255,255,0.005)) !important;
    overflow: hidden !important;
}
[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: transparent !important;
    padding: 12px 14px !important;
}

.dialog-wrapper {
    height: 460px;
    overflow-y: auto;
    padding: 10px 4px;
    scrollbar-width: thin;
    scrollbar-color: #1e293b transparent;
}

.dialog-wrapper::-webkit-scrollbar { width: 4px; }
.dialog-wrapper::-webkit-scrollbar-track { background: transparent; }
.dialog-wrapper::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }

.bubble-row-client {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
    width: 100%;
}
.bubble-row-agent {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 10px;
    width: 100%;
}

.bubble {
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 76%;
    min-width: 0;
    font-size: 13.5px;
    line-height: 1.5;
    animation: fadeUp 0.3s ease;
    word-break: break-word;
    box-sizing: border-box;
}

.bubble-client {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    border-radius: 14px 14px 2px 14px;
    color: #e0eaff;
    margin-left: auto;
}

.bubble-agent {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px 14px 14px 2px;
    color: #cbd5e1;
    margin-right: auto;
}

.bubble-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
    color: #64748b;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.content-fade {
    animation: fadeIn 0.35s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.reason-box {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.2);
    border-left: 3px solid #ef4444;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    color: #fca5a5;
    margin-bottom: 14px;
}

.stars { font-size: 22px; letter-spacing: 2px; }
.star-filled { color: #facc15; }
.star-empty { color: #1e293b; }

.score-big {
    font-family: 'JetBrains Mono', monospace;
    font-size: 48px;
    font-weight: 500;
    line-height: 1;
    background: linear-gradient(135deg, #facc15, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.intent-tag {
    display: inline-block;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.25);
    color: #93c5fd;
    font-size: 12px;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
}

.panel {
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 18px;
    height: 100%;
}

[data-testid="stHorizontalBlock"] { gap: 14px !important; }
[data-testid="column"] > div { height: 100%; }

.stMarkdown p { margin: 0; }
h1 { font-family: 'Space Grotesk', sans-serif !important; font-size: 20px !important; font-weight: 600 !important; margin-bottom: 20px !important; color: #f1f5f9 !important; }

div[data-testid="stJson"] {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    font-size: 12px !important;
}

.json-block {
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.json-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 8px;
    border-radius: 6px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.04);
}

.json-key {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #64748b;
    letter-spacing: 0.03em;
}

.json-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #93c5fd;
    font-weight: 500;
}

[data-testid="stButton"] button {
    background: rgba(59,130,246,0.08) !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-radius: 6px !important;
    color: #3b82f6 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    height: 28px !important;
    padding: 0 !important;
    margin: -6px 0 10px 0 !important;
    cursor: pointer !important;
    width: 100% !important;
    transition: background 0.2s, border-color 0.2s !important;
}
[data-testid="stButton"] button:hover {
    background: rgba(59,130,246,0.18) !important;
    border-color: rgba(59,130,246,0.4) !important;
    box-shadow: none !important;
}

.errors-table {
    border: 1px solid rgba(239,68,68,0.15);
    border-radius: 10px;
    overflow: hidden;
}

.errors-header {
    display: flex;
    justify-content: space-between;
    padding: 7px 12px;
    background: rgba(239,68,68,0.08);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #f87171;
    border-bottom: 1px solid rgba(239,68,68,0.15);
}

.errors-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 8px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    gap: 10px;
}

.errors-row:last-child { border-bottom: none; }

.err-type {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #fca5a5;
    white-space: nowrap;
    min-width: 0;
    flex-shrink: 0;
}

.err-desc {
    font-size: 11px;
    color: #64748b;
    text-align: right;
}

.errors-empty {
    padding: 10px 12px;
    font-size: 12px;
    color: #4ade80;
    font-weight: 500;
    background: rgba(34,197,94,0.06);
    border: 1px solid rgba(34,197,94,0.15);
    border-radius: 10px;
}

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# ДАНІ
# Діалоги:   data/chats.json
# Аналітика: data/analysis.json
# Щоб додати чат — додайте запис в обидва файли з однаковим chat_id
# ---------------------------------------------------------------

MISTAKE_LABELS = {
    "no_resolution":    "Відсутність рішення",
    "ignored_question": "Ігнорування питання",
    "rude_tone":        "Грубий тон",
}

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

if "chats" not in st.session_state:
    with open(os.path.join(DATA_DIR, "chats.json"), encoding="utf-8") as f:
        chats_raw = json.load(f)

    with open(os.path.join(DATA_DIR, "analysis.json"), encoding="utf-8") as f:
        analysis_raw = json.load(f)

    analysis_map = {a["chat_id"]: a for a in analysis_raw}

    chats = []
    for i, c in enumerate(chats_raw):
        cid = c["chat_id"]
        an  = analysis_map.get(cid, {})
        sat = "Задоволений" if an.get("satisfaction") == "satisfied" else "Незадоволений"

        mistakes = an.get("agent_mistakes", [])
        errors   = [{"type": MISTAKE_LABELS.get(m, m), "description": ""} for m in mistakes]

        chats.append({
            "id":       i + 1,
            "chat_id":  cid,
            "messages": [
                {"role": "client" if m["role"] == "customer" else "agent", "text": m["text"]}
                for m in c["messages"]
            ],
            "analysis": {
                "intent":        an.get("intent", ""),
                "satisfaction":  sat,
                "quality_score": an.get("quality_score", 0),
                "reasoning":     an.get("satisfaction_reasoning", ""),
            },
            "reason": an.get("satisfaction_reasoning") if sat == "Незадоволений" else None,
            "errors": errors,
        })

    st.session_state.chats = chats

if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = 1

# ---------------------------------------------------------------
# МЕТРИКИ
# ---------------------------------------------------------------
total      = len(st.session_state.chats)
satisfied  = sum(1 for c in st.session_state.chats if c["analysis"]["satisfaction"] == "Задоволений")
csat       = round(satisfied / total * 100) if total else 0
avg_score  = round(sum(c["analysis"]["quality_score"] for c in st.session_state.chats) / total, 1) if total else 0
issues     = total - satisfied

accent_colors = {
    "total":  "#3b82f6",
    "csat":   "#22c55e" if csat >= 60 else "#ef4444",
    "score":  "#facc15",
    "issues": "#ef4444",
}

st.markdown(
    '<div class="metrics-row">'
    '<div class="metric-card" style="--accent:' + accent_colors["total"] + '">'
    '<div class="metric-value">' + str(total) + '</div>'
    '<div class="metric-label">Всього чатів</div>'
    '<div class="metric-sub">за поточний період</div>'
    '</div>'
    '<div class="metric-card" style="--accent:' + accent_colors["csat"] + '">'
    '<div class="metric-value">' + str(csat) + '%</div>'
    '<div class="metric-label">CSAT</div>'
    '<div class="metric-sub">' + str(satisfied) + ' задоволених</div>'
    '</div>'
    '<div class="metric-card" style="--accent:' + accent_colors["score"] + '">'
    '<div class="metric-value">' + str(avg_score) + '</div>'
    '<div class="metric-label">Середня оцінка</div>'
    '<div class="metric-sub">з 5.0 балів</div>'
    '</div>'
    '<div class="metric-card" style="--accent:' + accent_colors["issues"] + '">'
    '<div class="metric-value">' + str(issues) + '</div>'
    '<div class="metric-label">Проблемні чати</div>'
    '<div class="metric-sub">потребують уваги</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

selected_chat = next(c for c in st.session_state.chats if c["id"] == st.session_state.selected_chat_id)

left, center, right = st.columns([1, 2, 1])

# ---------------------------------------------------------------
# ЛІВА ПАНЕЛЬ — список чатів
# ---------------------------------------------------------------
with left:
    st.markdown(
        '<div class="full-panel" style="margin-bottom:4px;border-radius:16px 16px 0 0;border-bottom:none;">'
        '<div class="panel-title" style="margin-bottom:0;">📂 Список чатів</div>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.container(height=510, border=False):
        for chat in st.session_state.chats:
            is_active    = chat["id"] == st.session_state.selected_chat_id
            sat          = chat["analysis"]["satisfaction"]
            score        = chat["analysis"]["quality_score"]
            preview_msg  = chat["messages"][0]["text"]
            chat_id      = chat["id"]
            chat_id_label = chat["chat_id"]
            badge_icon   = "✓" if sat == "Задоволений" else "✗"
            badge_color  = "#4ade80" if sat == "Задоволений" else "#f87171"
            stars        = "★" * score + "☆" * (5 - score)
            border_color = "rgba(59,130,246,0.5)" if is_active else "rgba(255,255,255,0.06)"
            bg_color     = "rgba(59,130,246,0.10)" if is_active else "rgba(255,255,255,0.02)"

            st.markdown(
                '<div style="background:' + bg_color + ';border:1px solid ' + border_color + ';border-radius:10px;padding:11px 13px;margin-bottom:2px;pointer-events:none;">'
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">'
                '<span style="font-family:\'JetBrains Mono\',monospace;font-size:12px;color:#94a3b8;">' + chat_id_label + '</span>'
                '<span style="font-size:11px;font-weight:600;color:' + badge_color + ';">' + badge_icon + ' ' + sat + '</span>'
                '</div>'
                '<div style="font-size:12px;color:#475569;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:5px;">' + preview_msg + '</div>'
                '<div style="font-size:12px;color:#facc15;letter-spacing:1px;">' + stars + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button("Відкрити " + chat_id_label, key="btn_" + chat_id_label, use_container_width=True):
                st.session_state.selected_chat_id = chat_id
                st.rerun()

# ---------------------------------------------------------------
# ЦЕНТРАЛЬНА ПАНЕЛЬ — діалог
# ---------------------------------------------------------------
with center:
    reason_html = ('<div class="reason-box">⚠ ' + selected_chat["reason"] + '</div>') if selected_chat["reason"] else ""

    dialog_html = ""
    for msg in selected_chat["messages"]:
        if msg["role"] == "client":
            dialog_html += (
                '<div class="bubble-row-client">'
                '<div style="display:flex;flex-direction:column;align-items:flex-end;max-width:76%;">'
                '<div class="bubble-label">Клієнт</div>'
                '<div class="bubble bubble-client">' + msg["text"] + '</div>'
                '</div></div>'
            )
        else:
            dialog_html += (
                '<div class="bubble-row-agent">'
                '<div style="display:flex;flex-direction:column;align-items:flex-start;max-width:76%;">'
                '<div class="bubble-label">Агент</div>'
                '<div class="bubble bubble-agent">' + msg["text"] + '</div>'
                '</div></div>'
            )

    st.markdown(
        '<div class="full-panel content-fade">'
        '<div class="panel-title">💬 Діалог — ' + selected_chat["chat_id"] + '</div>'
        + reason_html
        + '<div class="dialog-wrapper">' + dialog_html + '</div>'
        '</div>',
        unsafe_allow_html=True
    )

# ---------------------------------------------------------------
# ПРАВА ПАНЕЛЬ — аналітика
# ---------------------------------------------------------------
with right:
    analysis     = selected_chat["analysis"]
    score        = analysis["quality_score"]
    sat_color    = "#4ade80" if analysis["satisfaction"] == "Задоволений" else "#f87171"
    satisfaction = analysis["satisfaction"]
    intent       = analysis["intent"]

    stars_html = ""
    for i in range(1, 6):
        cls = "star-filled" if i <= score else "star-empty"
        stars_html += '<span class="' + cls + '">★</span>'

    json_rows = ""
    for key, val in analysis.items():
        json_rows += (
            '<div class="json-row">'
            '<span class="json-key">' + key + '</span>'
            '<span class="json-val">' + str(val) + '</span>'
            '</div>'
        )

    errors = selected_chat.get("errors", [])
    if errors:
        errors_html = (
            '<div class="errors-table">'
            '<div class="errors-header">'
            '<span>Тип помилки</span><span>Опис</span>'
            '</div>'
        )
        for err in errors:
            errors_html += (
                '<div class="errors-row">'
                '<span class="err-type">' + err["type"] + '</span>'
                '<span class="err-desc">' + err.get("description", "") + '</span>'
                '</div>'
            )
        errors_html += '</div>'
    else:
        errors_html = '<div class="errors-empty">✓ Немає мінету</div>'

    st.markdown(
        '<div class="full-panel content-fade">'
        '<div class="panel-title">📊 AI Аналіз</div>'
        '<div class="score-big">' + str(score) + '<span style="font-size:18px;color:#475569;">/5</span></div>'
        '<div class="stars" style="margin-top:8px;">' + stars_html + '</div>'
        '<div style="color:' + sat_color + ';font-weight:600;font-size:14px;margin:12px 0;">● ' + satisfaction + '</div>'
        '<div style="font-size:11px;color:#475569;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.1em;">Тип звернення</div>'
        '<div class="intent-tag">' + intent + '</div>'
        '<div style="font-size:11px;color:#475569;margin:14px 0 8px;text-transform:uppercase;letter-spacing:0.1em;">JSON дані</div>'
        '<div class="json-block">' + json_rows + '</div>'
        '<div style="font-size:11px;color:#475569;margin:14px 0 8px;text-transform:uppercase;letter-spacing:0.1em;">Помилки агента</div>'
        + errors_html +
        '</div>',
        unsafe_allow_html=True
    )