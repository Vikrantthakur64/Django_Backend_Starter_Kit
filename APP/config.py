
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    VECTOR_DB_PATH: str = "data/vector_store"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o-mini"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
