from services.vector_service import create_faiss_index


def test_create_faiss_index():
    embeddings = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6]
    ]

    index = create_faiss_index(embeddings)

    assert index.ntotal == 2