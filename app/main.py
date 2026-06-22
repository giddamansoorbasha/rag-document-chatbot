from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers.auth import authroute
from app.routers.documents import docsroute
from app.routers.chat import chatroute

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG Document Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://rag-chatbot-ui-phi.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authroute)
app.include_router(docsroute)
app.include_router(chatroute)

@app.get("/")
def home():
    return {"message": "RAG Document Chatbot API"}