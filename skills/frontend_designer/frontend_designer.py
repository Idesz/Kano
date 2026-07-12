import ollama

class FrontendDesigner:
    def execute(self, requirements: str):
        prompt = f"Design a modern, responsive frontend component based on these requirements: {requirements}. Use Tailwind CSS and React if applicable. Return code only."
        response = ollama.generate(model="deepseek-coder", prompt=prompt)
        return response['response']
