import os
import sys
import streamlit as st
import requests

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.api_client import (
    upload_document,
    ask_question,
    generate_summary,
    generate_study_material,
    health_check
)

st.set_page_config(
    page_title="Multi Lingual Doc AI",
    page_icon="📘",
    layout="wide"
)

if "document_id" not in st.session_state:
    st.session_state["document_id"] = None

if "file_name" not in st.session_state:
    st.session_state["file_name"] = None

if "pages" not in st.session_state:
    st.session_state["pages"] = None

if "chunks" not in st.session_state:
    st.session_state["chunks"] = None

if "detected_language" not in st.session_state:
    st.session_state["detected_language"] = None

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "summary_output" not in st.session_state:
    st.session_state["summary_output"] = ""

if "study_output" not in st.session_state:
    st.session_state["study_output"] = ""

if "last_uploaded_name" not in st.session_state:
    st.session_state["last_uploaded_name"] = None


st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    .hero-box {
        padding: 1.8rem 1.8rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
        color: white;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.93;
        line-height: 1.6;
        max-width: 900px;
    }

    .metric-card {
        padding: 1rem 1rem;
        border-radius: 18px;
        border: 1px solid rgba(120,120,120,0.15);
        background: rgba(250,250,250,0.03);
        text-align: center;
        min-height: 110px;
    }

    .metric-label {
        font-size: 0.85rem;
        opacity: 0.72;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        font-size: 1.45rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .panel {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        border: 1px solid rgba(120,120,120,0.15);
        background: rgba(250,250,250,0.03);
        margin-bottom: 1rem;
    }

    .panel-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    .workflow-card {
        padding: 0.9rem 1rem;
        border-radius: 16px;
        border: 1px solid rgba(120,120,120,0.15);
        background: rgba(250,250,250,0.03);
        min-height: 105px;
    }

    .workflow-step {
        font-size: 0.8rem;
        font-weight: 700;
        color: #2563eb;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .workflow-title {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .workflow-desc {
        font-size: 0.9rem;
        opacity: 0.8;
        line-height: 1.45;
    }

    .status-good {
        padding: 0.7rem 0.9rem;
        border-radius: 12px;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.2);
        color: #166534;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    .status-bad {
        padding: 0.7rem 0.9rem;
        border-radius: 12px;
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.2);
        color: #991b1b;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    .footer-box {
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid rgba(120,120,120,0.2);
        font-size: 0.9rem;
        opacity: 0.75;
        text-align: center;
    }

    .stButton button, .stDownloadButton button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 2.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

backend_ok = False
backend_message = "Backend not reachable"

try:
    backend_status = health_check()
    backend_ok = backend_status.get("status") == "ok"
    backend_message = backend_status.get("message", "Backend connected")
except Exception:
    backend_ok = False
    backend_message = "FastAPI backend is offline"

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">📘 Multi Lingual Doc AI</div>
        <div class="hero-subtitle">
            A multilingual document intelligence platform for question answering, summarization,
            and AI-generated study material. Upload a PDF, understand it faster, and transform it into usable knowledge.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("## ⚙️ Control Center")

    if backend_ok:
        st.markdown(
            f"<div class='status-good'>● {backend_message}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='status-bad'>● {backend_message}</div>",
            unsafe_allow_html=True
        )

    output_language = st.selectbox(
        "Output Language",
        ["English", "Spanish", "Hindi", "French", "Chinese"]
    )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if st.button("Reset Chat History", use_container_width=True):
        st.session_state["chat_history"] = []
        st.success("Chat history cleared.")

    st.markdown("---")

    st.markdown("### Workflow")
    st.markdown(
        """
        1. Upload a PDF  
        2. Ask questions  
        3. Generate summary  
        4. Create study material  
        """
    )

    st.markdown("---")

    st.markdown("### Product Snapshot")
    st.info(
        """
        **LinguaDoc AI** supports:
        - PDF upload and processing
        - Multilingual answers
        - Document summarization
        - AI-generated study content
        """
    )

if not backend_ok:
    st.warning("Start FastAPI first with: uvicorn api.main:app --reload")
    st.stop()

if uploaded_file is not None:
    if uploaded_file.name != st.session_state["last_uploaded_name"]:
        with st.spinner("Uploading and processing document..."):
            try:
                file_bytes = uploaded_file.read()
                result = upload_document(file_bytes, uploaded_file.name)

                st.session_state["document_id"] = result["document_id"]
                st.session_state["file_name"] = result["file_name"]
                st.session_state["pages"] = result["pages"]
                st.session_state["chunks"] = result["chunks"]
                st.session_state["detected_language"] = result["detected_language"]
                st.session_state["chat_history"] = []
                st.session_state["summary_output"] = ""
                st.session_state["study_output"] = ""
                st.session_state["last_uploaded_name"] = uploaded_file.name

            except Exception as e:
                st.error(f"Upload failed: {e}")

