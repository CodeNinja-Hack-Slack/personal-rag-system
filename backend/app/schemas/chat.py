from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    query: str
    top_k: Optional[int] = None


class SourceDocument(BaseModel):
    id: str
    document: str
    metadata: dict
    score: Optional[float] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
