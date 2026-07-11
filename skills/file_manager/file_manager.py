import os

class FileManager:
    def execute(self, action: str, filepath: str, content: str = None):
        if action == "read":
            with open(filepath, 'r') as f:
                return f.read()
        elif action == "write":
            with open(filepath, 'w') as f:
                f.write(content)
                return f"File written to {filepath}"
        elif action == "list":
            return os.listdir(filepath or ".")
        return "Unknown action"
