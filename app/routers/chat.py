from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.vector_store import search_chunks
from app.services.llm import get_answer

chatroute = APIRouter(prefix="/chat", tags=["Chat"])

@chatroute.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    doc = db.query(Document).filter(
        Document.id == request.document_id,
        Document.user_id == user.id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    chunks = search_chunks(doc.collection_name, request.question)
    answer = get_answer(request.question, chunks)

    return ChatResponse(
        question=request.question,
        answer=answer,
        sources=chunks
    )