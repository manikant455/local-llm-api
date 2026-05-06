import httpx
import time
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_HOST
        self.model = settings.DEFAULT_MODEL
        self.client = httpx.AsyncClient(timeout=60.0)

    async def generate(self, prompt: str, model: str = None) -> dict:
        """Generate text from prompt"""
        model = model or self.model
        start_time = time.time()

        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": settings.MAX_TOKENS
                    }
                }
            )
            response.raise_for_status()
            data = response.json()

            latency = round(time.time() - start_time, 2)
            tokens = data.get("eval_count", 0)
            tokens_per_sec = round(tokens / latency, 2) if latency > 0 else 0

            return {
                "model": model,
                "response": data.get("response", ""),
                "tokens": tokens,
                "latency_seconds": latency,
                "tokens_per_second": tokens_per_sec,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Ollama generate failed: {e}")
            return {
                "model": model,
                "response": f"Error: {str(e)}",
                "tokens": 0,
                "latency_seconds": 0,
                "tokens_per_second": 0,
                "status": "error",
                "error": str(e)
            }

    async def chat(self, messages: list, model: str = None) -> dict:
        """Chat with model"""
        model = model or self.model
        start_time = time.time()

        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "num_predict": settings.MAX_TOKENS
                    }
                }
            )
            response.raise_for_status()
            data = response.json()

            latency = round(time.time() - start_time, 2)
            tokens = data.get("eval_count", 0)
            tokens_per_sec = round(tokens / latency, 2) if latency > 0 else 0

            return {
                "model": model,
                "message": data.get("message", {}).get("content", ""),
                "tokens": tokens,
                "latency_seconds": latency,
                "tokens_per_second": tokens_per_sec,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Ollama chat failed: {e}")
            return {
                "model": model,
                "message": f"Error: {str(e)}",
                "tokens": 0,
                "latency_seconds": 0,
                "tokens_per_second": 0,
                "status": "error",
                "error": str(e)
            }

    async def list_models(self) -> dict:
        """List available models"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return {
                "models": [m["name"] for m in data.get("models", [])],
                "status": "success"
            }
        except Exception as e:
            return {
                "models": [],
                "status": "error",
                "error": str(e)
            }

    async def close(self):
        await self.client.aclose()
