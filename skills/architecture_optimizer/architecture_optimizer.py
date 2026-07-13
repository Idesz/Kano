import ollama
from core.model_router import ModelRouter

class ArchitectureOptimizer:
    def __init__(self, model_router: ModelRouter = None):
        self.router = model_router or ModelRouter()

    def execute(self, codebase_summary: str):
        prompt = f"Analyze the following codebase architecture and suggest optimizations.\n\nSummary:\n{codebase_summary}"
        model = self.router.get_model_for_task("reasoning")
        response = ollama.generate(model=model, prompt=prompt)
        return response['response']
