from services.language_service import detect_language


def test_detect_english_language():
    text = "Artificial intelligence is transforming education and healthcare."
    result = detect_language(text)

    assert result["language_code"] == "en"
    assert result["language_name"] == "English"