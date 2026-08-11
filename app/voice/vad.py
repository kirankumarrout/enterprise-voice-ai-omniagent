import io, wave
import numpy as np
import torch
from silero_vad import load_silero_vad, get_speech_timestamps

class VADService:
    def __init__(self, threshold):
        self.threshold = threshold
        self.model = load_silero_vad()

    def analyze_wav_bytes(self, data):
        with wave.open(io.BytesIO(data), "rb") as wf:
            rate = wf.getframerate()
            channels = wf.getnchannels()
            width = wf.getsampwidth()
            raw = wf.readframes(wf.getnframes())
        if channels != 1 or width != 2 or rate not in (8000, 16000, 48000):
            raise ValueError("Expected mono 16-bit PCM WAV at 8k/16k/48kHz.")
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
        audio = torch.from_numpy(samples)
        ts = get_speech_timestamps(audio, self.model, threshold=self.threshold,
                                   sampling_rate=rate, return_seconds=True)
        duration = len(samples) / rate
        speech = sum(x["end"] - x["start"] for x in ts)
        return {"audio_duration_s": round(duration,3),
                "speech_duration_s": round(speech,3),
                "speech_ratio": round(speech/duration,3) if duration else 0,
                "segments": ts}
