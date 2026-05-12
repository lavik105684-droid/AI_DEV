import streamlit as st
import json
import os
import time

STATE_FILE = "state.json"

st.set_page_config(page_title="Agent Status Monitor", page_icon="🤖", layout="wide")

st.title("🤖 Agent Swarm Status Monitor")
st.markdown("Мониторинг состояния агентов (Обновляется автоматически)")

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "agents": {},
        "logs": ["Ожидание данных от API..."]
    }

state = load_state()

col_m1, col_m2, col_m3, col_m4 = st.columns([1, 1, 1, 1])

report = state.get("system_report", {"efficiency": "0%", "saved_calls": 0})

with col_m1:
    st.metric("Total Agents", "8")
with col_m2:
    st.metric("Cloud Calls", state.get("cloud_calls", 0))
with col_m3:
    st.metric("Efficiency", report["efficiency"])
with col_m4:
    st.metric("Saved Cloud Calls", report["saved_calls"])

st.divider()

col_main1, col_main2 = st.columns([1, 2])

with col_main1:
    st.header("Статус Агентов")
    
    def get_status_color(status):
        status_lower = status.lower()
        if "error" in status_lower or "fail" in status_lower: return "red"
        if "completed" in status_lower or "done" in status_lower: return "green"
        if "idle" in status_lower: return "grey"
        return "blue"

    for agent, info in state.get("agents", {}).items():
        status = info["status"]
        color = get_status_color(status)
        st.markdown(f"**{agent}**: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
        st.progress(100 if color == "green" else (50 if color == "blue" else (100 if color == "red" else 0)))

with col_main2:
    st.header("Логи действий")
    log_text = "\n".join(state.get("logs", []))
    st.text_area("Activity Log", value=log_text, height=500, disabled=True)

# Auto-refresh
time.sleep(3)
st.rerun()
