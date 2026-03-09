from backend.rag.retrieval_service import retrieve_context
from backend.services.llm_service import generate_answer


def document_agent(question, document=None, memory_context=None):

    print(f"[AGENT] document_agent handling: {question}")

    # ---------------------------------------
    # Retrieve context from vector database
    # ---------------------------------------
    context, sources = retrieve_context(question, document)

    # ---------------------------------------
    # If nothing retrieved → safe response
    # ---------------------------------------
    if not context or context.strip() == "":
        return (
            "I could not find this information in your uploaded documents.",
            []
        )

    # ---------------------------------------
    # Add optional memory context
    # ---------------------------------------
    if memory_context:
        context = memory_context + "\n\n" + context

    # ---------------------------------------
    # Generate answer strictly from context
    # ---------------------------------------
    answer = generate_answer(
        question=question,
        context=context
    )

    # ---------------------------------------
    # Safety fallback
    # ---------------------------------------
    if not answer or answer.strip() == "":
        return (
            "I could not find this information in your uploaded documents.",
            []
        )

    return answer, sources