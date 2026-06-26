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
    
    def update(self, db: Session, item_id: str, **kwargs) -> Optional[KnowledgeItem]:
        item = db.query(KnowledgeItem).filter(KnowledgeItem.id == item_id).first()
        if not item:
            return None
        
        content_changed = "content" in kwargs and kwargs["content"] != item.content
        
        for key, value in kwargs.items():
            if value is not None and hasattr(item, key):
                setattr(item, key, value)
        
        if content_changed and item.embedding_id:
            chroma_db.delete(ids=item.embedding_id.split(","))
            
            content = kwargs.get("content", item.content)
            content_type = kwargs.get("content_type", item.content_type)
            title = kwargs.get("title", item.title)
            language = kwargs.get("language", item.language)
            
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
            
            item.embedding_id = ",".join(embedding_ids)
        
        item.version += 1
        db.commit()
        db.refresh(item)
        return item
    
    def delete(self, db: Session, item_id: str) -> bool:
        item = db.query(KnowledgeItem).filter(KnowledgeItem.id == item_id).first()
        if item:
            if item.embedding_id:
                chroma_db.delete(ids=item.embedding_id.split(","))
            db.delete(item)
            db.commit()
            return True
        return False
    
    def search(self, db: Session, query: str, top_k: int = 5) -> List[dict]:
        results = chroma_db.query(query_text=query, n_results=top_k)
        documents = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                documents.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None
                })
        return documents
    
    def export_all(self, db: Session) -> List[dict]:
        items = db.query(KnowledgeItem).all()
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "content_type": item.content_type,
                "source": item.source,
                "language": item.language,
                "tags": item.tags,
                "category": item.category,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "version": item.version
            }
            for item in items
        ]
    
    def import_batch(self, db: Session, items: List[dict]) -> List[KnowledgeItem]:
        created = []
        for item_data in items:
            item = self.create(
                db=db,
                title=item_data.get("title", "Untitled"),
                content=item_data.get("content", ""),
                content_type=item_data.get("content_type", "manual"),
                source=item_data.get("source"),
                language=item_data.get("language", "zh"),
                tags=item_data.get("tags"),
                category=item_data.get("category")
            )
            created.append(item)
        return created


knowledge_service = KnowledgeService()
