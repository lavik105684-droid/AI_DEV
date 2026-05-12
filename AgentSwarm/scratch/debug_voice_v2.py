import os
import json
import wave
from piper import PiperVoice

json_path = r"C:\AI_DEV\AgentSwarm\Scripts\chapter1_test.json"
output_dir = r"C:\AI_DEV\AgentSwarm\Audio"

try:
    model_path = r"C:\AI_DEV\AgentSwarm\bin\piper\models\ru_RU-dmitri-medium.onnx"
    voice = PiperVoice.load(model_path)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    scenes = data.get('scenes', [])
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    session_audio_dir = os.path.join(output_dir, base_name)
    os.makedirs(session_audio_dir, exist_ok=True)
    
    for i, scene in enumerate(scenes):
        text = scene.get('narration_text', '')
        print(f"Generating for scene {i+1}: {text}")
        
        wav_path = os.path.join(session_audio_dir, f"scene_{i+1}.wav")
        with wave.open(wav_path, "wb") as wav_file:
            voice.synthesize(text, wav_file)
        print(f"Generated {wav_path}")
        
except Exception as e:
    import traceback
    traceback.print_exc()
