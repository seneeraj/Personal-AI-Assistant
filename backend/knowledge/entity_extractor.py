import re


def extract_entities(text):

    words = re.findall(r"\b[A-Z][a-zA-Z]{3,}\b", text)

    entities = list(set(words))

    return entities[:40]