import os
from core.memory import MemoryManager
from core.context_manager import ContextManager

class ProjectIndexer:
    def __init__(self):
        self.memory = MemoryManager()
        self.context = ContextManager(self.memory)

    def execute(self, root_dir: str = "."):
        """Indexes all .py and .md files in the project."""
        indexed_count = 0
        for root, dirs, files in os.walk(root_dir):
            if any(p in root for p in [".git", "venv", "__pycache__", "data"]):
                continue

            for file in files:
                if file.endswith((".py", ".md", ".json")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        self.context.chunk_and_store(content, source=path, metadata={"type": "project_code"})
                        indexed_count += 1
                    except: pass

        return f"Project indexing complete. {indexed_count} files processed and chunked."
