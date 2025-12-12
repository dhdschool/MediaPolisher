from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_PRIVATE_KEY: str
