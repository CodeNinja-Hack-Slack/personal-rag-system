import pytest
from app.services.knowledge import knowledge_service
from app.db.sqlite import SessionLocal


@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()


def test_create_knowledge_item(db):
    item = knowledge_service.create(
        db=db,
        title="Test Knowledge",
        content="This is a test content for knowledge base.",
        content_type="manual",
        language="en"
    )
    assert item.id is not None
    assert item.title == "Test Knowledge"
    assert item.content_type == "manual"
    assert item.language == "en"


def test_list_knowledge_items(db):
    items = knowledge_service.list(db=db)
    assert isinstance(items, list)


def test_get_knowledge_item(db):
    item = knowledge_service.create(
        db=db,
        title="Get Test",
        content="Content for get test.",
        content_type="manual"
    )
    retrieved = knowledge_service.get(db=db, item_id=item.id)
    assert retrieved is not None
    assert retrieved.title == "Get Test"


def test_delete_knowledge_item(db):
    item = knowledge_service.create(
        db=db,
        title="Delete Test",
        content="Content for delete test.",
        content_type="manual"
    )
    result = knowledge_service.delete(db=db, item_id=item.id)
    assert result is True
    assert knowledge_service.get(db=db, item_id=item.id) is None
