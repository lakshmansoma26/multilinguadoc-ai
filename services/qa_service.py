from core.constants import TOP_K_RESULTS
from services.retrieval_service import retrieve_relevant_chunks
from services.llm_service import generate_answer_from_context


def answer_question(
    question: str,
    index,
    chunks: list[dict],
    output_language: str = "English",
    full_text: str | None = None
) -> dict:
    """
    QA pipeline using:
    - broad document context for high-level understanding
    - retrieved evidence for precise answering
    """

    relevant_chunks = retrieve_relevant_chunks(
        question=question,
        index=index,
        chunks=chunks,
        top_k=TOP_K_RESULTS
    )

    retrieved_context = "\n\n".join(
        (
            f"[Evidence {i+1} | Page {chunk['page']} | {chunk['chunk_id']} | Distance {chunk.get('distance', 0):.4f}]\n"
            f"{chunk['text']}"
        )
        for i, chunk in enumerate(relevant_chunks)
    )

    broad_context = full_text[:5000] if full_text else retrieved_context

    answer = generate_answer_from_context(
        question=question,
        broad_context=broad_context,
        retrieved_context=retrieved_context,
        output_language=output_language
    )

    source_pages = sorted({chunk["page"] for chunk in relevant_chunks})

    return {
        "question": question,
        "answer": answer,
        "source_pages": source_pages,
        "source_chunks": relevant_chunks,
        "broad_context_used": broad_context,
        "retrieved_context_used": retrieved_context
    }