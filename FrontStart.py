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
    margin-bottom: 0;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.panel-outer {
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.06);
    border-bottom: none;
    border-radius: 16px 16px 0 0;
    padding: 16px 18px 14px 18px;
    margin-bottom: 0;
}

.panel-inner {
    background: linear-gradient(145deg, rgba(255,255,255,0.02), rgba(255,255,255,0.005));
    border: 1px solid rgba(255,255,255,0.06);
    border-top: none;
    border-radius: 0 0 16px 16px;
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

.bubble-row-client { display: flex; justify-content: flex-end; margin-bottom: 10px; }
.bubble-row-agent  { display: flex; justify-content: flex-start; margin-bottom: 10px; }

.bubble {
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 76%;
    font-size: 13.5px;
    line-height: 1.5;
    animation: fadeUp 0.3s ease;
}

.bubble-client {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    border-radius: 14px 14px 2px 14px;
    color: #e0eaff;
}

.bubble-agent {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px 14px 14px 2px;
    color: #cbd5e1;
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

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 18px;
}
</style>
""", unsafe_allow_html=True)

if "chats" not in st.session_state:
    st.session_state.chats = [
        {
            "id": 1,
            "messages": [
                {"role": "client", "text": "Я оплатив підписку, але доступ не активовано."},
                {"role": "agent",  "text": "Спробуйте перезайти в акаунт."}
            ],
            "analysis": {"intent": "Проблема з оплатою", "satisfaction": "Незадоволений", "quality_score": 2},
            "reason": "Агент не надав конкретного рішення і не запропонував ескалацію."
        },
        {
            "id": 2,
            "messages": [
                {"role": "client", "text": "Не можу увійти до акаунту."},
                {"role": "agent",  "text": "Скористайтесь відновленням паролю."},
                {"role": "client", "text": "Дякую, все працює."}
            ],
            "analysis": {"intent": "Проблема доступу", "satisfaction": "Задоволений", "quality_score": 5},
            "reason": None
        },
        {
            "id": 3,
            "messages": [
                {"role": "client", "text": "Де мій рахунок-фактура за лютий?"},
                {"role": "agent",  "text": "Рахунки надсилаються до 5-го числа наступного місяця."},
                {"role": "client", "text": "Зрозуміло, дякую."}
            ],
            "analysis": {"intent": "Питання з документами", "satisfaction": "Задоволений", "quality_score": 4},
            "reason": None
        },
        {
            "id": 4,
            "messages": [
                {"role": "client", "text": "Ваш сервіс постійно зависає!"},
                {"role": "agent",  "text": "Вибачте за незручності. Очистіть кеш браузера."},
                {"role": "client", "text": "Не допомогло, все ще зависає."},
                {"role": "agent",  "text": "Передаємо до технічного відділу."}
            ],
            "analysis": {"intent": "Технічна проблема", "satisfaction": "Незадоволений", "quality_score": 3},
            "reason": "Перше рішення не спрацювало, клієнт очікує занадто довго."
        },
        {
            "id": 5,
            "messages": [
                {"role": "client", "text": "Хочу змінити тарифний план."},
                {"role": "agent",  "text": "Звичайно! Який план вас цікавить?"},
                {"role": "client", "text": "Pro-версія."},
                {"role": "agent",  "text": "Оформив перехід. Він буде активний з наступного місяця."},
                {"role": "client", "text": "Чудово, дякую!"}
            ],
            "analysis": {"intent": "Зміна тарифу", "satisfaction": "Задоволений", "quality_score": 5},
            "reason": None
        },
        {
            "id": 6,
            "messages": [
                {"role": "client", "text": "Не отримав підтвердження реєстрації на пошту."},
                {"role": "agent",  "text": "Перевірте папку Спам."}
            ],
            "analysis": {"intent": "Email проблема", "satisfaction": "Незадоволений", "quality_score": 2},
            "reason": "Агент не запропонував альтернативи (повторна відправка, зміна email)."
        },
    ]

if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = 1

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

st.markdown(f"""
<div class="metrics-row">
  <div class="metric-card" style="--accent:{accent_colors['total']}">
    <div class="metric-value">{total}</div>
    <div class="metric-label">Всього чатів</div>
    <div class="metric-sub">за поточний період</div>
  </div>
  <div class="metric-card" style="--accent:{accent_colors['csat']}">
    <div class="metric-value">{csat}%</div>
    <div class="metric-label">CSAT</div>
    <div class="metric-sub">{satisfied} задоволених</div>
  </div>
  <div class="metric-card" style="--accent:{accent_colors['score']}">
    <div class="metric-value">{avg_score}</div>
    <div class="metric-label">Середня оцінка</div>
    <div class="metric-sub">з 5.0 балів</div>
  </div>
  <div class="metric-card" style="--accent:{accent_colors['issues']}">
    <div class="metric-value">{issues}</div>
    <div class="metric-label">Проблемні чати</div>
    <div class="metric-sub">потребують уваги</div>
  </div>
</div>
""", unsafe_allow_html=True)

left, center, right = st.columns([1, 2, 1])

with left:
    st.markdown('''
    <div class="panel-outer">
        <div class="panel-title">📂 Список чатів</div>
    </div>
    ''', unsafe_allow_html=True)
    with st.container(height=510, border=False):
        for chat in st.session_state.chats:
            is_active    = chat["id"] == st.session_state.selected_chat_id
            sat          = chat["analysis"]["satisfaction"]
            score        = chat["analysis"]["quality_score"]
            preview_msg  = chat["messages"][0]["text"]
            badge_icon   = "✓" if sat == "Задоволений" else "✗"
            badge_color  = "#4ade80" if sat == "Задоволений" else "#f87171"
            stars        = "★" * score + "☆" * (5 - score)
            border_color = "rgba(59,130,246,0.5)" if is_active else "rgba(255,255,255,0.06)"
            bg_color     = "rgba(59,130,246,0.10)" if is_active else "rgba(255,255,255,0.02)"

            st.markdown(f"""
            <div style="background:{bg_color};border:1px solid {border_color};border-radius:10px;padding:11px 13px;margin-bottom:2px;pointer-events:none;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#94a3b8;">#{chat['id']:03d}</span>
                    <span style="font-size:11px;font-weight:600;color:{badge_color};">{badge_icon} {sat}</span>
                </div>
                <div style="font-size:12px;color:#475569;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:5px;">{preview_msg}</div>
                <div style="font-size:12px;color:#facc15;letter-spacing:1px;">{stars}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Відкрити #{chat['id']:03d}", key=f"btn_{chat['id']}", use_container_width=True):
                st.session_state.selected_chat_id = chat["id"]
                st.rerun()

selected_chat = next(c for c in st.session_state.chats if c["id"] == st.session_state.selected_chat_id)

with center:
    st.markdown(f'''
    <div class="panel-outer">
        <div class="panel-title">💬 Діалог — Чат #{selected_chat["id"]:03d}</div>
    </div>
    <div class="panel-inner content-fade">
    ''', unsafe_allow_html=True)

    if selected_chat["reason"]:
        st.markdown(f'<div class="reason-box">⚠ {selected_chat["reason"]}</div>', unsafe_allow_html=True)

    dialog_html = '<div class="dialog-wrapper">'
    for msg in selected_chat["messages"]:
        if msg["role"] == "client":
            dialog_html += f"""
            <div class="bubble-row-client">
                <div>
                    <div class="bubble-label" style="text-align:right;">Клієнт</div>
                    <div class="bubble bubble-client">{msg['text']}</div>
                </div>
            </div>"""
        else:
            dialog_html += f"""
            <div class="bubble-row-agent">
                <div>
                    <div class="bubble-label">Агент</div>
                    <div class="bubble bubble-agent">{msg['text']}</div>
                </div>
            </div>"""
    dialog_html += '</div>'
    st.markdown(dialog_html + '</div>', unsafe_allow_html=True)

with right:
    st.markdown(f'''
    <div class="panel-outer">
        <div class="panel-title">📊 AI Аналіз</div>
    </div>
    <div class="panel-inner content-fade">
    ''', unsafe_allow_html=True)

    analysis  = selected_chat["analysis"]
    score     = analysis["quality_score"]
    sat_color = "#4ade80" if analysis["satisfaction"] == "Задоволений" else "#f87171"

    stars_html = '<div class="stars">'
    for i in range(1, 6):
        stars_html += f'<span class="{"star-filled" if i <= score else "star-empty"}">★</span>'
    stars_html += '</div>'

    st.markdown(f'''
    <div class="score-big">{score}<span style="font-size:18px;color:#475569;">/5</span></div>
    {stars_html}
    <div style="color:{sat_color};font-weight:600;font-size:14px;margin:12px 0;">● {analysis["satisfaction"]}</div>
    <div style="font-size:11px;color:#475569;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.1em;">Тип звернення</div>
    <div class="intent-tag">{analysis["intent"]}</div>
    <div style="font-size:11px;color:#475569;margin:14px 0 8px;text-transform:uppercase;letter-spacing:0.1em;">JSON дані</div>
    </div>
    ''', unsafe_allow_html=True)
    st.json(analysis)