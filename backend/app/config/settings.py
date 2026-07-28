from pathlib import Path
from pydantic_settings import BaseSettings

_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
_BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    MONGODB_URI: str
    DATABASE_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHROMA_DB_PATH: str = str(_BASE_DIR / "chroma_db")

    model_config = {"env_file": str(_ENV_FILE), "extra": "ignore"}


settings = Settings()
