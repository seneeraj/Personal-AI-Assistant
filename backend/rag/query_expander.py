from backend.services.llm_service import generate_response


def expand_query(query):

    prompt = f"""
Rewrite the following user query to improve document retrieval.

Original Query:
{query}

Expanded Query:
"""

    expanded = generate_response(prompt)

    if expanded:
        return expanded.strip()

    return query