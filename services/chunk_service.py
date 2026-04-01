from core.constants import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(
    pages_data: list[dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> list[dict]:
    """
    Split extracted text into cleaner paragraph-aware chunks.

    Strategy:
    - first split page text into paragraph-like blocks
    - then merge blocks up to chunk_size
    - preserve page metadata
    """

    chunks = []
    chunk_id = 1

    for page_data in pages_data:
        page_number = page_data["page"]
        text = page_data["text"].strip()

        if not text:
            continue

        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) + 1 <= chunk_size:
                current_chunk += (" " if current_chunk else "") + para
            else:
                if current_chunk.strip():
                    chunks.append(
                        {
                            "chunk_id": f"chunk_{chunk_id}",
                            "page": page_number,
                            "text": current_chunk.strip()
                        }
                    )
                    chunk_id += 1

                if len(para) > chunk_size:
                    start = 0
                    while start < len(para):
                        end = start + chunk_size
                        sub_chunk = para[start:end].strip()
                        if sub_chunk:
                            chunks.append(
                                {
                                    "chunk_id": f"chunk_{chunk_id}",
                                    "page": page_number,
                                    "text": sub_chunk
                                }
                            )
                            chunk_id += 1
                        start += chunk_size - overlap
                    current_chunk = ""
                else:
                    current_chunk = para

        if current_chunk.strip():
            chunks.append(
                {
                    "chunk_id": f"chunk_{chunk_id}",
                    "page": page_number,
                    "text": current_chunk.strip()
                }
            )
            chunk_id += 1

    return chunks