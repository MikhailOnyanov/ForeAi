from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ChromaConfig(BaseSettings):
    """Настройки Chroma."""
    model_config = SettingsConfigDict(env_prefix='CHROMA_')
    
    CLIENT_TYPE: str = "http"
    HOST: str = "127.0.0.1"
    PORT: int = 8000

class YandexGPTConfig(BaseSettings):
    """Настройки Yandex API"""
    model_config = SettingsConfigDict(env_prefix='YANDEX_')
    API_KEY: str = ""