from services.qa_service import answer_question


class DummyIndex:
    pass


def test_answer_question_returns_expected_structure(monkeypatch):
    dummy_chunks = [
        {"chunk_id": "chunk_1", "page": 1, "text": "AI internship at Smart Bridge."},
        {"chunk_id": "chunk_2", "page": 1, "text": "Worked on poultry disease detection."}
    ]

    def mock_retrieve_relevant_chunks(question, index, chunks, top_k):
        return dummy_chunks

    def mock_generate_answer_from_context(question, context, output_language):
        return "The person worked as an AI and ML intern."

    monkeypatch.setattr(
        "services.qa_service.retrieve_relevant_chunks",
        mock_retrieve_relevant_chunks
    )

    monkeypatch.setattr(
        "services.qa_service.generate_answer_from_context",
        mock_generate_answer_from_context
    )

    result = answer_question(
        question="What internship experience does this person have?",
        index=DummyIndex(),
        chunks=dummy_chunks,
        output_language="English"
    )

    assert "answer" in result
    assert "source_pages" in result
    assert "source_chunks" in result
    assert result["answer"] == "The person worked as an AI and ML intern."
    assert result["source_pages"] == [1]
    assert len(result["source_chunks"]) == 2