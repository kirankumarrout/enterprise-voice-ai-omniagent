from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    vad_threshold: float = 0.50
    min_speech_ms: int = 250
    endpoint_silence_ms: int = 700
    barge_in_enabled: bool = True
    data_dir: str = "data"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
