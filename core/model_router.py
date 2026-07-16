import ollama
import logging
import time
import asyncio

class ModelRouter:
    _instance_semaphore = None

    def __init__(self, default_model="dolphin-llama3", cache_ttl=300):
        self.default_model = default_model
        self.cache_ttl = cache_ttl
        self.last_refresh = 0
        # Categories prioritized for Uncensored/High Performance
        self.categories = {
            "coding": ["dolphin-coder", "deepseek-coder", "codellama"],
            "reasoning": ["dolphin-mixtral", "dolphin-llama3", "llama3"],
            "chat": ["dolphin-llama3", "dolphin-mistral", "gemma"],
            "vision": ["llava", "moondream"]
        }
        self.available_models = []
        self.refresh_models()

    def _get_semaphore(self):
        if ModelRouter._instance_semaphore is None:
            ModelRouter._instance_semaphore = asyncio.Semaphore(3)
        return ModelRouter._instance_semaphore

    def refresh_models(self, force=False):
        current_time = time.time()
        if not force and (current_time - self.last_refresh < self.cache_ttl) and self.available_models:
            return
        try:
            response = ollama.list()
            self.available_models = [m['name'] for m in response.get('models', [])]
            self.last_refresh = current_time
        except Exception:
            if not self.available_models: self.available_models = []

    def get_model_for_task(self, task_type: str) -> str:
        self.refresh_models()
        if not self.available_models: return self.default_model
        preferred = self.categories.get(task_type, [])
        for p in preferred:
            for av in self.available_models:
                if p in av.lower(): return av
        return self.available_models[0] if self.available_models else self.default_model

    async def generate_queued(self, task_type: str, prompt: str, **kwargs):
        model = self.get_model_for_task(task_type)
        async with self._get_semaphore():
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: ollama.generate(model=model, prompt=prompt, **kwargs))
            return response
