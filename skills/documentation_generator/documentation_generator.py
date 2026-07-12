import ollama

class DocumentationGenerator:
    def execute(self, code_summary: str):
        prompt = f"Create a comprehensive README.md and technical documentation based on this codebase summary:\n{code_summary}"
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
