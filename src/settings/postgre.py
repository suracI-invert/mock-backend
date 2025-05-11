from pydantic import BaseModel, SecretStr


class PostgreSettings(BaseModel):
    host: str
    port: int
    username: str
    password: SecretStr
    db: str
