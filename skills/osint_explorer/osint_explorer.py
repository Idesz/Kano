import ollama

class OSINTExplorer:
    def execute(self, target: str):
        prompt = f"Outline a professional OSINT investigation plan for: {target}. Include tools like Maltego, Shodan, and social media techniques."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