if st.session_state["document_id"] is not None:
    st.success(f"Loaded document: {st.session_state['file_name']}")

    metric1, metric2 = st.columns(2)

    with metric1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Pages</div>
                <div class="metric-value">{st.session_state["pages"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with metric2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Detected Language</div>
                <div class="metric-value">{st.session_state["detected_language"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Guided Workflow")

    wf1, wf2, wf3 = st.columns(3)

    with wf1:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-step">Step 1</div>
                <div class="workflow-title">Inspect Document</div>
                <div class="workflow-desc">
                    Review the uploaded file metadata and detected language before generating outputs.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with wf2:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-step">Step 2</div>
                <div class="workflow-title">Ask Smart Questions</div>
                <div class="workflow-desc">
                    Query the document using semantic retrieval and source-grounded answers.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with wf3:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-step">Step 3</div>
                <div class="workflow-title">Generate Outputs</div>
                <div class="workflow-desc">
                    Create summaries and study material in your selected language.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>Document Overview</div>", unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.text_area(
            "Preview",
            f"File: {st.session_state['file_name']}\n\n"
            f"The uploaded document has been processed successfully. "
            f"Use the tabs below to ask questions, generate a summary, or create study material.",
            height=220,
            label_visibility="collapsed"
        )

    with right_col:
        st.write(f"**Document ID:** `{st.session_state['document_id']}`")
        st.write(f"**File Name:** {st.session_state['file_name']}")
        st.write(f"**Pages:** {st.session_state['pages']}")
        st.write(f"**Chunks:** {st.session_state['chunks']}")
        st.write(f"**Detected Language:** {st.session_state['detected_language']}")
        st.write(f"**Output Language:** {output_language}")

    st.markdown("</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        ["💬 Ask Questions", "📝 Summarize", "📚 Study Mode"]
    )

    with tab1:
        st.subheader("Document Question Answering")

        # Smaller height = no huge gap
        chat_height = 260 if len(st.session_state["chat_history"]) == 0 else 420

        chat_container = st.container(height=chat_height, border=False)

        with chat_container:
            if not st.session_state["chat_history"]:
                st.info("Ask a question below to start chatting with your document.")

            for i, chat in enumerate(st.session_state["chat_history"], start=1):
                with st.chat_message("user"):
                    st.write(chat["question"])

                with st.chat_message("assistant"):
                    st.write(chat["answer"])
                    st.caption(f"Source Pages: {chat['source_pages']}")

                   

        # Input directly below messages
        question = st.chat_input("Ask anything about the uploaded document...")

        if question:
            with st.spinner("Generating answer...🏃‍♀️‍➡️"):
                try:
                    result = ask_question(
                        document_id=st.session_state["document_id"],
                        question=question,
                        output_language=output_language
                    )

                    st.session_state["chat_history"].append(
                        {
                            "question": question,
                            "answer": result["answer"],
                            "source_pages": result["source_pages"],
                            "source_chunks": result["source_chunks"]
                        }
                    )

                    # After new question, rerender so messages stay above input
                    st.rerun()

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Ensure FastAPI is running on http://127.0.0.1:8000")
                except requests.exceptions.HTTPError as e:
                    st.error(f"❌ API Error: {e.response.status_code} - {e.response.text}")
                except Exception as e:
                    st.error(f"❌ Error generating answer: {str(e)}")

    with tab2:
        st.subheader("Document Summarization")

        summary_type = st.selectbox(
            "Summary Type",
            ["short", "detailed", "bullet"]
        )

        if st.button("Generate Summary", use_container_width=True):
            with st.spinner("Generating summary..."):
                try:
                    result = generate_summary(
                        document_id=st.session_state["document_id"],
                        summary_type=summary_type,
                        output_language=output_language
                    )
                    st.session_state["summary_output"] = result["summary"]
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

        if st.session_state["summary_output"]:
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>Generated Summary</div>", unsafe_allow_html=True)
            st.write(st.session_state["summary_output"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                "Download Summary 📩",
                st.session_state["summary_output"],
                file_name="summary.txt",
                use_container_width=True
            )

    with tab3:
        st.subheader("Study Material Generator")

        if st.button("Generate Study Material", use_container_width=True):
            with st.spinner("Generating study material..."):
                try:
                    result = generate_study_material(
                        document_id=st.session_state["document_id"],
                        output_language=output_language
                    )
                    st.session_state["study_output"] = result["study_material"]
                except Exception as e:
                    st.error(f"Error generating study material: {e}")

        if st.session_state["study_output"]:
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>Generated Study Material</div>", unsafe_allow_html=True)
            st.write(st.session_state["study_output"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                "Download Study Material 📩",
                st.session_state["study_output"],
                file_name="study_material.txt",
                use_container_width=True
            )

else:
    st.info("Upload a PDF from the sidebar to begin.")

st.markdown(
    """
    <div class="footer-box">
        LinguaDoc AI • Streamlit frontend • FastAPI backend • OpenAI • FAISS • Persistent storage
    </div>
    """,
    unsafe_allow_html=True
)