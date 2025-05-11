from pydantic_ai.messages import ModelMessage

from enum import Enum


class SpeakingPart(str, Enum):
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"


conversation_histories: dict[str, dict[SpeakingPart, list[ModelMessage]]] = {}


def parse_history_format(history: list[ModelMessage]):
    new_history = []
    for mm in history:
        if mm.kind == "request":
            for part in mm.parts:
                if part.part_kind == "user-prompt":
                    new_history.append({"role": "user", "content": part.content})
        elif mm.kind == "response":
            for part in mm.parts:
                if part.part_kind == "text":
                    new_history.append({"role": "assistant", "content": part.content})
    import json

    return json.dumps(new_history, indent=4)


def get_conversation_history(session_id: str, part: SpeakingPart) -> list[ModelMessage]:
    all_conversations = conversation_histories.get(session_id, {})
    if part in all_conversations:
        return all_conversations[part]
    return []


def save_conversation_history(
    session_id: str, part: SpeakingPart, history: list[ModelMessage]
):
    if session_id not in conversation_histories:
        conversation_histories[session_id] = {part: history}
        return
    conversation_histories[session_id][part] = history


def delete_conversation_history(session_id: str):
    conversation_histories.pop(session_id, None)


def unload_conversation_history(session_id: str):
    new_h = {}
    if session_id not in conversation_histories:
        return {}
    for part, history in conversation_histories[session_id].items():
        new_h[part.value] = parse_history_format(history)

    return new_h
