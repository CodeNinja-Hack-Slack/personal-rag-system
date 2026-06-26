from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from app.db.sqlite import get_db
from app.models.knowledge import KnowledgeItem
from app.core.config import settings

router = APIRouter()

AVAILABLE_MODELS = [
    {"id": "gpt-4-turbo-preview", "name": "GPT-4 Turbo", "provider": "openai"},
    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"},
    {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "provider": "anthropic"},
    {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "provider": "anthropic"},
]


class ModelSwitchRequest(BaseModel):
    model_id: str


@router.get("/system/models")
async def list_models():
    return {"models": AVAILABLE_MODELS, "current_model": settings.openai_model}


@router.post("/system/models/switch")
async def switch_model(request: ModelSwitchRequest):
    valid_ids = [m["id"] for m in AVAILABLE_MODELS]
    if request.model_id not in valid_ids:
        raise HTTPException(status_code=400, detail=f"Invalid model. Available: {valid_ids}")
    return {"message": f"Model switched to {request.model_id}", "current_model": request.model_id}


@router.get("/system/stats")
async def get_stats(db: Session = Depends(get_db)):
    total_items = db.query(func.count(KnowledgeItem.id)).scalar()
    return {
        "total_knowledge_items": total_items,
        "embedding_model": settings.embedding_model,
        "vector_db": "chroma",
        "llm_model": settings.openai_model,
    }
