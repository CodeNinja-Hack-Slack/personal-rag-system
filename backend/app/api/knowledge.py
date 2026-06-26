from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sqlite import get_db
from app.services.knowledge import knowledge_service
from app.schemas.knowledge import KnowledgeCreate, KnowledgeResponse, KnowledgeList

router = APIRouter()


@router.post("/knowledge", response_model=KnowledgeResponse)
async def create_knowledge(item: KnowledgeCreate, db: Session = Depends(get_db)):
    db_item = knowledge_service.create(
        db=db,
        title=item.title,
        content=item.content,
        content_type=item.content_type,
        source=item.source,
        language=item.language,
        tags=item.tags,
        category=item.category
    )
    return db_item


@router.get("/knowledge", response_model=KnowledgeList)
async def list_knowledge(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = knowledge_service.list(db, skip=skip, limit=limit)
    return {"items": items, "total": len(items)}


@router.get("/knowledge/{item_id}", response_model=KnowledgeResponse)
async def get_knowledge(item_id: str, db: Session = Depends(get_db)):
    item = knowledge_service.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Knowledge item not found")
    return item


@router.delete("/knowledge/{item_id}")
async def delete_knowledge(item_id: str, db: Session = Depends(get_db)):
    success = knowledge_service.delete(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Knowledge item not found")
    return {"message": "Knowledge item deleted successfully"}
