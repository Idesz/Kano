import os
import time
import threading
import ollama
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
            files = [f for f in os.listdir(self.raw_data_dir) if os.path.isfile(os.path.join(self.raw_data_dir, f))]
            if files:
                for filename in files:
                    if not self.running: break
                    self._process_file(filename)
            time.sleep(60) # Check every minute

    def _process_file(self, filename):
        filepath = os.path.join(self.raw_data_dir, filename)
        processed_dir = os.path.join(self.raw_data_dir, "processed")
        os.makedirs(processed_dir, exist_ok=True)

        try:
            with open(filepath, 'r') as f:
                content = f.read()

            # Summarize with LLM
            model = self.router.get_model_for_task("reasoning")
            prompt = f"Summarize the following content for a knowledge base. Focus on key facts and logic.\nContent:\n{content}"
            response = ollama.generate(model=model, prompt=prompt)
            summary = response['response']

            # Vectorize
            self.memory.add_document(
                text=summary,
                metadata={"source": filename, "type": "summary"},
                doc_id=f"summary_{filename}"
            )
            self.memory.add_document(
                text=content,
                metadata={"source": filename, "type": "raw"},
                doc_id=f"raw_{filename}"
            )

            # Move to processed
            os.rename(filepath, os.path.join(processed_dir, filename))
            print(f"Learned from {filename}")
        except Exception as e:
            print(f"Error learning from {filename}: {e}")
