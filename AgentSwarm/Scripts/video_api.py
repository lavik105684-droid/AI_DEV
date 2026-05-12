import os
import json
import requests
import subprocess
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Video Assembly API")

class RenderRequest(BaseModel):
    json_path: str

class VoiceoverRequest(BaseModel):
    json_path: str
    output_dir: str = r"C:\AI_DEV\AgentSwarm\Audio"

# Global Piper model
try:
    from piper import PiperVoice
    MODEL_PATH = r"C:\AI_DEV\AgentSwarm\bin\piper\models\ru_RU-dmitri-medium.onnx"
    if os.path.exists(MODEL_PATH):
        VOICE = PiperVoice.load(MODEL_PATH)
    else:
        VOICE = None
except Exception as e:
    print(f"Failed to load Piper model: {e}")
    VOICE = None

def run_voiceover(json_path: str, output_dir: str):
    import wave
    # Load JSON
    try:
        if VOICE is None:
            raise Exception("Piper model not loaded")

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        scenes = data.get('scenes', [])
        if not scenes and isinstance(data, list):
            scenes = data
            
        base_name = os.path.splitext(os.path.basename(json_path))[0]
        session_audio_dir = os.path.join(output_dir, base_name)
        os.makedirs(session_audio_dir, exist_ok=True)
        
        # Ping Dashboard
        requests.get(f"http://localhost:8501/?agent=Design&status=Voiceover&message=Generating_for_{base_name}")
        
        for i, scene in enumerate(scenes):
            text = scene.get('narration_text', '')
            if not text:
                continue
                
            wav_path = os.path.join(session_audio_dir, f"scene_{i+1}.wav")
            with wave.open(wav_path, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(VOICE.config.sample_rate)
                for chunk in VOICE.synthesize(text):
                    wav_file.writeframes(chunk.audio_int16_bytes)
            
        requests.get(f"http://localhost:8501/?agent=Design&status=Idle&message=Voiceover_Generated")
        
    except Exception as e:
        with open("C:/AI_DEV/AgentSwarm/voiceover_error.log", "a") as log:
            log.write(f"Error for {json_path}: {str(e)}\n")
        requests.get(f"http://localhost:8501/?agent=QA&status=Error&message=Voiceover_Failed")

def run_assembly(json_path: str):
    # Ensure it's pointing to the correct host path if the container sends a container path
    # e.g., container sends /scripts/file.json -> we need C:\AI_DEV\AgentSwarm\Scripts\file.json
    if json_path.startswith('/scripts/') or json_path.startswith('/home/node/'):
        host_path = os.path.join(r"C:\AI_DEV\AgentSwarm\Scripts", os.path.basename(json_path))
    else:
        host_path = json_path
        
    script_path = r"C:\AI_DEV\AgentSwarm\Scripts\assemble_video.py"
    
    # Run the assembly script
    subprocess.Popen(['python', script_path, host_path])

@app.post("/voiceover")
async def trigger_voiceover(req: VoiceoverRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_voiceover, req.json_path, req.output_dir)
    return {"status": "Voiceover initiated", "path": req.json_path}

@app.post("/render")
async def trigger_render(req: RenderRequest, background_tasks: BackgroundTasks):
    if not req.json_path:
        raise HTTPException(status_code=400, detail="json_path is required")
        
    # Run in background so n8n doesn't timeout
    background_tasks.add_task(run_assembly, req.json_path)
    return {"status": "Render initiated", "path": req.json_path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
