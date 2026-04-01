import os
import sys

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from api.db import init_db
from api.schemas import AskRequest, SummaryRequest, StudyRequest
from api.persistent_store import (
    create_document_id,
    save_uploaded_file,
    save_chunks_and_text,
    save_faiss_index,
    save_document_record,
    load_document_record,
    load_chunks,
    load_full_text,
    load_faiss_index
)

from services.pdf_service import extract_text_from_pdf, combine_pages_to_text
from services.language_service import detect_language
from services.chunk_service import chunk_text
from services.embedding_service import get_text_embedding
from services.vector_service import create_faiss_index
from services.qa_service import answer_question
from services.summary_service import generate_summary
from services.study_service import generate_study_material

app = FastAPI(
    title="Multi Lingual Doc AI API",
    description="Backend API for multilingual document intelligence",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "LinguaDoc API root working."}


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        file_bytes = await file.read()
        document_id = create_document_id()

        file_path = save_uploaded_file(document_id, file.filename, file_bytes)

        pages = extract_text_from_pdf(file_path)
        full_text = combine_pages_to_text(pages)
        language_info = detect_language(full_text[:2000])
        chunks = chunk_text(pages)

        embeddings = [get_text_embedding(chunk["text"]) for chunk in chunks]
        index = create_faiss_index(embeddings)

        chunks_path, full_text_path = save_chunks_and_text(document_id, chunks, full_text)
        index_path = save_faiss_index(document_id, index)

        save_document_record(
            document_id=document_id,
            file_name=file.filename,
            file_path=file_path,
            language_name=language_info["language_name"],
            page_count=len(pages),
            chunk_count=len(chunks),
            index_path=index_path,
            chunks_path=chunks_path,
            full_text_path=full_text_path
        )

        return {
            "document_id": document_id,
            "file_name": file.filename,
            "pages": len(pages),
            "chunks": len(chunks),
            "detected_language": language_info["language_name"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")


@app.post("/ask")
def ask_question_endpoint(request: AskRequest):
    document = load_document_record(request.document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        chunks = load_chunks(document["chunks_path"])
        full_text = load_full_text(document["full_text_path"])
        index = load_faiss_index(document["index_path"])

        result = answer_question(
            question=request.question,
            index=index,
            chunks=chunks,
            output_language=request.output_language,
            full_text=full_text
        )

        return {
            "answer": result["answer"],
            "source_pages": result["source_pages"],
            "source_chunks": result["source_chunks"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question answering failed: {str(e)}")


@app.post("/summary")
def summarize_document(request: SummaryRequest):
    document = load_document_record(request.document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        full_text = load_full_text(document["full_text_path"])

        summary = generate_summary(
            document_text=full_text,
            output_language=request.output_language,
            summary_type=request.summary_type
        )

        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")


@app.post("/study")
def generate_study(request: StudyRequest):
    document = load_document_record(request.document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        full_text = load_full_text(document["full_text_path"])

        study_material = generate_study_material(
            document_text=full_text,
            output_language=request.output_language
        )

        return {"study_material": study_material}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Study material generation failed: {str(e)}")