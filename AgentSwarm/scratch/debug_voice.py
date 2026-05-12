import os
import json
import subprocess
import requests

json_path = r"C:\AI_DEV\AgentSwarm\Scripts\chapter1_test.json"
output_dir = r"C:\AI_DEV\AgentSwarm\Audio"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    scenes = data.get('scenes', [])
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    session_audio_dir = os.path.join(output_dir, base_name)
    os.makedirs(session_audio_dir, exist_ok=True)
    
    model_path = r"C:\AI_DEV\AgentSwarm\bin\piper\models\ru_RU-dmitri-medium.onnx"
    
    for i, scene in enumerate(scenes):
        text = scene.get('narration_text', '')
        print(f"Generating for scene {i+1}: {text}")
        
        wav_path = os.path.join(session_audio_dir, f"scene_{i+1}.wav")
        temp_txt = os.path.join(session_audio_dir, "temp.txt")
        with open(temp_txt, "w", encoding="utf-8") as tf:
            tf.write(text)
        
        cmd = f'Get-Content "{temp_txt}" | python -m piper --model "{model_path}" --output_file "{wav_path}"'
        print(f"Running command: {cmd}")
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        print(f"Stdout: {res.stdout}")
        print(f"Stderr: {res.stderr}")
        
except Exception as e:
    print(f"ERROR: {e}")
