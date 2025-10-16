import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

DOTENV = os.path.join(os.path.dirname(__file__), "../.env")

class Settings(BaseSettings):
    db_url: str
    api_key_secret: str
    jwt_rsa_private_key: str

    model_config = SettingsConfigDict(env_file=DOTENV,extra='ignore', case_sensitive=True)


settings = Settings()

@lru_cache()
def get_settings() -> Settings:
    return settings