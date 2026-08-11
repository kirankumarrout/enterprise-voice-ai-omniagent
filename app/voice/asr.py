import os, tempfile
from threading import Lock

class ASRService:
    def __init__(self, model_name, device, compute_type):
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self.model_lock = Lock()

    @property
    def is_loaded(self):
        return self.model is not None

    def _get_model(self):
        if self.model is None:
            with self.model_lock:
                if self.model is None:
                    from faster_whisper import WhisperModel
                    self.model = WhisperModel(
                        self.model_name,
                        device=self.device,
                        compute_type=self.compute_type,
                    )
        return self.model

    def transcribe(self, audio_bytes):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            path = f.name
        try:
            # Small CPU instances are much faster with greedy decoding than beam search.
            segments, info = self._get_model().transcribe(
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
