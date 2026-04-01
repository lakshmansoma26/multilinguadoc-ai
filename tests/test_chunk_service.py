from services.chunk_service import chunk_text


def test_chunk_text():
    pages_data = [
        {"page": 1, "text": "A" * 1000}
    ]

    chunks = chunk_text(pages_data, chunk_size=300, overlap=50)

    assert len(chunks) > 1
    assert chunks[0]["page"] == 1
    assert "chunk_id" in chunks[0]
    assert "text" in chunks[0]