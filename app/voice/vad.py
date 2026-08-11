import io, wave
from threading import Lock
import numpy as np

class VADService:
    def __init__(self, threshold):
        self.threshold = threshold
        self.model = None
        self.get_speech_timestamps = None
        self.torch = None
        self.model_lock = Lock()

    @property
    def is_loaded(self):
        return self.model is not None

    def _get_model(self):
        if self.model is None:
            with self.model_lock:
                if self.model is None:
                    import torch
                    from silero_vad import load_silero_vad, get_speech_timestamps
                    self.torch = torch
                    self.get_speech_timestamps = get_speech_timestamps
                    self.model = load_silero_vad()
        return self.model

    def analyze_wav_bytes(self, data):
        with wave.open(io.BytesIO(data), "rb") as wf:
            rate = wf.getframerate()
            channels = wf.getnchannels()
            width = wf.getsampwidth()
            raw = wf.readframes(wf.getnframes())
        if channels != 1 or width != 2 or rate not in (8000, 16000, 48000):
            raise ValueError("Expected mono 16-bit PCM WAV at 8k/16k/48kHz.")
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
        model = self._get_model()
        audio = self.torch.from_numpy(samples)
        ts = self.get_speech_timestamps(audio, model, threshold=self.threshold,
                                        sampling_rate=rate, return_seconds=True)
        duration = len(samples) / rate
        speech = sum(x["end"] - x["start"] for x in ts)
        return {"audio_duration_s": round(duration,3),
                "speech_duration_s": round(speech,3),
                "speech_ratio": round(speech/duration,3) if duration else 0,
                "segments": ts}
