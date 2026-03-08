"""budAI Configuration — Settings from environment variables."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Default routing strategy
    default_strategy: str = "cheapest"  # cheapest | fastest | best

    # API Keys
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    together_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None  # Optional, works without
    openrouter_api_key: Optional[str] = None  # Free models available

    # Vector Store
    chroma_persist_dir: str = "./data/chroma_db"

    # Self-hosted vLLM (optional)
    vllm_base_url: Optional[str] = None
    vllm_model: Optional[str] = None

    # RAG defaults
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
