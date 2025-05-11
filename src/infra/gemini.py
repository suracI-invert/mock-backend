from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

from settings import get_settings


def get_gemini():
    return GeminiModel(
        get_settings().gemini.model,
        provider=GoogleGLAProvider(
            api_key=get_settings().gemini.api_key.get_secret_value()
        ),
    )
