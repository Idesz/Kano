import ollama

class RegexMaster:
    def execute(self, requirement: str):
        prompt = f"Generate a robust regular expression for the following requirement: {requirement}. Explain each part of the regex."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
