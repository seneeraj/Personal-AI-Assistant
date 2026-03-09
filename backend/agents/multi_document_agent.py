from backend.rag.retrieval_service import retrieve_context
from backend.services.llm_service import generate_response


def multi_document_agent(question):

    context, sources = retrieve_context(question)

    prompt = f"""
You are an expert document analyst.

Using the context below, compare information across documents.

Context:
{context}

Question:
{question}
"""

    answer = generate_response(prompt)

    return answer, sources