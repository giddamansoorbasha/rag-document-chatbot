from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers.auth import authroute
from app.routers.documents import docsroute
from app.routers.chat import chatroute
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG Document Chatbot")

app.add_middleware(
    CORSMiddleware,
    origins = [
    "http://localhost:3000",
    "https://rag-ui-phi-eight.vercel.app/"
    ], 
    allow_credentials=False,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(authroute)
app.include_router(docsroute)
app.include_router(chatroute)

@app.get("/")
def home():
    return {"message": "RAG Document Chatbot API"}