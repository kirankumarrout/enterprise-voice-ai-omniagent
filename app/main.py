import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .rag.engine import RAGEngine
from .agent.graph import build_graph
from .voice.asr import ASRService
from .voice.vad import VADService
from .voice.pipeline import VoicePipeline
from .api.routes import knowledge_router, voice_router

settings = get_settings()
rag = RAGEngine(settings.data_dir)
agent = build_graph(rag)
asr = ASRService(settings.whisper_model, settings.whisper_device, settings.whisper_compute_type)
vad = VADService(settings.vad_threshold)
pipeline = VoicePipeline(asr, vad, agent, settings)

app = FastAPI(title="Enterprise Voice AI & OmniAgent")

frontend_url = os.getenv("FRONTEND_URL", "*")
origins = [origin.strip() for origin in frontend_url.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knowledge_router(rag))
app.include_router(voice_router(pipeline))

@app.get("/health")
def health():
    return {
        "status": "ok",
        "rag_chunks": len(rag.chunks),
        "speech_models_loaded": {
            "asr": asr.is_loaded,
            "vad": vad.is_loaded,
        },
    }

static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")
