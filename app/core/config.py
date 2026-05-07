from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # for adjusting environment variable
    app_name: str = "FastAPI RAG Docs Assistant"
    app_description: str = "A modular RAG API for document-based question answering."
    app_version: str = "0.1.0"
    debug: bool = True
    # these are lowercases but in .env they read in uppercase format
    # pydantic-settings do the mapping job
    
    BASE_URL: str
    OPENAI_API_KEY: str
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
settings = Settings()
# we make an instance that the entire of the project can import
# whenever we want to read the settings, we could just:
# from app.core.config import settings 