import os
import requests
from bs4 import BeautifulSoup
from core.memory import MemoryManager
from agents.base_agent import BaseAgent
import logging

class IngestorAgent(BaseAgent):
    def __init__(self, model_router=None, raw_data_dir="raw_data"):
        from core.model_router import ModelRouter
        router = model_router or ModelRouter()
        super().__init__("IngestorAgent", router)
        self.raw_data_dir = raw_data_dir
        self.memory = MemoryManager()
        if not os.path.exists(self.raw_data_dir):
            os.makedirs(self.raw_data_dir)

    def fetch_url(self, url: str):
        if "youtube.com" in url or "youtu.be" in url:
            return f"Media URL detected. Routing to media_fetcher skill for: {url}"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            filename = f"web_{os.urandom(4).hex()}.txt"
            filepath = os.path.join(self.raw_data_dir, filename)
            with open(filepath, 'w') as f:
                f.write(text)
            return f"Data saved to {filepath}"
        except Exception as e:
            return f"Error fetching URL: {e}"

    def run(self, task: str):
        # MasterAgent already handles routing, this is a safety fallback
        return self.fetch_url(task)
