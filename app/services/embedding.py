from fastembed import TextEmbedding

model = TextEmbedding("BAAI/bge-small-en-v1.5")

def get_embeddings(texts: list[str]) -> list[list[float]]:
    return [emb.tolist() for emb in model.embed(texts)]