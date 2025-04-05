import os

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_GENERATE_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"

# CORS allowed origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://juici-agents.vercel.app",
    "https://juici-sandbox.vercel.app"
]

# Timeout settings (in seconds)
DEFAULT_TIMEOUT = 60
UPLOAD_TIMEOUT = 120

# Models
DEFAULT_VISION_MODEL = "llava"
DEFAULT_TEXT_MODEL = "llama3" 