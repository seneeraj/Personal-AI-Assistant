from backend.services.llm_service import generate_answer


def compress_context(query, chunks):

    compressed_chunks = []

    for chunk in chunks:

        prompt = f"""
You are a document filtering system.

User question:
{query}

Document text:
{chunk}

Return ONLY the sentences relevant to answering the question.
If nothing is relevant, return: NONE
"""

        result = generate_answer(prompt)

        if result and result.strip() != "NONE":
            compressed_chunks.append(result.strip())

    return compressed_chunks