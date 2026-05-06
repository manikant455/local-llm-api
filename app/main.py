from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api import generate, chat
from app.core.config import settings
from app.services.ollama_client import OllamaClient

app = FastAPI(
    title=settings.APP_NAME,
    description="Local AI Model API using Ollama - Run open-source LLMs locally",
    version=settings.VERSION,
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api/v1", tags=["Generate"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "default_model": settings.DEFAULT_MODEL,
        "endpoints": {
            "generate": "/api/v1/generate",
            "chat": "/api/v1/chat",
            "models": "/api/v1/models",
            "compare": "/api/v1/compare",
            "health": "/api/v1/health"
        }
    }

@app.get("/api/v1/models")
async def list_models():
    """List available Ollama models"""
    client = OllamaClient()
    result = await client.list_models()
    await client.close()
    return result

@app.get("/api/v1/health")
async def health():
    """Check if Ollama is running"""
    client = OllamaClient()
    result = await client.list_models()
    await client.close()
    return {
        "ollama_status": result["status"],
        "models_available": len(result.get("models", [])),
        "default_model": settings.DEFAULT_MODEL
    }

@app.post("/api/v1/compare")
async def compare_models(request: dict):
    """Compare two models on same prompt"""
    from app.services.prompt_builder import PromptBuilder
    
    prompt = request.get("prompt", "Explain what is AI in one sentence")
    model1 = request.get("model1", "llama3.2")
    model2 = request.get("model2", "mistral")
    
    client = OllamaClient()
    
    result1 = await client.generate(prompt, model1)
    result2 = await client.generate(prompt, model2)
    
    comparison_prompt = PromptBuilder.compare_models(
        prompt, model1, result1["response"], model2, result2["response"]
    )
    comparison = await client.generate(comparison_prompt)
    
    await client.close()
    
    return {
        "prompt": prompt,
        "model1": {
            "name": model1,
            "response": result1["response"],
            "latency": result1["latency_seconds"],
            "tokens": result1["tokens"],
            "tokens_per_second": result1["tokens_per_second"]
        },
        "model2": {
            "name": model2,
            "response": result2["response"],
            "latency": result2["latency_seconds"],
            "tokens": result2["tokens"],
            "tokens_per_second": result2["tokens_per_second"]
        },
        "comparison": comparison["response"]
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
