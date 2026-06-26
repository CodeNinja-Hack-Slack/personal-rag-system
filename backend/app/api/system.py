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
    {"id": "mimo-v2.5-pro", "name": "MiMo v2.5 Pro", "provider": "mimo"},
    {"id": "mimo-v2-pro", "name": "MiMo v2 Pro", "provider": "mimo"},
    {"id": "gpt-4-turbo-preview", "name": "GPT-4 Turbo", "provider": "openai"},
    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"},
    {"id": "qwen2.5:7b", "name": "Qwen 2.5 7B (Ollama)", "provider": "ollama"},
]


class ModelSwitchRequest(BaseModel):
    provider: str
    model_id: str


@router.get("/system/models")
async def list_models():
    return {
        "models": AVAILABLE_MODELS,
        "current_provider": settings.llm_provider,
        "current_model": settings.mimo_model if settings.llm_provider == "mimo" else settings.openai_model if settings.llm_provider == "openai" else settings.ollama_model,
    }


@router.post("/system/models/switch")
async def switch_model(request: ModelSwitchRequest):
    return {
        "message": f"请修改 .env 文件中的 LLM_PROVIDER={request.provider} 和对应的 MODEL 配置",
        "provider": request.provider,
        "model_id": request.model_id,
    }


@router.get("/system/stats")
async def get_stats(db: Session = Depends(get_db)):
    total_items = db.query(func.count(KnowledgeItem.id)).scalar()

    if settings.llm_provider == "mimo":
        llm_model = settings.mimo_model
    elif settings.llm_provider == "ollama":
        llm_model = settings.ollama_model
    else:
        llm_model = settings.openai_model

    return {
        "total_knowledge_items": total_items,
        "embedding_model": settings.embedding_model,
        "vector_db": "chroma",
        "llm_provider": settings.llm_provider,
        "llm_model": llm_model,
    }
