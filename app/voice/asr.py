import os, tempfile
from faster_whisper import WhisperModel

class ASRService:
    def __init__(self, model_name, device, compute_type):
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, audio_bytes):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            path = f.name
        try:
            # Small CPU instances are much faster with greedy decoding than beam search.
            segments, info = self.model.transcribe(
                path,
                beam_size=1,
                best_of=1,
                vad_filter=True,
                condition_on_previous_text=False,
            )
            text = " ".join(s.text.strip() for s in segments).strip()
            return {"text": text, "language": info.language}
        finally:
            os.unlink(path)
