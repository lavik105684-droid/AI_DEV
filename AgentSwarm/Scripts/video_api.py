import os
import subprocess
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Video Assembly API")

class RenderRequest(BaseModel):
    json_path: str

def run_assembly(json_path: str):
    # Ensure it's pointing to the correct host path if the container sends a container path
    # e.g., container sends /scripts/file.json -> we need C:\AI_DEV\AgentSwarm\Scripts\file.json
    if json_path.startswith('/scripts/'):
        host_path = os.path.join(r"C:\AI_DEV\AgentSwarm\Scripts", os.path.basename(json_path))
    else:
        host_path = json_path
        
    script_path = r"C:\AI_DEV\AgentSwarm\Scripts\assemble_video.py"
    
    # Run the assembly script
    subprocess.Popen(['python', script_path, host_path])

@app.post("/render")
async def trigger_render(req: RenderRequest, background_tasks: BackgroundTasks):
    if not req.json_path:
        raise HTTPException(status_code=400, detail="json_path is required")
        
    # Run in background so n8n doesn't timeout
    background_tasks.add_task(run_assembly, req.json_path)
    return {"status": "Render initiated", "path": req.json_path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
