from backend.knowledge.knowledge_graph import get_related


def knowledge_agent(query):

    words = query.split()

    for word in words:

        related = get_related(word)

        if related:

            return f"{word} is related to: {', '.join(related)}"

    return "No knowledge graph relationships found."