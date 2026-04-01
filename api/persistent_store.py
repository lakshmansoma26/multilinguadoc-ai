import json
import os
import uuid
import faiss

from api.db import get_connection

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

DOCUMENTS_DIR = os.path.join(PROJECT_ROOT, "storage", "documents")
INDEXES_DIR = os.path.join(PROJECT_ROOT, "storage", "indexes")
METADATA_DIR = os.path.join(PROJECT_ROOT, "storage", "metadata")

os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(INDEXES_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)


def create_document_id() -> str:
    return str(uuid.uuid4())


def save_uploaded_file(document_id: str, file_name: str, file_bytes: bytes) -> str:
    safe_name = f"{document_id}_{file_name}"
    file_path = os.path.join(DOCUMENTS_DIR, safe_name)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return file_path


def save_chunks_and_text(document_id: str, chunks: list[dict], full_text: str) -> tuple[str, str]:
    chunks_path = os.path.join(METADATA_DIR, f"{document_id}_chunks.json")
    full_text_path = os.path.join(METADATA_DIR, f"{document_id}_full_text.json")

    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    with open(full_text_path, "w", encoding="utf-8") as f:
        json.dump({"full_text": full_text}, f, ensure_ascii=False, indent=2)

    return chunks_path, full_text_path


def save_faiss_index(document_id: str, index) -> str:
    index_path = os.path.join(INDEXES_DIR, f"{document_id}.faiss")
    faiss.write_index(index, index_path)
    return index_path


def save_document_record(
    document_id: str,
    file_name: str,
    file_path: str,
    language_name: str,
    page_count: int,
    chunk_count: int,
    index_path: str,
    chunks_path: str,
    full_text_path: str
) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (
            document_id,
            file_name,
            file_path,
            language_name,
            page_count,
            chunk_count,
            index_path,
            chunks_path,
            full_text_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        document_id,
        file_name,
        file_path,
        language_name,
        page_count,
        chunk_count,
        index_path,
        chunks_path,
        full_text_path
    ))

    conn.commit()
    conn.close()


def load_document_record(document_id: str) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM documents WHERE document_id = ?",
        (document_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)


def load_chunks(chunks_path: str) -> list[dict]:
    with open(chunks_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_full_text(full_text_path: str) -> str:
    with open(full_text_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["full_text"]


def load_faiss_index(index_path: str):
    return faiss.read_index(index_path)