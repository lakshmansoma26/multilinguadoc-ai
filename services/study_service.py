from openai import OpenAI
from core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_study_material(document_text: str, output_language: str = "English") -> str:
    """
    Generate study material from the document:
    - short-answer questions with answers
    - MCQs
    - flashcards
    """
    prompt = f"""
You are an educational assistant.

Based ONLY on the document below, generate:

1. 5 short-answer questions with answers
2. 5 multiple-choice questions with 4 options each and the correct answer
3. 5 flashcards in question-answer format

Rules:
- Use only the document content
- Do not invent facts
- Keep the questions useful for studying
- Return everything in {output_language}

Document:
{document_text[:12000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You create study material strictly from source documents."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()