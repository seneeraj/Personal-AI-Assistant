from backend.agents.document_agent import document_agent
from backend.agents.research_agent import research_agent
from backend.agents.tool_agent import tool_agent


def execute_step(step, user_query, document=None):

    step_lower = step.lower()

    if "document" in step_lower or "extract" in step_lower:
        result, _ = document_agent(user_query, document)
        return result

    if "research" in step_lower:
        return research_agent(user_query)

    return tool_agent(user_query)