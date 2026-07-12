import ollama

class ArchitectureOptimizer:
    def execute(self, codebase_summary: str):
        # In a real scenario, this would read files. Here we use the summary provided.
        prompt = f"Analyze the following codebase architecture and suggest optimizations for modularity, scalability, and performance.\n\nSummary:\n{codebase_summary}"
        # We assume the Master Agent provides the router or we use default
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
