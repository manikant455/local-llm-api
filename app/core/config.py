import os

class Settings:
    APP_NAME: str = "Local LLM API"
    VERSION: str = "1.0.0"
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama3.2")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "500"))

settings = Settings()
