import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    DOCKER_IMAGE = os.getenv("DOCKER_IMAGE", "python:3.11-slim")

    # Mandatory API Key without hardcoded fallback
    KANO_API_KEY = os.getenv("KANO_API_KEY")
    if not KANO_API_KEY:
        raise ValueError("KANO_API_KEY environment variable is not set. System initialization halted.")

    NMAP_PATH = os.getenv("NMAP_PATH", "nmap")
    DEFAULT_MODEL = "llama3"
    MODEL_CACHE_TTL = 300
