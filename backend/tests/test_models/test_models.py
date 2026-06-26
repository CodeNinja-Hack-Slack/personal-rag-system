import pytest
from app.models.knowledge import KnowledgeItem
from app.models.conversation import Conversation


def test_knowledge_item_fields():
    fields = KnowledgeItem.__table__.columns.keys()
    assert "id" in fields
    assert "title" in fields
    assert "content" in fields
    assert "content_type" in fields
    assert "source" in fields
    assert "language" in fields
    assert "tags" in fields
    assert "category" in fields
    assert "embedding_id" in fields
    assert "created_at" in fields
    assert "updated_at" in fields
    assert "version" in fields


def test_conversation_fields():
    fields = Conversation.__table__.columns.keys()
    assert "id" in fields
    assert "question" in fields
    assert "answer" in fields
    assert "context_ids" in fields
    assert "model_used" in fields
    assert "created_at" in fields


def test_knowledge_item_table_name():
    assert KnowledgeItem.__tablename__ == "knowledge_items"


def test_conversation_table_name():
    assert Conversation.__tablename__ == "conversations"
