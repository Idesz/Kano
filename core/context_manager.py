import os
from core.memory import MemoryManager

class ContextManager:
    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager
        self.chunk_size = 1000

    def chunk_and_store(self, content: str, source: str, metadata: dict = None):
        """Splits content into chunks based on line breaks to preserve structure."""
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0

        for line in lines:
            if current_size + len(line) > self.chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            current_chunk.append(line)
            current_size += len(line)

        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        for i, chunk in enumerate(chunks):
            chunk_id = f"{source}_chunk_{i}"
            meta = metadata or {}
            meta.update({"source": source, "chunk_index": i})
            self.memory.add_document(text=chunk, metadata=meta, doc_id=chunk_id)
        return len(chunks)

    def retrieve_relevant_context(self, query: str, n_results: int = 5):
        results = self.memory.search(query, n_results=n_results)
        return "\n---\n".join(results.get("documents", [[]])[0])
