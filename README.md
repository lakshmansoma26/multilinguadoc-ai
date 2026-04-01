# Multi LingualDoc AI

## Multilingual Document Intelligence Platform

Multi Lingual Doc AI is a Python-based end-to-end AI system for building knowledge from PDF documents and enabling intelligent interactions via natural language and multilingual support.

### Main functionalities
- PDF ingest + extraction
- Language detection
- Chunk-based semantic indexing with FAISS
- Vector embeddings via OpenAI `text-embedding-3-small`
- Retrieval-augmented question answering
- Document summarization (short, bullet, detailed)
- Study material generation (Q&A, MCQs, flashcards)
- Persistent storage: SQLite + disk for files, indexes, metadata
- REST API + OpenAPI docs
- Streamlit frontend for interactively testing features

---

## NLP components and techniques
This project uses the following NLP-based elements:
- `langdetect` for language identification from extracted text (`services/language_service.py`)
- Paragraph-aware text chunking and overlap strategy for semantic coherence (`services/chunk_service.py`)
- Embedding generation for semantic representation with `text-embedding-3-small` (`services/embedding_service.py`)
- FAISS similarity search in semantic vector space for retrieval (`services/vector_service.py`, `services/retrieval_service.py`)
- Prompt-based generation for QA, summarization, and educational content using OpenAI (`services/llm_service.py`, `services/summary_service.py`, `services/study_service.py`)
- Multi-step development: extract ➜ pre-process ➜ embed ➜ retrieve ➜ generate answers, summaries and study materials.


---

## Repository structure

- `api/`
  - `main.py`: FastAPI server and routes (`/health`, `/upload`, `/ask`, `/summary`, `/study`)
  - `db.py`: SQLite DB initialization and connection
  - `persistent_store.py`: file/index metadata save/load
  - `schemas.py`: endpoint request models
- `services/`
  - `pdf_service.py`: PDF text extraction with `pdfplumber`
  - `language_service.py`: language detection with `langdetect`
  - `chunk_service.py`: text chunking with overlap
  - `embedding_service.py`: OpenAI embedding creation
  - `vector_service.py`: FAISS index create
  - `retrieval_service.py`: k-NN retrieval of relevant chunks
  - `llm_service.py`: OpenAI completion prompt for QA
  - `qa_service.py`: end-to-end question answering pipeline
  - `summary_service.py`: summary generation LLM prompt
  - `study_service.py`: study material LLM prompt
- `core/`
  - `config.py`: loads `.env` and `OPENAI_API_KEY`
  - `constants.py`: default params and supported languages
- `storage/`
  - `documents/`: uploaded PDFs
  - `indexes/`: FAISS `.faiss` files
  - `metadata/`: JSON chunks and full text
- `tests/`: unit tests for service modules

---

## Features in detail

1. **Upload + preprocess** (`POST /upload`)
   - accepts only PDF
   - stores PDF under `storage/documents`
   - extracts page text with `pdfplumber`
   - combines page text into full document
   - detects language using `langdetect`
   - chunks text (`800` tokens default, `100` overlap)
   - embeddings via OpenAI; FAISS index built
   - stores chunks + full text JSON + index file
   - stores metadata record in SQLite

2. **Question Answering** (`POST /ask`)
   - loads document by `document_id`
   - loads chunks, full text, FAISS index
   - performs semantic search with OpenAI query embeddings
   - selects top 3 chunks (configurable `TOP_K_RESULTS`)
   - builds prompt with broad context + retrieved evidence
   - generates answer via OpenAI `gpt-4o-mini`

3. **Summarization** (`POST /summary`)
   - input: `document_id`, `output_language`, `summary_type` (`short`, `bullet`, `detailed`)
   - returns LLM summary

4. **Study material** (`POST /study`)
   - generates:
     - 5 short-answer Q&A
     - 5 MCQs with choices + correct answer
     - 5 flashcards
   - returns LLM result string

5. **Health check** (`GET /health`)
   - verifies service up with `{status: "ok"}`

---

## API schema examples

### upload

`POST /upload` (form-data): `file` (PDF)

Response example:
```json
{
  "document_id": "uuid",
  "file_name": "mydoc.pdf",
  "pages": 8,
  "chunks": 30,
  "detected_language": "English"
}
```

### ask

`POST /ask`
```json
{
  "document_id": "<uuid>",
  "question": "What are the main points?",
  "output_language": "English"
}
```

### summary

`POST /summary`
```json
{
  "document_id": "<uuid>",
  "output_language": "English",
  "summary_type": "bullet"
}
```

### study

`POST /study`
```json
{
  "document_id": "<uuid>",
  "output_language": "English"
}
```

