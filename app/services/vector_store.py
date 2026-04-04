import chromadb
from app.services.embedding import get_embeddings

client = chromadb.PersistentClient(path="./chroma_db")

def create_collection(collection_name: str):
    return client.get_or_create_collection(collection_name)

def add_chunks(collection_name: str, chunks: list[str], ids: list[str]):
    collection = create_collection(collection_name)
    embeddings = get_embeddings(chunks)
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

def search_chunks(collection_name: str, query: str, n_results: int = 3) -> list[str]:
    collection = create_collection(collection_name)
    query_embedding = get_embeddings([query])
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results["documents"][0]