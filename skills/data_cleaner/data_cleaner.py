import ollama
from core.model_router import ModelRouter

class DataCleaner:
    def __init__(self, model_router: ModelRouter = None):
        self.router = model_router or ModelRouter()

    def execute(self, data_description: str):
        prompt = f"Write a Python script using Pandas to clean and preprocess data described as: {data_description}. Handle missing values, outliers, and type conversions."
        # Fixed: use router instead of direct ollama call
        response = asyncio.run(self.router.generate_queued("coding", prompt)) if hasattr(self.router, "generate_queued") else ollama.generate(model=self.router.get_model_for_task("coding"), prompt=prompt)
        return response['response']

import asyncio
