import ollama

class PRDGenerator:
    def execute(self, idea: str):
        prompt = f"Convert the following idea into a professional, structured Product Requirements Document (PRD).\nIdea: {idea}"
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
