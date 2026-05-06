
# 🤖 Local AI Model API

> Run open-source LLMs locally with FastAPI. No cloud, no API keys, no costs. Built with Ollama.

## ✨ Features

- **Run AI Locally**: LLaMA 3.2, Mistral, and more on your machine
- **Generate API**: Text generation endpoint
- **Chat API**: Multi-turn conversations
- **Model Comparison**: Compare different models side-by-side
- **Performance Metrics**: Latency, tokens/sec, token count
- **Free & Unlimited**: No API costs, no rate limits

## 🛠️ Tech Stack

- **Ollama**: Local LLM runtime
- **FastAPI**: API framework
- **LLaMA 3.2 / Mistral**: Open-source models
- **Docker**: Containerized deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- 8GB+ RAM (for models)

### Method 1: Local

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.2

# Clone & setup
git clone https://github.com/manikant455/local-llm-api.git
cd local-llm-api

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload --port 8001

Method 2: Docker
bash
git clone https://github.com/manikant455/local-llm-api.git
cd local-llm-api

docker-compose up --build

# Pull model inside container
docker exec ollama-server ollama pull llama3.2

📚 API Endpoints
Method	Endpoint	Description
POST	/api/v1/generate	Generate text
POST	/api/v1/chat	Chat with model
GET	/api/v1/models	List models
POST	/api/v1/compare	Compare models
GET	/api/v1/health	Health check

Usage

# Generate
curl -X POST http://localhost:8001/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain FastAPI in one sentence", "model": "llama3.2"}'

# Chat
curl -X POST http://localhost:8001/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is Python?"}], "model": "llama3.2"}'

# List models
curl http://localhost:8001/api/v1/models

# Compare models
curl -X POST http://localhost:8001/api/v1/compare \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?", "model1": "llama3.2", "model2": "mistral"}'

📊 Sample Response
json
{
  "model": "llama3.2",
  "response": "FastAPI is a modern Python web framework...",
  "tokens": 25,
  "latency_seconds": 1.45,
  "tokens_per_second": 17.24,
  "status": "success"
}

💰 Cost Comparison
Local (Ollama)	OpenAI API
Cost	$0	~$0.002/1K tokens
Latency	Depends on hardware	~1-2 seconds
Rate Limit	Unlimited	Tiered
Privacy	100% Private	Data sent to cloud
Offline	✅ Yes	❌ No

🎯 Why This Matters
No API Key Required: Works completely offline

Zero Cost: Run inference as much as you want

Privacy: Your data never leaves your machine

Customizable: Use any open-source model

👤 Author
Manikant

GitHub: @manikant455
