from pydantic import BaseModel
from fastapi import Response


class STTRequest(BaseModel):
    data: bytes


class AudioSegment(BaseModel):
    start: float
    end: float
    text: str


class STTResponse(BaseModel):
    segments: list[AudioSegment]


class TTSRequest(BaseModel):
    content: str


class TTSResponse(Response):
    media_type = "audio/x-wav"
