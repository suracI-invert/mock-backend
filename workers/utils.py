import os
from typing import Union, Any
from pathlib import Path
import numpy as np
import scipy
from typing import BinaryIO

from TTS.api import TTS


def save_wav(
    *,
    wav: list[int],
    sample_rate: int,
    pipe_out: BinaryIO,
) -> None:
    _wav = np.array(wav)
    wav_norm = _wav * (32767 / max(0.01, np.max(np.abs(_wav))))

    wav_norm = wav_norm.astype(np.int16)

    scipy.io.wavfile.write(pipe_out, sample_rate, wav_norm)
    pipe_out.seek(0)


def initialize(path: str = ".storage"):
    print("Initializing...")
    from TTS.utils.manage import ModelManager
    from TTS import api

    os.environ["COQUI_TOS_AGREED"] = "1"

    full_path = path

    os.makedirs(full_path, exist_ok=True)

    manager = ModelManager(
        models_file=Path(api.__file__).parent / ".models.json",
        output_prefix=full_path,
        progress_bar=True,
    )

    model_path, config_path, _ = manager.download_model(
        "tts_models/multilingual/multi-dataset/xtts_v2"
    )
    return model_path.as_posix(), config_path.as_posix() if config_path else None


def init_tts_model(model_path: str, config_path: str | None):
    from torch.cuda import is_available

    tts = TTS(
        model_path=model_path,
        config_path=config_path,
    )

    if is_available():
        tts = tts.to("cuda")
    return tts


def init_stt_model(path: str = ".storage"):
    from faster_whisper import WhisperModel

    os.makedirs(path, exist_ok=True)

    model = WhisperModel(
        "distil-large-v3",
        device="cpu",
        compute_type="float32",
        download_root=path,
    )

    return model
