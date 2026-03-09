import os
from backend.rag.vector_store import collection

DOCUMENT_DIR = "documents"


# -----------------------------
# List Documents
# -----------------------------
def list_documents():

    if not os.path.exists(DOCUMENT_DIR):
        return []

    return os.listdir(DOCUMENT_DIR)


# -----------------------------
# Delete Document
# -----------------------------
def delete_document(document_name):

    try:

        results = collection.get()

        ids_to_delete = []

        for i, meta in enumerate(results["metadatas"]):

            if meta["source"] == document_name:
                ids_to_delete.append(results["ids"][i])

        if ids_to_delete:
            collection.delete(ids=ids_to_delete)

    except Exception as e:
        print("Vector delete error:", e)


# -----------------------------
# Document Statistics
# -----------------------------
def document_statistics():

    docs = list_documents()

    try:
        total_chunks = collection.count()
    except:
        total_chunks = 0

    return {
        "total_documents": len(docs),
        "total_chunks": total_chunks,
        "documents": docs
    }