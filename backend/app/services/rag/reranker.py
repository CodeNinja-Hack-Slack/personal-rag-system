from typing import List, Dict, Any


class Reranker:
    def rerank(self, documents: List[Dict[str, Any]], top_k: int = None) -> List[Dict[str, Any]]:
        if not documents:
            return []

        sorted_docs = sorted(documents, key=lambda d: d.get("distance") or 0.0)

        if top_k is not None:
            sorted_docs = sorted_docs[:top_k]

        return sorted_docs


reranker = Reranker()
