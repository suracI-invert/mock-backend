from pydantic import BaseModel, SecretStr, HttpUrl


class AuthSettings(BaseModel):
    client_id: str
    client_secret: SecretStr
    redirect_uri: HttpUrl
