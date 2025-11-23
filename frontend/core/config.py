from pydantic_settings import BaseSettings
from functools import lru_cache


class FrontendSettings(BaseSettings):
    backend_api_url: str = "http://localhost:8000"
    frontend_host: str = "localhost"
    frontend_port: int = 8501
    log_level: str = "DEBUG"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_frontend_settings() -> FrontendSettings:
    return FrontendSettings()

