import requests
from backend.services.llm_service import generate_response


def research_agent(query):

    # simple web knowledge prompt
    prompt = f"""
You are a research assistant.

Answer the following question using your knowledge.

Question:
{query}
"""

    answer = generate_response(prompt)

    return answer