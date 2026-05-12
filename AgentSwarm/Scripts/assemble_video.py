import os
import sys
import json
import time
import requests
import subprocess
from moviepy import TextClip, ColorClip, concatenate_videoclips, CompositeVideoClip

def get_vram_usage():
    try:
        # Tries to get AMD VRAM usage using rocm-smi if available
        # On Windows, this might require specific AMD tools. We'll simulate or use a fallback.
        result = subprocess.run(['rocm-smi', '--showuse'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return "VRAM Tracking Not Available"
    except Exception:
        return "VRAM Tracking Not Available"

def assemble_video(json_path):
    start_time = time.time()
    
    # Send "Working" status
    try:
        requests.get("http://localhost:8501/?agent=Developer&status=Working&message=Assembling_Video")
    except Exception:
        pass
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        scenes = data.get('scenes', [])
        if not scenes:
            # Fallback if the JSON structure is different
            if isinstance(data, list):
                scenes = data
            elif isinstance(data, dict):
                scenes = list(data.values())
        
        clips = []
        base_name = os.path.splitext(os.path.basename(json_path))[0]
        audio_dir = os.path.join(r"C:\AI_DEV\AgentSwarm\Audio", base_name)
        
        # Ping Dashboard
        try:
            requests.get(f"http://localhost:8501/?agent=Video-maker&status=Audio:_Synced&message=Assembling_{base_name}")
        except: pass

        for i, scene in enumerate(scenes):
            text = scene.get('narration_text', scene.get('text', f"Scene {i+1}"))
            
            # Default duration 3s
            duration = 3.0
            audio = None
            
            # Look for audio
            audio_path = os.path.join(audio_dir, f"scene_{i+1}.wav")
            if os.path.exists(audio_path):
                from moviepy import AudioFileClip
                audio = AudioFileClip(audio_path)
                duration = audio.duration + 0.5 # Add a small buffer
            
            # Create a simple placeholder scene
            bg_clip = ColorClip(size=(1920, 1080), color=(int(255 * (i % 2)), 50, 100), duration=duration)
            
            # Subtitle (using narration text)
            txt_clip = TextClip(text=text, font_size=50, color='white', size=(1800, 400), method='caption')
            txt_clip = txt_clip.with_position('bottom').with_duration(duration)
            
            # Combine
            comp = CompositeVideoClip([bg_clip, txt_clip])
            if audio:
                comp = comp.with_audio(audio)
                
            clips.append(comp)
            
        if not clips:
            raise ValueError("No scenes found in JSON")
            
        final_clip = concatenate_videoclips(clips)
        
        output_dir = os.path.dirname(json_path)
        base_name = os.path.splitext(os.path.basename(json_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_output.mp4")
        
        # Optimize for Radeon RX 6900 XT using h264_amf or hevc_amf
        final_clip.write_videofile(output_path, fps=24, codec="h264_amf", preset="balanced", audio_codec="aac", threads=8)
        
        end_time = time.time()
        render_time = round(end_time - start_time, 2)
        vram_usage = get_vram_usage()
        
        # Ping Dashboard as Analyst
        try:
            requests.get(f"http://localhost:8501/?agent=Analyst&status=Idle&message=Render_Time:_{render_time}_sec_VRAM:_{vram_usage.replace(' ', '_')}")
        except Exception as e:
            print(f"Failed to update dashboard: {e}")
            
        print(f"SUCCESS: Video rendered to {output_path}")
        return output_path

    except Exception as e:
        # QA/Dev error handling
        end_time = time.time()
        try:
            requests.get(f"http://localhost:8501/?agent=QA&status=Error&message=Video_Assembly_Failed")
        except Exception:
            pass
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assemble_video.py <path_to_json>")
        sys.exit(1)
        
    assemble_video(sys.argv[1])
