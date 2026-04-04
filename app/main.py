from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers.auth import authroute
from app.routers.documents import docsroute
from app.routers.chat import chatroute

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG Document Chatbot")

app.include_router(authroute)
app.include_router(docsroute)
app.include_router(chatroute)

@app.get("/")
def home():
    return {"message": "RAG Document Chatbot API"}