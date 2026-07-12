import ollama

class SystematicDebugger:
    def execute(self, error_log: str, code_context: str):
        prompt = f"Systematically debug the following error.\nLog:\n{error_log}\nContext:\n{code_context}\n\nProvide a step-by-step resolution plan."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
