import os
import time
import threading
import ollama
import logging
from core.memory import MemoryManager
from core.model_router import ModelRouter

class IdleLearner:
    def __init__(self, raw_data_dir="raw_data"):
        self.raw_data_dir = raw_data_dir
        self.memory = MemoryManager()
        self.router = ModelRouter()
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._learning_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _learning_loop(self):
        while self.running:
            try:
                files = [f for f in os.listdir(self.raw_data_dir) if os.path.isfile(os.path.join(self.raw_data_dir, f))]
                if files:
                    for filename in files:
                        if not self.running: break
                        self._process_file(filename)
            except Exception as e:
                logging.error(f"Learner loop error: {e}")
            time.sleep(60)

    def _process_file(self, filename):
        filepath = os.path.join(self.raw_data_dir, filename)
        processed_dir = os.path.join(self.raw_data_dir, "processed")
        os.makedirs(processed_dir, exist_ok=True)

        try:
            with open(filepath, 'r') as f:
                content = f.read()

            model = self.router.get_model_for_task("reasoning")
            prompt = f"Summarize content for RAG knowledge base:\n{content}"
            response = ollama.generate(model=model, prompt=prompt)
            summary = response['response']

            self.memory.add_document(text=summary, metadata={"source": filename, "type": "summary"}, doc_id=f"summary_{filename}")
            self.memory.add_document(text=content, metadata={"source": filename, "type": "raw"}, doc_id=f"raw_{filename}")

            os.rename(filepath, os.path.join(processed_dir, filename))
            logging.info(f"Learned from {filename}")
        except Exception as e:
            logging.error(f"Error learning from {filename}: {e}")
