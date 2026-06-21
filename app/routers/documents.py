from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.vector_store import add_chunks, delete_chunks
from app.services.vector_store import add_chunks
import uuid
import PyPDF2
import io
from langchain_text_splitters import RecursiveCharacterTextSplitter

docsroute = APIRouter(prefix="/documents", tags=["Documents"])

def extract_text(file: UploadFile) -> str:
    content = file.file.read()

    if file.filename.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(io.BytesIO(content))

        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n\n"

        return text

    return content.decode("utf-8")

def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )
    chunks = splitter.split_text(text)

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

    doc = Document(
        user_id=user.id,
        filename=file.filename,
        collection_name=collection_name
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)  

    # Now pass user_id and doc_id
    chunk_ids = [f"{collection_name}_chunk_{i}" for i in range(len(chunks))]
    add_chunks(collection_name, chunks, chunk_ids, user_id=user.id, doc_id=doc.id)

    return doc

@docsroute.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Document).filter(Document.user_id == user.id).all()

@docsroute.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    doc = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == user.id 
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    delete_chunks(doc.collection_name)  
    db.delete(doc)                      
    db.commit()

    return {"message": f"Document '{doc.filename}' deleted successfully"}