import ollama
import logging

class ModelRouter:
    def __init__(self, default_model="llama3"):
        self.default_model = default_model
        self.categories = {
            "coding": ["deepseek-coder", "codellama", "starcoder"],
            "reasoning": ["llama3", "qwen", "mistral"],
            "chat": ["llama3", "gemma", "vicuna"]
        }
        self.available_models = []
        self.refresh_models()

    def refresh_models(self):
        """Fetches the list of available models from local Ollama instance."""
        try:
            response = ollama.list()
            self.available_models = [m['name'] for m in response.get('models', [])]
        except Exception as e:
            logging.error(f"Failed to fetch models from Ollama: {e}")
            self.available_models = []

    def get_model_for_task(self, task_type: str) -> str:
        """
        Returns the best available model for a given task type.
        task_type: 'coding', 'reasoning', 'chat'
        """
        self.refresh_models() # Ensure we have the latest list

        if not self.available_models:
            return self.default_model

        preferred_models = self.categories.get(task_type, [])

        # Check if any preferred model (or its variant) is available
        for preferred in preferred_models:
            for available in self.available_models:
                if preferred in available.lower():
                    return available

        # Fallback to any available model if no preferred found
        if self.available_models:
            # Try to find default_model in available
            for available in self.available_models:
                if self.default_model in available.lower():
                    return available
            return self.available_models[0]

        return self.default_model

if __name__ == "__main__":
    router = ModelRouter()
    print(f"Available models: {router.available_models}")
    print(f"Coding model: {router.get_model_for_task('coding')}")
    print(f"Reasoning model: {router.get_model_for_task('reasoning')}")
