from langdetect import detect, LangDetectException
from core.constants import SUPPORTED_LANGUAGES


def detect_language(text: str) -> dict:
    if not text or not text.strip():
        return {
            "language_code": "unknown",
            "language_name": "Unknown"
        }

    try:
        detected_code = detect(text)

        language_name = SUPPORTED_LANGUAGES.get(detected_code, "Unsupported/Unknown")

        return {
            "language_code": detected_code,
            "language_name": language_name
        }

    except LangDetectException:
        return {
            "language_code": "unknown",
            "language_name": "Unknown"
        }