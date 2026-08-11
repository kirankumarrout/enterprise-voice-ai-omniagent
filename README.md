# Enterprise Voice AI & OmniAgent Platform

Local-first Voice AI + RAG + LangGraph reference project.

## Stack
- Python + FastAPI
- LangGraph
- RAG with TF-IDF retrieval
- faster-whisper ASR
- Silero VAD
- Browser Speech Synthesis TTS fallback
- Configurable endpointing, silence detection, turn-taking and barge-in state
- Per-stage latency telemetry

## Run on Windows

1. Install Python 3.11+ and FFmpeg.
2. Open PowerShell in this folder.
3. Run:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

The first ASR request downloads the Whisper model. Use `WHISPER_MODEL=tiny` for a faster CPU demo or `base` for better accuracy.

## Voice flow

Browser microphone -> VAD -> Whisper ASR -> endpointing/turn state -> LangGraph -> RAG -> response -> browser TTS.

## Knowledge base

Upload TXT/MD/PDF files from the UI or:

```bash
curl -X POST http://127.0.0.1:8000/api/knowledge/upload -F "file=@data/sample_banking_policy.txt"
```

## Voice configuration

Edit `.env`:

```text
VAD_THRESHOLD=0.50
MIN_SPEECH_MS=250
ENDPOINT_SILENCE_MS=700
BARGE_IN_ENABLED=true
```

## Important

This is a local engineering/demo implementation, not a production banking system. Only claim the exact components you actually run and validate on your resume.
