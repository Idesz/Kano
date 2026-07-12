import ollama

class SubdomainEnumerator:
    def execute(self, domain: str):
        prompt = f"Explain the best tools and commands (e.g., subfinder, amass, assetfinder) to enumerate subdomains for: {domain}"
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
