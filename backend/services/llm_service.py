import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "mistral"


def generate_response(prompt):

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    return data.get("response", "")


# ---------------------------------------------------
# NEW FUNCTION FOR RAG ANSWERING
# ---------------------------------------------------

def generate_answer(question, context):

    prompt = f"""
You are an AI assistant answering questions ONLY from the provided document context.

Rules:
- Answer ONLY using the context
- If the answer is not present, say: "The answer is not found in the provided documents."
- Keep answers concise.

Context:
{context}

Question:
{question}

Answer:
"""

    return generate_response(prompt)