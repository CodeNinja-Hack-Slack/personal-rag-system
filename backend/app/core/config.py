from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # LLM Provider: openai / mimo / ollama
    llm_provider: str = "mimo"

    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_base_url: str = "https://api.openai.com/v1"

    # Mimo Configuration (Xiaomi AI)
    mimo_api_key: str = ""
    mimo_model: str = "mimo-v2.5-pro"
    mimo_base_url: str = "https://api.mimo.ai/v1"

    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"

    # Claude Configuration
    claude_api_key: str = ""

    # Embedding Configuration
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    
    # Vector Database
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection_name: str = "knowledge_base"
    
    # Service Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000"
    
    # Knowledge Base Configuration
    max_chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
