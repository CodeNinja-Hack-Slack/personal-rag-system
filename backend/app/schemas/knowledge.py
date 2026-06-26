from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class KnowledgeCreate(BaseModel):
    title: str
    content: str
    content_type: str
    source: Optional[str] = None
    language: str = "zh"
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class KnowledgeResponse(BaseModel):
    id: str
    title: str
    content: str
    content_type: str
    source: Optional[str]
    language: str
    tags: List[str]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime
    version: int

    class Config:
        from_attributes = True


class KnowledgeList(BaseModel):
    items: List[KnowledgeResponse]
    total: int


class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None
    source: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class KnowledgeImport(BaseModel):
    items: List[KnowledgeCreate]


class SearchResult(BaseModel):
    content: str
    metadata: dict
    distance: Optional[float] = None


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
