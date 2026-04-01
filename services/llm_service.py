from openai import OpenAI
from core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer_from_context(
    question: str,
    broad_context: str,
    retrieved_context: str,
    output_language: str = "English"
) -> str:
    """
    Generate an answer using document-wide context and retrieved evidence.
    """

    prompt = f"""
You are a multilingual document question-answering assistant.

Answer the user's question ONLY using the information below.

You are given:
1. Broad document context for understanding the full document
2. Retrieved evidence for precise details

Rules:
1. Do not invent facts.
2. If the question is broad, use the broad document context.
3. If the question is specific, prioritize retrieved evidence.
4. If retrieved evidence conflicts with broad context, prioritize retrieved evidence.
5. If the answer is not supported by the provided information, say:
   "The document does not provide enough information to answer this question."
6. Keep the answer clear and concise.
7. Return the answer in {output_language}.

Broad Document Context:
{broad_context}

Retrieved Evidence:
{retrieved_context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You answer questions strictly from provided document evidence."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()