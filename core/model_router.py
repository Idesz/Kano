import ollama
import logging
import time
import asyncio
import os
import requests

class ModelRouter:
    _instance_semaphore = None

    def __init__(self, default_model="dolphin-llama3", cache_ttl=300):
        self.default_model = default_model
        self.cache_ttl = cache_ttl
        self.last_refresh = 0
        self.categories = {
            "coding": ["dolphin-coder", "deepseek-coder", "codellama"],
            "reasoning": ["dolphin-mixtral", "dolphin-llama3", "llama3"],
            "chat": ["dolphin-llama3", "dolphin-mistral", "gemma"],
            "vision": ["llava", "moondream"]
        }
        self.available_models = []
        self.use_cloud_fallback = False
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.refresh_models()

    def _get_semaphore(self):
        if ModelRouter._instance_semaphore is None:
            ModelRouter._instance_semaphore = asyncio.Semaphore(3)
        return ModelRouter._instance_semaphore

    def refresh_models(self, force=False):
        current_time = time.time()
        if not force and (current_time - self.last_refresh < self.cache_ttl) and self.available_models:
            return

        # Check local Ollama connectivity
        try:
            response = ollama.list()
            self.available_models = [m['name'] for m in response.get('models', [])]
            self.last_refresh = current_time
            self.use_cloud_fallback = False
            logging.info("Connected to local Ollama.")
        except Exception:
            logging.warning("Local Ollama unreachable. Checking for Cloud Fallback (Groq)...")
            self.available_models = []
            if self.groq_api_key:
                self.use_cloud_fallback = True
                logging.info("Cloud Fallback (Groq) engaged.")
            else:
                logging.error("No local Ollama found and GROQ_API_KEY is not set.")

    def get_model_for_task(self, task_type: str) -> str:
        self.refresh_models()
        if self.use_cloud_fallback:
            # Map categories to Groq cloud models
            groq_mappings = {
                "coding": "llama3-70b-8192",
                "reasoning": "llama3-70b-8192",
                "chat": "llama3-8b-8192",
                "vision": "llama3-8b-8192"
            }
            return groq_mappings.get(task_type, "llama3-8b-8192")

        if not self.available_models:
            return self.default_model

        preferred = self.categories.get(task_type, [])
        for p in preferred:
            for av in self.available_models:
                if p in av.lower(): return av
        return self.available_models[0] if self.available_models else self.default_model

    async def generate_queued(self, task_type: str, prompt: str, **kwargs):
        self.refresh_models()
        model = self.get_model_for_task(task_type)

        async with self._get_semaphore():
            loop = asyncio.get_event_loop()
            if self.use_cloud_fallback:
                # Call Groq Cloud API (OpenAI-compatible)
                return await loop.run_in_executor(None, self._call_groq_api, model, prompt)
            else:
                # Call local Ollama
                response = await loop.run_in_executor(None, lambda: ollama.generate(model=model, prompt=prompt, **kwargs))
                return response

    def _call_groq_api(self, model: str, prompt: str):
        """Performs a direct POST request to Groq API to avoid extra library dependencies."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=30)
            result = resp.json()
            # Standardize output format to match ollama's structure
            text = result["choices"][0]["message"]["content"]
            return {"response": text}
        except Exception as e:
            logging.error(f"Groq Cloud API Call Failed: {e}")
            return {"response": f"Cloud Fallback Error: {e}"}
