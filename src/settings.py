from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    HOST: str
    ALGORITHM: str
    SECRET_KEY: str
    
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file='.env')

settings = Settings()
print(settings.DB_URL)