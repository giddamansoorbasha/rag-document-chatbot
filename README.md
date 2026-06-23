# RAG Document Chatbot API 🤖📄

A production-ready Retrieval-Augmented Generation (RAG) REST API that allows users to upload PDF/TXT documents and chat with them using AI.

Built with **FastAPI**, **PostgreSQL + pgvector**, and **Groq LLMs**.

## 🚀 Live Demo

 https://rag-chatbot-ui-phi.vercel.app/

---

# ✨ Features

* 🔐 JWT Authentication (Signup/Login)
* 📄 Upload PDF and TXT documents
* ✂️ Intelligent document chunking using RecursiveCharacterTextSplitter
* 🧠 Semantic search using vector embeddings
* 💬 Ask questions about uploaded documents
* 📚 Source chunk citations for transparency
* 👤 User-specific document isolation
* 🗑️ Delete uploaded documents
* ⚡ Fast LLM inference using Groq
* 📖 Interactive Swagger/OpenAPI documentation
* 🐳 Dockerized and production-ready

---

# 🏗️ Architecture

```text
Client (Swagger UI / React / Streamlit / Mobile App)
                            │
                            ▼
                    FastAPI REST API
                            │
          ┌─────────────────┴─────────────────┐
          ▼                                   ▼
 PostgreSQL + pgvector                 Groq LLM API
 (Users + Documents + Vectors)      (Llama 3.3 70B)
```

---

# 🛠️ Tech Stack

| Layer            | Technology                               |
| ---------------- | ---------------------------------------- |
| API Framework    | FastAPI                                  |
| Database         | PostgreSQL (Supabase)                    |
| Vector Search    | pgvector                                 |
| ORM              | SQLAlchemy                               |
| Authentication   | JWT + bcrypt                             |
| Embeddings       | FastEmbed + BAAI/bge-small-en-v1.5       |
| LLM              | Groq API (Llama 3.3 70B Versatile)       |
| Chunking         | LangChain RecursiveCharacterTextSplitter |
| API Docs         | Swagger/OpenAPI                          |
| Deployment       | Render                                   |
| Containerization | Docker                                   |

---

# 📂 Project Structure

```text
rag-document-chatbot/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── document.py
│   │   
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── documents.py
│   │   └── chat.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── document.py
│   │   └── chat.py
│   │
│   └── services/
│       ├── embedding.py
│       ├── vector_store.py
│       └── llm.py
│
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .env
```

---

# ⚙️ Local Setup

## Prerequisites

* Python 3.10+
* Docker + Docker Compose (optional)
* PostgreSQL / Supabase
* Groq API Key

---

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rag-document-chatbot.git

cd rag-document-chatbot
```

---

## 2. Create Virtual Environment

### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:password@host:5432/postgres

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_TIME=30

REFRESH_TOKEN_TIME=7

GROQ_API_KEY=your_groq_api_key
```

---

## 5. Enable pgvector

If using Supabase, execute:

```sql
create extension if not exists vector;
```

---

## 6. Run the API

```bash
uvicorn app.main:app --reload
```

API:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

# 🔐 API Endpoints

## Authentication

| Method | Endpoint       | Description                 |
| ------ | -------------- | --------------------------- |
| POST   | `/auth/signup` | Register a new user         |
| POST   | `/auth/login`  | Login and receive JWT token |

---

## Documents

| Method | Endpoint            | Description                       |
| ------ | ------------------- | --------------------------------- |
| POST   | `/documents/upload` | Upload a PDF/TXT document         |
| GET    | `/documents/`       | Get all documents of current user |
| DELETE | `/documents/{id}`   | Delete a document                 |

---

## Chat

| Method | Endpoint | Description                    |
| ------ | -------- | ------------------------------ |
| POST   | `/chat/` | Ask questions about a document |

---

# Example Chat Request

```json
{
    "document_id": 1,
    "question": "What are the main topics discussed in this document?"
}
```

---

# Example Response

```json
{
    "answer": "The document discusses ...",
    "sources": [
        "Chunk 1 text...",
        "Chunk 2 text...",
        "Chunk 3 text..."
    ]
}
```

---

# 🔄 How the RAG Pipeline Works

```text
User uploads PDF/TXT
            │
            ▼
Extract text
(PyPDF2 / plain text)
            │
            ▼
Split text into overlapping chunks
(RecursiveCharacterTextSplitter)
            │
            ▼
Generate embeddings
(BAAI/bge-small-en-v1.5)
            │
            ▼
Store chunks + vectors
(PostgreSQL + pgvector)
            │
            ▼
User asks a question
            │
            ▼
Generate query embedding
            │
            ▼
Cosine similarity search
(top relevant chunks)
            │
            ▼
Send retrieved chunks to Groq LLM
            │
            ▼
Generate answer grounded on document context
            │
            ▼
Return answer + source chunks
```

---

# 🐳 Docker

Run using Docker:

```bash
docker-compose up --build
```

---

# 🌍 Deployment

## Backend Deployment

The API is deployed on Render.

Deployment Steps:

1. Push code to GitHub.
2. Create a new Render Web Service.
3. Connect repository.
4. Select **Docker Runtime**.
5. Add environment variables.
6. Deploy.

---

# 📌 Environment Variables

| Variable           | Description                       |
| ------------------ | --------------------------------- |
| DATABASE_URL       | PostgreSQL connection string      |
| SECRET_KEY         | Secret key used for JWT           |
| ALGORITHM          | JWT algorithm (`HS256`)           |
| ACCESS_TOKEN_TIME  | Access token expiration (minutes) |
| REFRESH_TOKEN_TIME | Refresh token expiration (days)   |
| GROQ_API_KEY       | Groq API key                      |

---

# 🎯 Key Interview Concepts

## What is RAG?

Retrieval-Augmented Generation (RAG) combines information retrieval with Large Language Models to generate responses grounded in external knowledge instead of relying solely on the model's training data.

---

## Why pgvector?

pgvector enables efficient vector similarity search directly inside PostgreSQL, allowing relational and vector data to live in the same database.

---

## Why FastEmbed?

FastEmbed generates embeddings locally with low latency and zero API cost.

---

## Why BGE Embeddings?

`BAAI/bge-small-en-v1.5` provides strong semantic retrieval performance while remaining lightweight and efficient.

---

## Why Groq?

Groq provides extremely fast inference for open-source LLMs with a generous free tier, making it ideal for RAG applications and prototyping.

---

# 📄 License

MIT License
