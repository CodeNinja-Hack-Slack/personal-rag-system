from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.knowledge import KnowledgeItem
from app.db.chroma import chroma_db
from app.services.parsers.markdown import markdown_parser
from app.services.parsers.code import code_parser
from app.services.parsers.webpage import webpage_parser
import uuid


class KnowledgeService:
    def create(self, db: Session, title: str, content: str, 
               content_type: str, source: str = None, 
               language: str = "zh", tags: list = None, 
               category: str = None) -> KnowledgeItem:
        if content_type == "markdown":
            chunks = markdown_parser.parse(content)
        elif content_type == "code":
            chunks = code_parser.parse(content)
        elif content_type == "webpage":
            chunks = webpage_parser.parse(content)
        else:
            chunks = [content]
        
        embedding_ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            chroma_db.add_documents(
                ids=[chunk_id],
                documents=[chunk],
                metadatas=[{
                    "title": title,
                    "content_type": content_type,
                    "chunk_index": i,
                    "language": language
                }]
            )
            embedding_ids.append(chunk_id)
        
        db_item = KnowledgeItem(
            title=title,
            content=content,
            content_type=content_type,
            source=source,
            language=language,
            tags=tags or [],
            category=category,
            embedding_id=",".join(embedding_ids)
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        return db_item
    
    def get(self, db: Session, item_id: str) -> Optional[KnowledgeItem]:
        return db.query(KnowledgeItem).filter(KnowledgeItem.id == item_id).first()
    
    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[KnowledgeItem]:
        return db.query(KnowledgeItem).offset(skip).limit(limit).all()
    
    def delete(self, db: Session, item_id: str) -> bool:
        item = db.query(KnowledgeItem).filter(KnowledgeItem.id == item_id).first()
        if item:
            if item.embedding_id:
                chroma_db.delete(ids=item.embedding_id.split(","))
            db.delete(item)
            db.commit()
            return True
        return False


knowledge_service = KnowledgeService()
