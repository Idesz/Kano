import ollama

class SQLiTester:
    def execute(self, target_url: str, db_type: str = "generic"):
        prompt = f"Generate SQL injection test payloads for '{target_url}' targeting a {db_type} database. Include error-based, union-based, and blind SQLi techniques."
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
