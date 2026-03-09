from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import os

from backend.rag.embedding_service import (
    extract_text_from_pdf,
    chunk_text,
    generate_embeddings
)

from backend.rag.vector_store import store_embeddings
from backend.rag.keyword_search import keyword_engine

from backend.services.document_manager import (
    list_documents,
    delete_document,
    document_statistics
)

router = APIRouter(prefix="/api", tags=["Documents"])

DOCUMENT_DIR = "documents"
os.makedirs(DOCUMENT_DIR, exist_ok=True)


# ----------------------------------------------------
# Upload Document
# ----------------------------------------------------

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    try:

        file_path = os.path.join(DOCUMENT_DIR, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        print(f"STORING DOCUMENT: {file.filename}")

        # -------------------------
        # Extract text
        # -------------------------
        text = extract_text_from_pdf(file_path)

        if not text or text.strip() == "":
            return {
                "status": "error",
                "message": "No text extracted from PDF"
            }

        # -------------------------
        # Chunk text
        # -------------------------
        chunks = chunk_text(text)

        if not chunks:
            return {
                "status": "error",
                "message": "Chunking failed"
            }

        print("Chunks created:", len(chunks))
        
        
        # -------------------------
        # Generate embeddings
        # -------------------------
        embeddings = generate_embeddings(chunks)
        
        
        from backend.rag.vector_store import collection

        # remove existing chunks for this document
        existing = collection.get()

        ids_to_delete = []

        for i, meta in enumerate(existing["metadatas"]):
            if meta["source"] == file.filename:
                ids_to_delete.append(existing["ids"][i])

        if ids_to_delete:
            collection.delete(ids=ids_to_delete)

        # -------------------------
        # Store embeddings
        # -------------------------
        store_embeddings(
            chunks,
            embeddings,
            file.filename
        )

        # -------------------------
        # Update keyword search index
        # -------------------------
        keyword_engine.index(chunks)

        print(f"{len(chunks)} chunks stored from {file.filename}")

        return {
            "status": "success",
            "message": f"{file.filename} processed",
            "chunks_created": len(chunks)
        }

    except Exception as e:

        print("UPLOAD ERROR:", str(e))

        return {
            "status": "error",
            "message": str(e)
        }


# ----------------------------------------------------
# List Documents
# ----------------------------------------------------

@router.get("/documents/list")
def get_documents():

    docs = list_documents()

    return {
        "status": "success",
        "documents": docs
    }


# ----------------------------------------------------
# Delete Single Document
# ----------------------------------------------------

@router.delete("/documents/delete/{document_name}")
def remove_document(document_name: str):

    delete_document(document_name)

    return {
        "status": "success",
        "message": f"{document_name} deleted"
    }


# ----------------------------------------------------
# Delete Multiple Documents
# ----------------------------------------------------

class DeleteRequest(BaseModel):
    documents: list[str]


@router.post("/documents/delete")
async def delete_documents(request: DeleteRequest):

    deleted = []

    for doc in request.documents:

        file_path = os.path.join(DOCUMENT_DIR, doc)

        if os.path.exists(file_path):

            os.remove(file_path)
            deleted.append(doc)

            # Remove embeddings
            delete_document(doc)

    return {
        "status": "success",
        "deleted": deleted
    }


# ----------------------------------------------------
# Document Statistics
# ----------------------------------------------------

from backend.rag.vector_store import collection
import os

DOCUMENT_DIR = "documents"


def document_statistics():

    docs = os.listdir(DOCUMENT_DIR) if os.path.exists(DOCUMENT_DIR) else []

    total_chunks = 0
    total_tokens = 0

    try:
        results = collection.get()

        documents = results.get("documents", [])

        total_chunks = len(documents)

        # approximate tokens (1 token ≈ 0.75 words)
        for doc in documents:
            total_tokens += len(doc.split())

    except:
        pass

    # simple token estimate
    total_tokens = int(total_tokens * 1.3)

    return {
        "total_documents": len(docs),
        "total_chunks": total_chunks,
        "total_tokens": total_tokens
    }

@router.get("/documents/stats")
def get_document_stats():

    stats = document_statistics()

    return {
        "status": "success",
        "statistics": stats
    }