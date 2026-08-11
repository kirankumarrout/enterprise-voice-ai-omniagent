import subprocess
import tempfile
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException


def knowledge_router(rag):
    r = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

    @r.post("/upload")
    async def upload(file: UploadFile = File(...)):
        if file.filename.lower().split(".")[-1] not in {"txt", "md", "pdf"}:
            raise HTTPException(400, "Only TXT, MD and PDF files are supported.")
        name = rag.add_file(file.filename, await file.read())
        return {"ok": True, "filename": name, "chunks": len(rag.chunks)}

    return r


def _to_wav(data: bytes, filename: str = "audio.webm") -> bytes:
    """Convert browser-recorded audio to mono 16-bit PCM WAV for VAD/ASR."""
    if data[:4] == b"RIFF":
        return data

    suffix = Path(filename).suffix.lower() or ".webm"
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / f"input{suffix}"
        dst = Path(tmp) / "output.wav"
        src.write_bytes(data)
        result = subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", str(src),
                "-ac", "1", "-ar", "16000", "-sample_fmt", "s16",
                str(dst),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not dst.exists():
            raise ValueError(f"Unable to decode uploaded audio: {result.stderr.strip()}")
        return dst.read_bytes()


def voice_router(pipeline):
    r = APIRouter(prefix="/api/voice", tags=["voice"])

    @r.post("/turn")
    async def turn(audio: UploadFile = File(...)):
        try:
            raw = await audio.read()
            wav = _to_wav(raw, audio.filename or "audio.webm")
            return pipeline.process(wav)
        except Exception as e:
            raise HTTPException(500, str(e))

    return r
