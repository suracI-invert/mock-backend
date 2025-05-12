from pydantic import BaseModel


class ChatResponse(BaseModel):
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    user: str
    lang: str