---

## Setup

1. clone repository
2. create venv: `python -m venv venv`
3. activate and install: `venv\\Scripts\\activate` + `pip install -r requirements.txt`
4. copy `.env`:
   - `OPENAI_API_KEY=YOUR_OWN_API_KEY`
5. start backend server (terminal 1):
   - `uvicorn api.main:app --reload --host 0.0.0.0 --port 8000`
6. start Streamlit frontend (terminal 2):
   - `streamlit run app/streamlit_app.py`
7. backend API docs: `http://127.0.0.1:8000/docs`
8. frontend UI: `http://localhost:8501`
9. run tests: `pytest -q`

### Troubleshooting setup
- **Backend won't start**: Ensure `OPENAI_API_KEY` is set in `.env`
- **Streamlit won't connect**: Check backend is running on `http://127.0.0.1:8000`
- **Import errors**: Run `pip install --upgrade -r requirements.txt`
- **FAISS errors on Windows**: Use `faiss-cpu` (included in requirements.txt)

---

## Dependencies

Core required packages (in `requirements.txt`):
- `fastapi==0.104.1` + `uvicorn==0.24.0` - REST API server
- `openai==1.3.3` - embedding + LLM calls
- `faiss-cpu==1.7.4` - vector search indexing
- `pdfplumber==0.10.3` - PDF text extraction
- `langdetect==1.0.9` - language detection
- `streamlit==1.33.0` - frontend interface
- `python-dotenv==1.0.0` - environment variable loading
- `requests==2.31.0` - HTTP client for API calls
- `pytest==7.4.3` - testing framework
- `numpy==1.24.3` - numerical computations
- `pydantic==2.5.0` - data validation (FastAPI)

Install all with: `pip install -r requirements.txt`

---

## Config

`core/constants.py`:
- `CHUNK_SIZE=800`
- `CHUNK_OVERLAP=100`
- `TOP_K_RESULTS=3`
- `SUPPORTED_LANGUAGES`: en, es, hi, fr, zh-cn, zh-tw

`core/config.py`:
- `OPENAI_API_KEY` from `.env`

---

## Storage

- `storage/documents`: uploaded docs
- `storage/indexes`: FAISS indexes
- `storage/metadata`: chunks + full text
- `storage/linguadoc.db`: document metadata

---

## Testing

Current unit tests:
- `tests/test_chunk_service.py`
- `tests/test_vector_service.py`

Add tests recommended:
- endpoint tests with `TestClient`
- mocking OpenAI API calls

---


### How users run the project safely

- clone repo
- install deps (`pip install -r requirements.txt`)
- create `.env` manually with users OpenAI key
- start backend and Streamlit UI

The code uses `os.getenv("OPENAI_API_KEY")` so no key is stored in source.

- endpoint tests with `TestClient`
- OpenAI client mocking

---


---

## Streamlit frontend

### Launch
1. Start backend API first (terminal 1):
   - `uvicorn api.main:app --reload --host 0.0.0.0 --port 8000`
2. Run Streamlit app in new terminal (terminal 2):
   - `streamlit run app/streamlit_app.py`
3. Open in browser: `http://localhost:8501`
4. Backend health status shown in sidebar

### Features
- **PDF Upload**: sidebar file picker, automatic processing
- **Chat Interface**: ask questions above input box, responses display in scrollable container
- **Evidence Retrieval**: view source pages + chunks with similarity scores
- **Summarization**: multiple types (short, bullet, detailed)
- **Study Material**: auto-generated Q&A, MCQs, flashcards
- **Download**: export summaries and study materials as `.txt` files
- **Session State**: persistent chat history within session



---

## Notes

- Backend API: FastAPI with CORS enabled for cross-origin requests
- Frontend client wrapper: `app/api_client.py` handles all HTTP calls to backend
- Database: SQLite3 (built-in)
- External costs: OpenAI embeddings + chat completions per request
- Session management: Streamlit session state persists across reruns during session
- FAISS indexes: L2 distance metric for semantic similarity

---



---

## Quick curl examples

Upload:
```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@/path/to/doc.pdf"
```

Ask:
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" \
  -d '{"document_id":"<uuid>","question":"What is this document about?","output_language":"English"}'
```

Summary:
```bash
curl -X POST "http://127.0.0.1:8000/summary" -H "Content-Type: application/json" \
  -d '{"document_id":"<uuid>","output_language":"English","summary_type":"short"}'
```

Study:
```bash
curl -X POST "http://127.0.0.1:8000/study" -H "Content-Type: application/json" \
  -d '{"document_id":"<uuid>","output_language":"English"}'
```


