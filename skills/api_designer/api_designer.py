import ollama

class APIDesigner:
    def execute(self, requirements: str):
        prompt = f"Design a professional API specification for: {requirements}. Include endpoints, methods, and schema."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
