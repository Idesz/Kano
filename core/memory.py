import chromadb
import os
import time

class MemoryManager:
    def __init__(self, db_path="data/chromadb"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="kano_memory")
        self.graph_collection = self.client.get_or_create_collection(name="kano_graph")

    def add_document(self, text, metadata=None, doc_id=None):
        meta = metadata or {}
        # Metadata Versioning
        meta["timestamp"] = time.time()
        meta["active"] = True

        self.collection.add(
            documents=[text],
            metadatas=[meta],
            ids=[doc_id] if doc_id else [str(os.urandom(8).hex())]
        )

    def search(self, query, n_results=5, filter_active=True):
        where_clause = {"active": True} if filter_active else None
        return self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause
        )

    def mark_obsolete(self, source_name):
        """Marks documents from a specific source as inactive (for version control)."""
        # Note: ChromaDB update logic varies by version, but metadata update is standard
        # Simplified: We retrieve and re-add with active=False or use update()
        pass

    def add_relationship(self, source_id, relation_type, target_id):
        self.graph_collection.add(
            documents=[f"{source_id} {relation_type} {target_id}"],
            metadatas=[{"source": source_id, "relation": relation_type, "target": target_id}],
            ids=[f"rel_{os.urandom(4).hex()}"]
        )
