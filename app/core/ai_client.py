from functools import lru_cache
from openai import OpenAI

from app.core.config import settings


@lru_cache
def get_openai_client() -> OpenAI:
    return OpenAI(
        base_url=settings.BASE_URL,
        api_key=settings.OPENAI_API_KEY,
    )
