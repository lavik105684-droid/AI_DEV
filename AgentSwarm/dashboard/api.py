import os
import json
from fastapi import FastAPI, Query
from datetime import datetime
import uvicorn

app = FastAPI()
STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "agents": {
            "Manager": {"status": "Idle", "last_active": "N/A"},
            "QA": {"status": "Idle", "last_active": "N/A"},
            "Dev": {"status": "Idle", "last_active": "N/A"},
            "Design": {"status": "Idle", "last_active": "N/A"},
            "Video-maker": {"status": "Idle", "last_active": "N/A"},
            "SEO": {"status": "Idle", "last_active": "N/A"},
            "Analyst": {"status": "Idle", "last_active": "N/A"},
            "Archivarius": {"status": "Idle", "last_active": "N/A"}
        },
        "logs": []
    }

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

@app.get("/")
async def update_status(
    agent: str = Query(...),
    status: str = Query(...),
    message: str = Query(None)
):
    state = load_state()
    if agent in state["agents"]:
        state["agents"][agent]["status"] = status
        state["agents"][agent]["last_active"] = datetime.now().strftime("%H:%M:%S")
        msg = message if message else f"Status changed to {status}"
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {agent}: {msg}"
        state["logs"].insert(0, log_entry)
        save_state(state)
        return {"status": "success", "agent": agent, "new_status": status}
    return {"status": "error", "message": "Agent not found"}

@app.get("/increment_cloud")
async def increment_cloud():
    state = load_state()
    state["cloud_calls"] = state.get("cloud_calls", 0) + 1
    save_state(state)
    return {"status": "success", "total_cloud_calls": state["cloud_calls"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)
