from openai import OpenAI
from core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_summary(document_text: str, output_language: str = "English", summary_type: str = "short") -> str:
   
    if summary_type == "bullet":
        instruction = "Summarize the document as clear bullet points."
    elif summary_type == "detailed":
        instruction = "Provide a detailed summary of the document."
    else:
        instruction = "Provide a short concise summary of the document."

    prompt = f"""
You are a multilingual document summarization assistant.

Rules:
1. Summarize only the provided document.
2. Do not add facts not present in the document.
3. Return the output in {output_language}.

Task:
{instruction}

Document:
{document_text[:12000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You summarize documents accurately."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()