# RAG Document Chatbot

A production-ready REST API that lets users upload documents (PDF/TXT) and chat with them using AI. Built with FastAPI, pgvector, and Groq (LLaMA 3).

Live Link:  https://rag-document-chatbot-3jqq.onrender.com/docs 

---

## What it does

1. User signs up and logs in → gets a JWT token
2. User uploads a PDF or TXT file → app extracts text, splits into chunks, embeds them using `sentence-transformers`, and stores vectors in PostgreSQL via pgvector
3. User asks a question about the document → app finds the most semantically similar chunks via cosine similarity search
4. Those chunks are sent to Groq (LLaMA 3.3 70B) as context → AI answers based only on the document
5. User gets an answer with the source chunks that were used

---

## Tech stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| Database | PostgreSQL (Supabase) |
| Vector search | pgvector |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Groq API — LLaMA 3.3 70B |
| Auth | JWT (python-jose) + bcrypt |
| ORM | SQLAlchemy |
| Containerization | Docker + Docker Compose |

---

## Project structure

```
rag-document-chatbot/
├── app/
│   ├── core/
│   │   ├── config.py          # Pydantic settings from .env
│   │   ├── database.py        # SQLAlchemy engine + session
│   │   └── security.py        # JWT, password hashing, get_current_user
│   ├── models/
│   │   ├── user.py            # User table
│   │   └── document.py        # Document metadata table
│   ├── routers/
│   │   ├── auth.py            # POST /auth/signup, /auth/login
│   │   ├── documents.py       # POST /documents/upload, GET /documents/
│   │   └── chat.py            # POST /chat/
│   ├── schemas/
│   │   ├── user.py
│   │   ├── document.py
│   │   └── chat.py
│   └── services/
│       ├── embedding.py       # sentence-transformers wrapper
│       ├── llm.py             # Groq API wrapper
│       └── vector_store.py    # pgvector add/search/delete
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

---

## Local setup

### Prerequisites

- Docker + Docker Compose
- A [Groq API key](https://console.groq.com) (free)
- A [Supabase](https://supabase.com) project (free) — or local Postgres

### 1. Clone and configure

```bash
git clone https://github.com/yourusername/rag-document-chatbot.git
cd rag-document-chatbot
```

Create a `.env` file in the root:

```dotenv
DATABASE_URL=postgresql://postgres:yourpassword@db.xxxx.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_TIME=30
REFRESH_TOKEN_TIME=7
GROQ_API_KEY=your-groq-api-key
```

### 2. Enable pgvector (Supabase only — skip if using local Postgres)

In Supabase dashboard → SQL Editor:

```sql
create extension if not exists vector;
```

### 3. Run with Docker

```bash
docker-compose up --build
```

API is now running at `http://localhost:8000`

Interactive docs (Swagger UI): `http://localhost:8000/docs`

---

## API reference

### Auth

```
POST /auth/signup     Create a new user account
POST /auth/login      Login and receive a JWT access token
```

### Documents

```
POST /documents/upload    Upload a PDF or TXT file (auth required)
GET  /documents/          List all documents for the current user (auth required)
```

### Chat

```
POST /chat/    Ask a question about a document (auth required)
```

Example request body for `/chat/`:

```json
{
  "document_id": 1,
  "question": "What are the main findings of this document?"
}
```

Example response:

```json
{
  "question": "What are the main findings of this document?",
  "answer": "Based on the document, the main findings are...",
  "sources": [
    "chunk 1 text that was used...",
    "chunk 2 text that was used...",
    "chunk 3 text that was used..."
  ]
}
```

All protected endpoints require the header:

```
Authorization: Bearer <your_access_token>
```

---

## How the RAG pipeline works

```
PDF/TXT upload
     │
     ▼
Extract text (PyPDF2 / plain decode)
     │
     ▼
Split into 500-character word chunks
     │
     ▼
Embed each chunk → 384-dimensional vector (all-MiniLM-L6-v2)
     │
     ▼
Store chunks + vectors in PostgreSQL (pgvector)
     │
   (later, on chat request)
     │
     ▼
Embed the user's question → query vector
     │
     ▼
Cosine similarity search → top 3 most relevant chunks
     │
     ▼
Send chunks as context to Groq (LLaMA 3.3 70B)
     │
     ▼
Return AI answer + source chunks
```

---

## Deployment (Render)

### 1. Database — Supabase (free, no expiry)

Create a free project at [supabase.com](https://supabase.com), enable the `vector` extension, and copy the direct connection URL.

### 2. API — Render Web Service

1. Push your code to GitHub
2. Render dashboard → New → Web Service → connect your repo
3. Runtime: **Docker**
4. Port: `8000`
5. Add environment variables (same as your `.env` but pointing to Supabase)

That's it. No separate ChromaDB service needed — vectors live in the same Postgres database.

---

## Environment variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Secret used to sign JWT tokens |
| `ALGORITHM` | JWT algorithm (use `HS256`) |
| `ACCESS_TOKEN_TIME` | Access token expiry in minutes |
| `REFRESH_TOKEN_TIME` | Refresh token expiry in days |
| `GROQ_API_KEY` | API key from console.groq.com |

---

## Key concepts for interviews

**What is RAG?** Retrieval Augmented Generation — instead of relying on the LLM's training data, you retrieve relevant context from your own documents and feed it to the model at inference time. The model answers only from that context.

**Why pgvector instead of ChromaDB?** pgvector adds vector similarity search directly to PostgreSQL. One database handles both relational data (users, documents) and vector search — simpler infrastructure, no extra service to maintain.

**Why sentence-transformers?** `all-MiniLM-L6-v2` runs locally (no API cost), produces 384-dimensional embeddings, and is fast enough for a document chatbot. Good balance of speed and quality.

**Why Groq?** Groq provides extremely fast LLM inference (LLaMA 3.3 70B) with a generous free tier — ideal for projects and demos.

---

## License

MIT
