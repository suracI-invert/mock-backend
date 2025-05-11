from enum import Enum
from datetime import datetime
from typing import Any


class Level(int, Enum):
    A1 = 1
    A2 = 2
    B1 = 3
    B2 = 4
    C1 = 5
    C2 = 6


class LessonType(str, Enum):
    READING = "reading"
    LISTENING = "listening"
    SPEAKING = "speaking"


def validate_datetime(v: datetime | str | Any):
    if isinstance(v, datetime):
        return v
    if isinstance(v, str):
        return datetime.fromisoformat(v)
    raise ValueError()
