<instruction>You are an expert software engineer. You are working on a WIP branch. Please run `git status` and `git diff` to understand the changes and the current state of the code. Analyze the workspace context and complete the mission brief.</instruction>
<workspace_context>
<artifacts>
--- CURRENT TASK CHECKLIST ---
# Task List: Full Pipeline Activation

## Sprint 01: Core Pipeline [DONE]
- [x] Fix Dashboard (`app.py`) to use `state.json` and auto-refresh.
- [x] Create Master Workflow `04_Memoirs_Full_Production` in n8n.
- [x] Integrate Local Creative Brain (Qwen 14B).
- [x] Implement Historical Context QA (Archivarius).
- [x] Test the pipeline on Chapter 1.
- [x] Verify `.mp4` output.

## Sprint 02: Self-Healing Loop [IN PROGRESS]
- [x] Add Dashboard status update for rejections.
- [x] Create feedback loop connection in n8n.
- [x] Implement retry counter (max 3).
- [x] Dynamic style wildcard for retries.
- [/] Verify recovery from context rejection.

--- IMPLEMENTATION PLAN ---
# Sprint 03: Voice Activation & Audio-Visual Sync

We are moving from silent movies to full voiceover production. This sprint integrates local TTS (Piper) into the autonomous pipeline.

## Proposed Changes

### Video API & Automation Layer

#### [MODIFY] [video_api.py](file:///C:/AI_DEV/AgentSwarm/Scripts/video_api.py)
- **Voiceover Endpoint**: Added `/voiceover` which uses the Piper Python API to generate `.wav` files for each scene in a storyboard.
- **Pre-loading**: Piper model is pre-loaded at startup to reduce latency.
- **Robustness**: Added logging to `voiceover_error.log` and dashboard status updates for the "Design" agent.

#### [MODIFY] [assemble_video.py](file:///C:/AI_DEV/AgentSwarm/Scripts/assemble_video.py)
- **Audio Integration**: The assembly script now automatically looks for audio files in `C:\AI_DEV\AgentSwarm\Audio\[SessionName]\scene_[N].wav`.
- **Dynamic Timing**: Scene duration is now dynamically adjusted to match the length of the voiceover track.
- **Dashboard Sync**: Added `Audio: Synced` status during assembly.

### Orchestration (n8n)

#### [NEW] [n8n_voiceover_generator.json](file:///C:/AI_DEV/AgentSwarm/n8n_voiceover_generator.json)
- New workflow `06_Voiceover_Generator` that:
    1. Triggers on new approved scripts.
    2. Calls `/voiceover` to generate audio.
    3. Triggers `/render` to produce the final `.mp4`.

## Verification Plan

### Automated Tests
- [x] **Piper API Test**: Verified `PiperVoice` can synthesize Russian text into valid `.wav` files.
- [x] **Video API Test**: Verified `/voiceover` endpoint successfully creates the audio directory and files.
- [x] **Render Test**: Verified `assemble_video.py` creates an `.mp4` with a size reflecting the addition of audio.

### Manual Verification
1. **Audio Quality**: User should listen to `C:\AI_DEV\AgentSwarm\Audio\chapter1_test\scene_1.wav` to verify the 'ru_RU-dmitri-medium' voice quality.
2. **Sync Check**: Open `chapter1_test_output.mp4` to ensure the audio matches the subtitles and the scene transitions occur when the voiceover ends.
</artifacts>
</workspace_context>
<mission_brief>[Describe your task here...]</mission_brief>