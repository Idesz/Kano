import chromadb
from chromadb.config import Settings
import os

class MemoryManager:
    def __init__(self, db_path="data/chromadb"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="kano_memory")

    def add_document(self, text, metadata=None, doc_id=None):
        self.collection.add(
            documents=[text],
            metadatas=[metadata] if metadata else None,
            ids=[doc_id] if doc_id else [str(os.urandom(8).hex())]
        )

    def search(self, query, n_results=5):
        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

    def delete_document(self, doc_id):
        self.collection.delete(ids=[doc_id])
