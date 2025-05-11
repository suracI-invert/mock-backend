import uuid
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
import httpx
import os

from ..models.resources import ConvertAudio

router = APIRouter(prefix="/resources/v1", tags=["resources"])


@router.get("/audio/{id}")
async def get_audio(id: str):
    if not os.path.exists(f"./cache/audio/{id}.wav"):
        raise HTTPException(404, "Audio not found")
    return FileResponse(f"./cache/audio/{id}.wav")


@router.post("/audio/convert")
async def convert_audio(req: ConvertAudio):
    uid = uuid.uuid4().hex
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            "http://10.0.7.49:16002/tts", json={"content": req.transcript}
        )
        os.makedirs("./cache/audio", exist_ok=True)
        with open(f"./cache/audio/{uid}.wav", "wb") as f:
            f.write(response.content)
    return {"uid": uid}


@router.post("/audio/text")
async def convert_to_text(req: Request):
    async with httpx.AsyncClient(timeout=None) as client:
        data = await req.body()
        response = await client.post("http://10.0.7.49:16002/stt", content=data)
        if response.status_code == 200:
            segments = response.json()["segments"]
            return {"transcript": " ".join([segment["text"] for segment in segments])}
        else:
            raise HTTPException(response.status_code, response.text)
