import time
from .endpointing import EndpointingController

class VoicePipeline:
    def __init__(self, asr, vad, agent, settings):
        self.asr, self.vad, self.agent, self.settings = asr, vad, agent, settings

    def process(self, audio):
        started = time.perf_counter()
        t = time.perf_counter()
        vad = self.vad.analyze_wav_bytes(audio)
        vad_ms = (time.perf_counter()-t)*1000

        endpoint = EndpointingController(self.settings.endpoint_silence_ms,
                                          self.settings.min_speech_ms)
        endpoint_state = endpoint.evaluate(int(vad["speech_duration_s"]*1000))

        t = time.perf_counter()
        asr = self.asr.transcribe(audio)
        asr_ms = (time.perf_counter()-t)*1000

        t = time.perf_counter()
        result = self.agent.invoke({"query": asr["text"]})
        agent_ms = (time.perf_counter()-t)*1000

        return {
            "transcript": asr["text"],
            "response": result["response"],
            "sources": result.get("sources", []),
            "latency_ms": {
                "vad_ms": round(vad_ms,2),
                "asr_ms": round(asr_ms,2),
                "agent_ms": round(agent_ms,2),
                "end_to_end_ms": round((time.perf_counter()-started)*1000,2)
            },
            "voice_state": {
                "vad": vad,
                "endpointing": endpoint_state,
                "turn_taking": "user_turn_complete" if endpoint_state["endpointed"] else "waiting",
                "barge_in_enabled": self.settings.barge_in_enabled
            }
        }
