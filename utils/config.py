from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    db_url: str
    api_key_secret: str

    model_config = SettingsConfigDict(env_file=".env",extra='ignore',case_sensitive=False)


settings = Settings()

@lru_cache()
def get_settings() -> Settings:
    return settings