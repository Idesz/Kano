import ollama

class RefactoringExpert:
    def execute(self, code: str):
        prompt = f"Analyze and refactor the following Python code for better readability, performance, and adherence to design patterns (SOLID, DRY). Code:\n{code}"
        response = ollama.generate(model="deepseek-coder", prompt=prompt)
        return response['response']
