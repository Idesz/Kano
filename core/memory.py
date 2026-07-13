import chromadb
import os

class MemoryManager:
    def __init__(self, db_path="data/chromadb"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="kano_memory")
        self.graph_collection = self.client.get_or_create_collection(name="kano_graph")

    def add_document(self, text, metadata=None, doc_id=None):
        self.collection.add(
            documents=[text],
            metadatas=[metadata] if metadata else None,
            ids=[doc_id] if doc_id else [str(os.urandom(8).hex())]
        )

    def add_relationship(self, source_id, relation_type, target_id):
        """Simple Knowledge Graph relationship storage."""
        self.graph_collection.add(
            documents=[f"{source_id} {relation_type} {target_id}"],
            metadatas=[{"source": source_id, "relation": relation_type, "target": target_id}],
            ids=[f"rel_{os.urandom(4).hex()}"]
        )

    def search(self, query, n_results=5):
        return self.collection.query(query_texts=[query], n_results=n_results)

    def get_related_entities(self, entity_id):
        return self.graph_collection.query(query_texts=[entity_id], n_results=10)
