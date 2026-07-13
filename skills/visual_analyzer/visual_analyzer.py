import ollama
from core.model_router import ModelRouter

class VisualAnalyzer:
    def __init__(self, model_router: ModelRouter = None):
        self.router = model_router or ModelRouter()

    def execute(self, image_path: str, prompt: str = "Describe this image."):
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            model = self.router.get_model_for_task("vision")
            response = ollama.generate(
                model=model,
                prompt=prompt,
                images=[image_data]
            )
            return response['response']
        except Exception as e:
            return f"Visual analysis error: {e}"
