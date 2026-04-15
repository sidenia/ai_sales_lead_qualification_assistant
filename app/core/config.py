import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
import httpx
from openai import OpenAI, AsyncOpenAI


class Settings(BaseModel):
    # API Keys
    openai_api_key: str

    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    auth_dir: Path = base_dir / ".." / "auth"
    data_dir: Path = base_dir / "data"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def knowledge_file_path(self) -> Path:
        return self.data_dir / "knowledge.json"

    @property
    def openai_key_file_path(self) -> Path:
        return self.auth_dir / "openai_key.txt"



def load_settings() -> Settings:
    """Load settings from environment or files."""
    auth_dir = Path(__file__).parent.parent.parent / ".." / "auth"
    key_file = auth_dir / "openai_key.txt"

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key and key_file.exists():
        with open(key_file, "r") as f:
            api_key = f.read().strip()

    if not api_key:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY env var or place key in ../auth/openai_key.txt")

    return Settings(openai_api_key=api_key)


settings = None

try:
    settings = load_settings()
except ValueError:
    # During testing or when API key is not available
    settings = None

# OpenAI clients
if settings is not None:
    async_openai_client = AsyncOpenAI(
        api_key=settings.openai_api_key,
        http_client=httpx.AsyncClient(timeout=30)
    )

    openai_client = OpenAI(
        api_key=settings.openai_api_key,
        http_client=httpx.Client(timeout=30)
    )
else:
    # For testing when no API key is available
    async_openai_client = None
    openai_client = None