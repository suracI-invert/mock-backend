from pydantic import BaseModel, SecretStr


class RabbitMQSettings(BaseModel):
    scheme: str
    host: str
    port: int
    username: str
    password: SecretStr
