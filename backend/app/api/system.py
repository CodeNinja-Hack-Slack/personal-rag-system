from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.sqlite import get_db
from app.models.knowledge import KnowledgeItem
from app.core.config import settings

router = APIRouter()


@router.get("/system/models")
async def list_models():
    models = [
        {"id": "gpt-4-turbo-preview", "name": "GPT-4 Turbo", "provider": "openai"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"},
        {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "provider": "anthropic"},
        {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "provider": "anthropic"},
    ]
    return {"models": models, "current_model": settings.openai_model}


@router.get("/system/stats")
async def get_stats(db: Session = Depends(get_db)):
    total_items = db.query(func.count(KnowledgeItem.id)).scalar()
    return {
        "total_knowledge_items": total_items,
        "embedding_model": settings.embedding_model,
        "vector_db": "chroma",
        "llm_model": settings.openai_model,
    }
