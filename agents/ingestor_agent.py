import os
import requests
from bs4 import BeautifulSoup
from core.memory import MemoryManager
from core.context_manager import ContextManager
from agents.base_agent import BaseAgent
import logging

class IngestorAgent(BaseAgent):
    def __init__(self, model_router=None, raw_data_dir="raw_data"):
        from core.model_router import ModelRouter
        router = model_router or ModelRouter()
        super().__init__("IngestorAgent", router)
        self.raw_data_dir = raw_data_dir
        self.memory = MemoryManager()
        self.context = ContextManager(self.memory)
        if not os.path.exists(self.raw_data_dir):
            os.makedirs(self.raw_data_dir)

    def fetch_url(self, url: str):
        if "youtube.com" in url or "youtu.be" in url:
            return f"Media URL detected. Routing to media_fetcher for: {url}"

        try:
            response = requests.get(url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)

            filename = f"web_{os.urandom(4).hex()}.txt"
            filepath = os.path.join(self.raw_data_dir, filename)
            with open(filepath, 'w') as f: f.write(text)

            # Unified Chunking Flow
            chunks = self.context.chunk_and_store(text, source=url, metadata={"type": "web_scrape"})
            return f"Data saved and split into {chunks} chunks for RAG."
        except Exception as e:
            return f"Error fetching URL: {e}"

    def run(self, task: str):
        return self.fetch_url(task)
