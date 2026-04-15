from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    score: float
    lead_category: str
    call_to_action: str
    source: str  # "cache" or "llm"