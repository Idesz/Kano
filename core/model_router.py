import ollama
import logging
import time
import asyncio

class ModelRouter:
    def __init__(self, default_model="llama3", cache_ttl=300):
        self.default_model = default_model
        self.cache_ttl = cache_ttl
        self.last_refresh = 0
        self.categories = {
            "coding": ["deepseek-coder", "codellama", "starcoder"],
            "reasoning": ["llama3", "qwen", "mistral"],
            "chat": ["llama3", "gemma", "vicuna"],
            "vision": ["llava", "moondream"]
        }
        self.available_models = []
        self.semaphore = asyncio.Semaphore(2) # Resource Queue: Limit to 2 concurrent LLM calls
        self.refresh_models()

    def refresh_models(self, force=False):
        current_time = time.time()
        if not force and (current_time - self.last_refresh < self.cache_ttl) and self.available_models:
            return

        try:
            response = ollama.list()
            self.available_models = [m['name'] for m in response.get('models', [])]
            self.last_refresh = current_time
            logging.info(f"Refreshed models: {self.available_models}")
        except Exception as e:
            logging.error(f"Failed to fetch models: {e}")
            if not self.available_models: self.available_models = []

    def get_model_for_task(self, task_type: str) -> str:
        self.refresh_models()
        if not self.available_models: return self.default_model
        preferred_models = self.categories.get(task_type, [])
        for preferred in preferred_models:
            for available in self.available_models:
                if preferred in available.lower(): return available
        if self.available_models:
            for available in self.available_models:
                if self.default_model in available.lower(): return available
            return self.available_models[0]
        return self.default_model

    async def generate_with_queue(self, **kwargs):
        """Asynchronous wrapper with semaphore to prevent GPU overloading."""
        async with self.semaphore:
            # Note: Using run_in_executor because ollama-python is synchronous
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: ollama.generate(**kwargs))
