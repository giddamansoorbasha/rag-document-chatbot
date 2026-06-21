from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from app.core.database import Base, engine, SessionLocal
from app.services.embedding import get_embeddings

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id               = Column(Integer, primary_key=True, index=True)
    collection_name  = Column(String, nullable=False, index=True)
    content          = Column(Text, nullable=False)
    embedding        = Column(Vector(384))          

    user_id   = Column(Integer, ForeignKey("users.id"), nullable=True)
    doc_id    = Column(Integer, ForeignKey("documents.id"), nullable=True)


Base.metadata.create_all(bind=engine)

def add_chunks(collection_name: str, chunks: list[str], ids: list[str], user_id: int = None, doc_id: int = None):
    """Embed chunks and store them in PostgreSQL."""
    embeddings = get_embeddings(chunks)         
    db = SessionLocal()
    try:
        for content, embedding in zip(chunks, embeddings):
            chunk = DocumentChunk(
                collection_name=collection_name,
                content=content,
                embedding=embedding,
                user_id=user_id,   
                doc_id=doc_id
            )
            db.add(chunk)
        db.commit()
    finally:
        db.close()


def search_chunks(collection_name: str, query: str, n_results: int = 3) -> list[str]:
    """Return the top-n most similar chunks for a query."""
    query_embedding = get_embeddings([query])[0]
    db = SessionLocal()
    try:
        results = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.collection_name == collection_name)
            .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
            .limit(n_results)
            .all()
        )
        return [r.content for r in results]
    finally:
        db.close()


def delete_chunks(collection_name: str):
    """Delete all chunks for a document (useful if you add a delete doc endpoint)."""
    db = SessionLocal()
    try:
        db.query(DocumentChunk).filter(
            DocumentChunk.collection_name == collection_name
        ).delete()
        db.commit()
    finally:
        db.close()