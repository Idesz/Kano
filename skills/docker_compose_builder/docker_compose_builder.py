import ollama

class DockerComposeBuilder:
    def execute(self, services: list):
        prompt = f"Generate a production-ready docker-compose.yml file for these services: {services}. Include networking, volumes, and healthchecks."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
