import ollama

class UIUXExpert:
    def execute(self, design_context: str):
        prompt = f"Analyze the following UI/UX context and provide professional improvement suggestions focusing on usability and aesthetics.\nContext: {design_context}"
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
