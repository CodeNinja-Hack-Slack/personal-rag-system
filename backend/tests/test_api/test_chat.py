import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Personal RAG System API"}


def test_get_models():
    response = client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert isinstance(data["models"], list)


def test_get_stats():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


def test_create_knowledge():
    response = client.post("/api/knowledge", json={
        "title": "Test Knowledge",
        "content": "This is test content for the knowledge base.",
        "content_type": "manual",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Knowledge"
    assert "id" in data
    return data["id"]


def test_list_knowledge():
    response = client.get("/api/knowledge")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_chat_endpoint():
    response = client.post("/api/chat", json={
        "question": "What is this system about?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "context" in data
    assert "model_used" in data
