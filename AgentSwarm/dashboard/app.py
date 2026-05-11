import streamlit as st
import pandas as pd
from datetime import datetime

# Настройка страницы
st.set_page_config(page_title="Agent Status Monitor", page_icon="🤖", layout="wide")

st.title("🤖 Agent Swarm Status Monitor")
st.markdown("Мониторинг состояния агентов и логирование их действий в реальном времени.")

# Инициализация состояния сессии для хранения данных
if 'agents' not in st.session_state:
    st.session_state.agents = {
        "Manager": {"status": "Idle", "last_active": datetime.now().strftime("%H:%M:%S")},
        "QA": {"status": "Idle", "last_active": datetime.now().strftime("%H:%M:%S")},
        "Dev": {"status": "Idle", "last_active": datetime.now().strftime("%H:%M:%S")},
        "Design": {"status": "Idle", "last_active": datetime.now().strftime("%H:%M:%S")},
        "Video-maker": {"status": "Idle", "last_active": datetime.now().strftime("%H:%M:%S")},
        "SEO": {"status": "Idle", "last_active": datetime.now().strftime("%H:%M:%S")},
        "Analyst": {"status": "Idle", "last_active": datetime.now().strftime("%H:%M:%S")},
    }

if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- API Endpoints ---
# Streamlit не очень хорошо подходит для полноценного REST API внутри одного процесса,
# но мы можем симулировать обновление данных через query_params для простоты интеграции
# В реальном Production лучше использовать FastAPI + Streamlit отдельно.
query_params = st.query_params
if "agent" in query_params and "status" in query_params:
    agent = query_params.get("agent")
    status = query_params.get("status")
    message = query_params.get("message", f"Status changed to {status}")
    
    if agent in st.session_state.agents:
        st.session_state.agents[agent]["status"] = status
        st.session_state.agents[agent]["last_active"] = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {agent}: {message}"
        st.session_state.logs.insert(0, log_entry) # Новые логи сверху
        
        # Очищаем query_params, чтобы не добавлять лог при каждой перезагрузке страницы
        st.query_params.clear()


# --- UI Layout ---
col1, col2 = st.columns([1, 2])

# Колонка 1: Статусы Агентов
with col1:
    st.header("Статус Агентов")
    
    def get_status_color(status):
        colors = {
            "Idle": "grey",
            "Thinking...": "blue",
            "Completed": "green",
            "Error": "red"
        }
        return colors.get(status, "grey")

    for agent, info in st.session_state.agents.items():
        status = info["status"]
        color = get_status_color(status)
        st.markdown(f"**{agent}**: <span style='color:{color}'>{status}</span> (Last active: {info['last_active']})", unsafe_allow_html=True)
        st.progress(100 if status == "Completed" else (50 if status == "Thinking..." else 0))

# Колонка 2: Логи
with col2:
    st.header("Логи действий")
    log_text = "\n".join(st.session_state.logs) if st.session_state.logs else "Нет логов."
    st.text_area("Agent Activity Log", value=log_text, height=400, disabled=True)

# Инструкция по использованию API
st.markdown("---")
st.subheader("API для обновления статуса")
st.code('''
# Пример вызова для обновления статуса (отправьте GET запрос)
# http://localhost:8501/?agent=Dev&status=Thinking...&message=Пишу%20SQL-скрипт
''', language="python")

# Кнопка для автообновления
import time
if st.button("Auto-Refresh (Обновить сейчас)"):
    st.rerun()

# --- Симуляция (только для демо) ---
st.sidebar.header("Demo Controls")
demo_agent = st.sidebar.selectbox("Agent", list(st.session_state.agents.keys()))
demo_status = st.sidebar.selectbox("Status", ["Idle", "Thinking...", "Completed", "Error"])
demo_message = st.sidebar.text_input("Message", "Тестовое сообщение")

if st.sidebar.button("Update Status"):
    st.session_state.agents[demo_agent]["status"] = demo_status
    st.session_state.agents[demo_agent]["last_active"] = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {demo_agent}: {demo_message}"
    st.session_state.logs.insert(0, log_entry)
    st.rerun()
