import ollama

class Fuzzer:
    def execute(self, target_function: str, input_schema: str):
        """Generates fuzzing vectors based on the input schema."""
        prompt = f"Generate 20 complex fuzzing input vectors for a function expecting: {input_schema}. Focus on edge cases, oversized buffers, and special characters."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
