from utils import initialize, init_tts_model, save_wav, init_stt_model
import io
from models import (
    TTSRequest,
    TTSResponse,
    STTRequest,
    STTResponse,
    AudioSegment,
)
from fastapi import FastAPI, Request

model_path, config_path = initialize()

stt = init_stt_model()

tts = init_tts_model(model_path, config_path)

SAMPLE_RATE: int = tts.synthesizer.output_sample_rate if tts.synthesizer else 24000


app = FastAPI()


@app.post("/tts")
async def text_to_speech(req: TTSRequest) -> TTSResponse:
    wav = io.BytesIO()
    _res = tts.tts(req.content, speaker="Ana Florence", language="en")
    save_wav(wav=_res, sample_rate=SAMPLE_RATE, pipe_out=wav)
    return TTSResponse(content=wav.read())


@app.post("/stt")
async def speak_to_text(req: Request) -> STTResponse:
    data = await req.body()
    buffer = io.BytesIO(data)

    segments, _ = stt.transcribe(buffer, language="en")

    return STTResponse(
        segments=[AudioSegment(start=s.start, end=s.end, text=s.text) for s in segments]
    )
