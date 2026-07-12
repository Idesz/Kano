import ollama

class FastAPIRouteBuilder:
    def execute(self, resource_name: str, fields: dict):
        prompt = f"Create a FastAPI router for '{resource_name}' with CRUD operations. Fields: {fields}. Use Pydantic schemas and Ponytail efficiency."
        response = ollama.generate(model="deepseek-coder", prompt=prompt)
        return response['response']
