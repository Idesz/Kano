import ollama

class CICDPipelineDesigner:
    def execute(self, platform: str, tech_stack: str):
        prompt = f"Generate a {platform} pipeline configuration for a {tech_stack} project. Include stages for linting, testing, and deployment."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
