conversation_memory = []


def store_message(role, content):

    conversation_memory.append({
        "role": role,
        "content": content
    })


def get_recent_memory(limit=6):

    return conversation_memory[-limit:]


def format_memory_for_prompt():

    history = get_recent_memory()

    formatted = ""

    for msg in history:
        formatted += f"{msg['role']}: {msg['content']}\n"

    return formatted