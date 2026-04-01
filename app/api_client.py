import requests

API_BASE_URL = "https://multilingualdoc-ai.onrender.com"


def upload_document(file_bytes: bytes, file_name: str) -> dict:
    files = {
        "file": (file_name, file_bytes, "application/pdf")
    }

    response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=300)
    response.raise_for_status()
    return response.json()


def ask_question(document_id: str, question: str, output_language: str) -> dict:
    payload = {
        "document_id": document_id,
        "question": question,
        "output_language": output_language
    }

    response = requests.post(f"{API_BASE_URL}/ask", json=payload, timeout=300)
    response.raise_for_status()
    return response.json()


def generate_summary(document_id: str, summary_type: str, output_language: str) -> dict:
    payload = {
        "document_id": document_id,
        "summary_type": summary_type,
        "output_language": output_language
    }

    response = requests.post(f"{API_BASE_URL}/summary", json=payload, timeout=300)
    response.raise_for_status()
    return response.json()


def generate_study_material(document_id: str, output_language: str) -> dict:
    payload = {
        "document_id": document_id,
        "output_language": output_language
    }

    response = requests.post(f"{API_BASE_URL}/study", json=payload, timeout=300)
    response.raise_for_status()
    return response.json()


def health_check() -> dict:
    response = requests.get(f"{API_BASE_URL}/health", timeout=30)
    response.raise_for_status()
    return response.json()