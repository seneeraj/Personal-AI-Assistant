from backend.rag.vector_store import search_vector
from backend.rag.embedding_service import model
from backend.rag.query_expansion import expand_query


def retrieve_context(query, source_document=None):
    """
    Retrieve relevant context from vector database.
    Ensures that chunks come from a single document.
    """

    expanded_queries = expand_query(query)

    print("Original Query:", query)
    print("Expanded Queries:", expanded_queries)

    # --------------------------------
    # Create embedding for query
    # --------------------------------
    query_embedding = model.encode([query])[0]

    # --------------------------------
    # Search vector DB
    # --------------------------------
    vector_results = search_vector(query_embedding, top_k=10)

    if not vector_results:
        return "", []

    # --------------------------------
    # Group results by document
    # --------------------------------
    doc_chunks = {}

    for r in vector_results:

        doc = r.get("source", "unknown")

        if source_document and doc != source_document:
            continue

        if doc not in doc_chunks:
            doc_chunks[doc] = []

        doc_chunks[doc].append(r)

    if not doc_chunks:
        return "", []

    # --------------------------------
    # Select best document
    # --------------------------------
    best_doc = None
    best_score = float("inf")

    for doc, chunks in doc_chunks.items():

        scores = []

        for c in chunks:

            if "distance" in c:
                scores.append(c["distance"])

            elif "score" in c:
                scores.append(c["score"])

            else:
                scores.append(1)

        avg_score = sum(scores) / len(scores)

        if avg_score < best_score:
            best_score = avg_score
            best_doc = doc

    # --------------------------------
    # Select top chunks from best doc
    # --------------------------------
    best_chunks = doc_chunks[best_doc][:5]

    context = "\n\n".join(
        chunk.get("content", "") for chunk in best_chunks
    )

    return context, best_chunks