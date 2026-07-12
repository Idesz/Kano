import ollama

class UnitTestSuiteCreator:
    def execute(self, code: str):
        prompt = f"Generate a comprehensive pytest suite for the following Python code. Cover edge cases and use mocks where appropriate.\nCode:\n{code}"
        response = ollama.generate(model="deepseek-coder", prompt=prompt)
        return response['response']
