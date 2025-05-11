from pydantic import BaseModel


class ConvertAudio(BaseModel):
    transcript: str
