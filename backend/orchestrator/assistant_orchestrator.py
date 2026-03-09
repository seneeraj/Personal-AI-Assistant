from backend.agents.document_agent import document_agent
from backend.agents.research_agent import research_agent
from backend.agents.tool_agent import tool_agent
from backend.agents.planner_agent import planner_agent
from backend.agents.memory_agent import store_message


def run_assistant(message, document=None):

    # store user message
    store_message("user", message)

    # planner decides which agent to use
    agent = planner_agent(message)

    print(f"[AGENT] {agent} handling: {message}")

    # ----------------------------
    # Document Agent
    # ----------------------------
    if agent == "document_agent":

        response, sources = document_agent(
            message,
            document
        )

    # ----------------------------
    # Research Agent
    # ----------------------------
    elif agent == "research_agent":

        response = research_agent(message)
        sources = []

    # ----------------------------
    # Tool Agent
    # ----------------------------
    else:

        response = tool_agent(message)
        sources = []

    # store assistant message
    store_message("assistant", response)

    return response, sources