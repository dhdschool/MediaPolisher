from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_SERVICE_URL: str
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_prefix="MP_", env_file=".env")
