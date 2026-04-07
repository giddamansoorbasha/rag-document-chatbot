from fastembed import TextEmbedding

model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings(texts: list[str]) -> list[list[float]]:
    return [emb.tolist() for emb in model.embed(texts)]