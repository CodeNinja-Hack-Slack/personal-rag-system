def __getattr__(name):
    if name == "retriever":
        from app.services.rag.retriever import retriever
        return retriever
    elif name == "reranker":
        from app.services.rag.reranker import reranker
        return reranker
    elif name == "generator":
        from app.services.rag.generator import generator
        return generator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["retriever", "reranker", "generator"]
