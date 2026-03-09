from backend.rag.vector_store import client


def planner_agent(query: str):

    query_lower = query.lower()

    # detect if user explicitly mentions document
    if ".pdf" in query_lower:
        return "document_agent"

    # check if documents exist in vector DB
    collections = client.list_collections()

    if len(collections) > 0:
        return "document_agent"

    # fallback to research
    return "research_agent"