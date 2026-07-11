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
        """Fetches content from a URL and saves it to raw_data."""
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
        # Implementation for MasterAgent.run interface
        return self.fetch_url(task)

    def process_raw_data(self):
        """Processes files in raw_data and moves them to RAG memory."""
        for filename in os.listdir(self.raw_data_dir):
            filepath = os.path.join(self.raw_data_dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()

                    self.memory.add_document(
                        text=content,
                        metadata={"source": filename},
                        doc_id=filename
                    )
                    logging.info(f"Vectorized {filename} into ChromaDB")
                except Exception as e:
                    logging.error(f"Failed to process {filename}: {e}")
