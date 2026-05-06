from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.services.ollama_client import OllamaClient

router = APIRouter()
ollama = OllamaClient()

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    model: Optional[str] = "llama3.2"

class GenerateResponse(BaseModel):
    model: str
    response: str
    tokens: int
    latency_seconds: float
    tokens_per_second: float
    status: str

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text from local AI model"""
    result = await ollama.generate(request.prompt, request.model)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result
