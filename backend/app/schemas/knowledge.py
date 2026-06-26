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
