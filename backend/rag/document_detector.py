import os


def detect_document_name(query):

    documents = os.listdir("documents")

    query_lower = query.lower()

    for doc in documents:

        if doc.lower() in query_lower:
            return doc

    return None