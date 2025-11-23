from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    log_level: str = "DEBUG"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

