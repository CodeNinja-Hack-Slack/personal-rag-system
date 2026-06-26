from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse, SourceDocument
from app.services.rag import retriever, reranker, generator

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    docs = retriever.retrieve(query=request.query, n_results=request.top_k)
    reranked = reranker.rerank(documents=docs)
    answer = generator.generate(query=request.query, context_docs=reranked)

    sources = [
        SourceDocument(
            id=doc["id"],
            document=doc["document"],
            metadata=doc["metadata"],
            score=doc.get("distance")
        )
        for doc in reranked
    ]

    return ChatResponse(answer=answer, sources=sources)
