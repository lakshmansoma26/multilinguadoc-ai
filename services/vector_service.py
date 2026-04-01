import faiss
import numpy as np


def create_faiss_index(embeddings: list[list[float]]):
    if not embeddings:
        raise ValueError("Embeddings list is empty.")

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)

    embedding_matrix = np.array(embeddings).astype("float32")
    index.add(embedding_matrix)

    return index