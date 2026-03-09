from backend.services.llm_service import generate_response
from backend.tools.tool_engine import run_python, web_search, analyze_text


def tool_agent(query):

    query_lower = query.lower()

    # Python execution
    if "calculate" in query_lower or "python" in query_lower:

        code_prompt = f"""
Generate Python code for this task:
{query}

Return only the code.
"""

        code = generate_response(code_prompt)

        return run_python(code)

    # Web search
    if "search" in query_lower or "latest" in query_lower:

        return web_search(query)

    # Text analysis
    if "analyze text" in query_lower:

        return analyze_text(query)

    # fallback
    return generate_response(query)