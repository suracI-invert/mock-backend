from dataclasses import dataclass


@dataclass
class Context:
    user_name: str
    session_id: str
    lang: str
