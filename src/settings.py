from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file='.env')

DB_URL = Settings().DB_URL