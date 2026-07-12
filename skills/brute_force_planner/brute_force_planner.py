import ollama

class BruteForcePlanner:
    def execute(self, service: str, target: str):
        prompt = f"Create a brute-force attack plan for {service} on {target}. Suggest wordlists (RockYou, etc.) and tools like Hydra or Medusa with command examples."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
