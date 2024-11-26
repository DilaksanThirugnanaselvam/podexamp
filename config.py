# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


@lru_cache
def get_settings():
    return settings


env_vars = get_settings()
