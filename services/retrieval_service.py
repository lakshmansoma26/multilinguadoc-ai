import numpy as np
from core.constants import TOP_K_RESULTS
from services.embedding_service import get_text_embedding


def retrieve_relevant_chunks(
    question: str,
    index,
    chunks: list[dict],
    top_k: int = TOP_K_RESULTS
) -> list[dict]:
    """
    Retrieve the most relevant chunks for a question,
    keeping similarity distances for debugging.
    """
    question_embedding = get_text_embedding(question)
    query_vector = np.array([question_embedding]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        if 0 <= idx < len(chunks):
            chunk = chunks[idx].copy()
            chunk["distance"] = float(distances[0][rank])
            results.append(chunk)

    return results