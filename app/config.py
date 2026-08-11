from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # tiny is intentionally the default for the free CPU Render instance.
    # Set WHISPER_MODEL=base/small only on a stronger machine.
    whisper_model: str = "tiny"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    vad_threshold: float = 0.50
    min_speech_ms: int = 150
    endpoint_silence_ms: int = 500
    barge_in_enabled: bool = True
    data_dir: str = "data"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
