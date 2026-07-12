import ollama

class MetasploitHelper:
    def execute(self, objective: str):
        prompt = f"Provide Metasploit module recommendations and payload setup for: {objective}. Include msfconsole commands."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
