import os
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if text and text.strip():
                pages_data.append(
                    {
                        "page": page_number,
                        "text": text.strip()
                    }
                )

    return pages_data


def combine_pages_to_text(pages_data: list[dict]) -> str:
    return "\n\n".join(page["text"] for page in pages_data if page.get("text"))