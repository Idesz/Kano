import ollama

class TDD:
    def execute(self, requirements: str):
        prompt = f"Follow TDD principles to design tests and implementation for: {requirements}. Start by writing the failing tests."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
