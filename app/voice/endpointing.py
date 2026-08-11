class EndpointingController:
    def __init__(self, silence_ms=700, min_speech_ms=250):
        self.silence_ms = silence_ms
        self.min_speech_ms = min_speech_ms

    def evaluate(self, speech_ms):
        return {
            "speech_ms": speech_ms,
            "endpointed": speech_ms >= self.min_speech_ms,
            "silence_threshold_ms": self.silence_ms,
            "state": "endpointed" if speech_ms >= self.min_speech_ms else "waiting"
        }
