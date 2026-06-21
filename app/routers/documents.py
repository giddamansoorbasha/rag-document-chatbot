from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.vector_store import add_chunks
import uuid
import PyPDF2
import io

docsroute = APIRouter(prefix="/documents", tags=["Documents"])

def extract_text(file: UploadFile) -> str:
    content = file.file.read()
    if file.filename.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(io.BytesIO(content))
        return " ".join(page.extract_text() for page in pdf.pages)
    return content.decode("utf-8")

def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    current = []
    count = 0
    for word in words:
        current.append(word)
        count += len(word) + 1
        if count >= chunk_size:
            chunks.append(" ".join(current))
            current = []
            count = 0
    if current:
        chunks.append(" ".join(current))
    return chunks

@docsroute.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT allowed")

    text = extract_text(file)
    chunks = chunk_text(text)
    collection_name = f"doc_{uuid.uuid4().hex}"

    # Create doc FIRST to get doc.id
    doc = Document(
        user_id=user.id,
        filename=file.filename,
        collection_name=collection_name
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)  # now doc.id exists

    # Now pass user_id and doc_id
    chunk_ids = [f"{collection_name}_chunk_{i}" for i in range(len(chunks))]
    add_chunks(collection_name, chunks, chunk_ids, user_id=user.id, doc_id=doc.id)

    return doc

@docsroute.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Document).filter(Document.user_id == user.id).all()