import chromadb

# -------------------------------------------------
# Create persistent Chroma client
# -------------------------------------------------

client = chromadb.PersistentClient(path="./vector_db")

# -------------------------------------------------
# Get or create collection
# -------------------------------------------------

collection = client.get_or_create_collection(
    name="documents"
)


# -------------------------------------------------
# Store embeddings
# -------------------------------------------------

def store_embeddings(chunks, embeddings, source):

    ids = [f"{source}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source} for _ in chunks]

    print("DEBUG storing chunks:", len(chunks))

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print("DEBUG stored successfully")


# -------------------------------------------------
# Vector search
# -------------------------------------------------

def search_vector(query_embedding, top_k=5):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    output = []

    if not results["documents"]:
        return []

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(docs, metas, distances):

        output.append({
            "content": doc,
            "source": meta["source"],
            "score": dist
        })

    return output