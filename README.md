# RAG Document Chatbot

An AI-powered document chatbot that lets users upload PDF/TXT files and ask questions about them. Built with Retrieval-Augmented Generation (RAG) architecture.

---

## Tech Stack

- **FastAPI** — Python web framework
- **PostgreSQL** — Relational database (document metadata)
- **SQLAlchemy** — ORM
- **ChromaDB** — Vector database for embeddings
- **Sentence Transformers** — Text embedding model (all-MiniLM-L6-v2)
- **Groq API** — LLM inference (Llama 3.3 70B)
- **PyPDF2** — PDF text extraction
- **JWT** — Authentication
- **Docker** — Containerization

---

## How It Works

```
Upload PDF → Extract Text → Chunk → Embed → Store in ChromaDB
                                                    ↓
User Question → Embed → Similarity Search → Top-K Chunks → Groq LLM → Answer
```

1. User uploads a PDF or TXT file
2. Text is extracted and split into ~500 character chunks
3. Each chunk is converted to a vector using Sentence Transformers
4. Vectors are stored in ChromaDB with the original text
5. When user asks a question, it is embedded using the same model
6. ChromaDB finds the most similar chunks (cosine similarity)
7. Top-K chunks + question are sent to Groq LLM
8. LLM answers using only the document context — no hallucination

---

## Features

- JWT authentication (signup, login)
- Upload PDF and TXT documents
- Ask questions about uploaded documents
- Returns answer + source chunks used
- Each user's documents are isolated
- No hallucination — answers strictly from document context

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and get access token |

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/documents/upload` | Upload a PDF or TXT file |
| GET | `/documents/` | List all uploaded documents |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat/` | Ask a question about a document |

---

## Local Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Groq API key (free at console.groq.com)

### Setup

```bash
git clone https://github.com/giddamansoorbasha/rag-document-chatbot.git
cd rag-document-chatbot

pip install -r requirements.txt
```

Create `.env` file:
```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/ragdb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_TIME=30
REFRESH_TOKEN_TIME=7
GROQ_API_KEY=your_groq_api_key
```

Run:
```bash
uvicorn app.main:app --reload
```

API runs at `http://localhost:8000/docs`

---

## Project Structure

```
app/
├── core/
│   ├── config.py         # Environment settings
│   ├── database.py       # DB connection
│   └── security.py       # JWT auth
├── models/
│   ├── user.py           # User ORM model
│   └── document.py       # Document ORM model
├── schemas/
│   ├── user.py           # User schemas
│   ├── document.py       # Document schemas
│   └── chat.py           # Chat request/response schemas
├── routers/
│   ├── auth.py           # Auth endpoints
│   ├── documents.py      # Upload + list endpoints
│   └── chat.py           # Chat endpoint
├── services/
│   ├── embedding.py      # Sentence Transformers
│   ├── vector_store.py   # ChromaDB operations
│   └── llm.py            # Groq LLM
└── main.py               # App entry point
```

---

## Author

**Gidda Mansoor Basha**
B.Tech CSE-AIML | Jain University, Bangalore
Backend Engineer | FastAPI · PostgreSQL · ChromaDB · Groq · Docker
