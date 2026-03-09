from sentence_transformers import SentenceTransformer
import pdfplumber

# --------------------------------------------
# Load embedding model
# --------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------
# Extract text from PDF
# --------------------------------------------

def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# --------------------------------------------
# Chunk text with overlap
# --------------------------------------------

def chunk_text(text, chunk_size=500, overlap=100):

    if not text:
        return []

    words = text.split()

    chunks = []
    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# --------------------------------------------
# Generate embeddings for chunks
# --------------------------------------------

def generate_embeddings(chunks):

    if not chunks:
        return []

    embeddings = model.encode(chunks)

    return embeddings.tolist()