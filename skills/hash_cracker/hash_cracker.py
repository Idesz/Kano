import ollama

class HashCracker:
    def execute(self, hash_value: str, hash_type: str = "auto"):
        prompt = f"Provide a guide to crack the following hash: '{hash_value}'. Suggested type: {hash_type}. Include Hashcat and John the Ripper command examples."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
