import ollama
import base64

class VisualAnalyzer:
    def execute(self, image_path: str, prompt: str = "Describe this image."):
        """Analyzes an image using Ollama's vision models (e.g., llava)."""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            response = ollama.generate(
                model="llava", # Assuming llava is available for vision
                prompt=prompt,
                images=[image_data]
            )
            return response['response']
        except Exception as e:
            return f"Visual analysis error: {e}"
