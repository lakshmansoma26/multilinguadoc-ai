from services.pdf_service import combine_pages_to_text


def test_combine_pages_to_text():
    sample_pages = [
        {"page": 1, "text": "Hello world"},
        {"page": 2, "text": "This is page two"}
    ]

    combined_text = combine_pages_to_text(sample_pages)

    assert "Hello world" in combined_text
    assert "This is page two" in combined_text