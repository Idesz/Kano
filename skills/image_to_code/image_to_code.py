import ollama

class ImageToCode:
    def execute(self, image_description: str):
        prompt = f"Convert the following visual/image description into clean HTML/CSS code: {image_description}"
        response = ollama.generate(model="deepseek-coder", prompt=prompt)
        return response['response']
