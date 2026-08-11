from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
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
app.include_router(knowledge_router(rag))
app.include_router(voice_router(pipeline))

@app.get("/health")
def health():
    return {"status":"ok", "rag_chunks":len(rag.chunks)}

@app.get("/")
def home():
    return FileResponse(Path("static/index.html"))
