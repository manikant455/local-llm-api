from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

router = APIRouter()

class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "llama3.2"

class ChatResponse(BaseModel):
    model: str
    message: str
    tokens: int
    latency_seconds: float
    tokens_per_second: float
    status: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with local AI model"""
    from app.services.ollama_client import OllamaClient
    
    ollama = OllamaClient()
    messages_dict = [{"role": m.role, "content": m.content} for m in request.messages]
    result = await ollama.chat(messages_dict, request.model)
    await ollama.close()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result
