import ollama

class XSSScanner:
    def execute(self, target_url: str):
        prompt = f"Generate XSS test payloads for '{target_url}'. Include reflected, stored, and DOM-based XSS vectors. Suggest filter bypass techniques."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
