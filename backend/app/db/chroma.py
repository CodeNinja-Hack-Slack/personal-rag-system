import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings


class ChromaDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, ids: list, documents: list, metadatas: list):
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def query(self, query_text: str, n_results: int = None) -> dict:
        if n_results is None:
            n_results = settings.top_k_results
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

    def delete(self, ids: list):
        self.collection.delete(ids=ids)


chroma_db = ChromaDB()
