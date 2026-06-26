# Personal RAG System

A personal knowledge base system with conversational Q&A and semantic search capabilities.

## Features

- **Conversational Q&A**: Chat with your knowledge base using RAG (Retrieval-Augmented Generation)
- **Semantic Search**: Search knowledge by meaning, not just keywords
- **Knowledge Management**: CRUD operations for knowledge items
- **Multiple Formats**: Support for Markdown, code, and webpage content
- **Local Deployment**: All data stored locally

## Tech Stack

- **Backend**: FastAPI, LangChain, ChromaDB, SQLite
- **Frontend**: Next.js 14, React 18, TailwindCSS

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key (or other LLM provider)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker Setup

```bash
# Copy and configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Start services
docker-compose up -d
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Chat with knowledge base |
| GET | `/api/chat/history` | Get chat history |
| POST | `/api/search` | Semantic search |
| GET | `/api/knowledge` | List knowledge items |
| POST | `/api/knowledge` | Create knowledge item |
| GET | `/api/knowledge/{id}` | Get knowledge item |
| DELETE | `/api/knowledge/{id}` | Delete knowledge item |
| GET | `/api/models` | List available models |
| GET | `/api/stats` | Get system stats |

## Project Structure

```
rag-system/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Configuration
│   │   ├── db/          # Database connections
│   │   ├── models/      # Data models
│   │   └── services/    # Business logic
│   └── tests/           # Backend tests
├── frontend/            # Next.js frontend
│   └── src/
│       ├── app/         # Pages
│       ├── components/  # UI components
│       ├── hooks/       # Custom hooks
│       └── services/    # API client
├── data/                # Data storage
└── docs/                # Documentation
```

## License

MIT
