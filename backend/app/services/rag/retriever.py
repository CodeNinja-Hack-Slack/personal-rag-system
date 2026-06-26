from typing import List, Dict, Any
from app.db.chroma import chroma_db
from app.core.config import settings


class Retriever:
    def retrieve(self, query: str, n_results: int = None) -> List[Dict[str, Any]]:
        if n_results is None:
            n_results = settings.top_k_results

        results = chroma_db.query(query_text=query, n_results=n_results)

        documents = []
        for i in range(len(results["ids"][0])):
            documents.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if results.get("distances") else None,
            })

        return documents


retriever = Retriever()
