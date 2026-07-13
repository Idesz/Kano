import os
from core.memory import MemoryManager

class ContextManager:
    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager
        self.chunk_size = 1000 # Characters

    def chunk_and_store(self, content: str, source: str, metadata: dict = None):
        """Splits content into semantic chunks and stores them in ChromaDB."""
        chunks = [content[i:i + self.chunk_size] for i in range(0, len(content), self.chunk_size)]
        for i, chunk in enumerate(chunks):
            chunk_id = f"{source}_chunk_{i}"
            meta = metadata or {}
            meta.update({"source": source, "chunk_index": i})
            self.memory.add_document(text=chunk, metadata=meta, doc_id=chunk_id)
        return len(chunks)

    def retrieve_relevant_context(self, query: str, n_results: int = 5):
        """Retrieves relevant chunks based on a query."""
        results = self.memory.search(query, n_results=n_results)
        return "\n---\n".join(results.get("documents", [[]])[0])
