from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import model_validator, Field

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY:str
    ALGORITHM:str

    DATABASE_URL: Optional[str] = None

    @model_validator(mode='after')
    def get_database_url(cls, values):

        database_url = f"postgresql+asyncpg://{values.DB_USER}:{values.DB_PASS}@{values.DB_HOST}:{values.DB_PORT}/{values.DB_NAME}"

        values.DATABASE_URL = database_url
        return values

    class Config:
        env_file = ".env"

settings = Settings()

