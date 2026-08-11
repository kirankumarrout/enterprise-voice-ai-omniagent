from fastapi import APIRouter, UploadFile, File, HTTPException

def knowledge_router(rag):
    r = APIRouter(prefix="/api/knowledge", tags=["knowledge"])
    @r.post("/upload")
    async def upload(file: UploadFile = File(...)):
        if file.filename.lower().split(".")[-1] not in {"txt","md","pdf"}:
            raise HTTPException(400, "Only TXT, MD and PDF files are supported.")
        name = rag.add_file(file.filename, await file.read())
        return {"ok": True, "filename": name, "chunks": len(rag.chunks)}
    return r

def voice_router(pipeline):
    r = APIRouter(prefix="/api/voice", tags=["voice"])
    @r.post("/turn")
    async def turn(audio: UploadFile = File(...)):
        try:
            return pipeline.process(await audio.read())
        except Exception as e:
            raise HTTPException(500, str(e))
    return r
