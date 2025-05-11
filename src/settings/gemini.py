from pydantic import BaseModel, SecretStr


class GeminiSettings(BaseModel):
    model: str
    api_key: SecretStr
