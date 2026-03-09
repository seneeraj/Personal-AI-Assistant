from collections import defaultdict


def rank_documents(vector_results):

    document_scores = defaultdict(list)

    for result in vector_results:
        source = result["source"]
        score = result["score"]

        document_scores[source].append(score)

    ranked_documents = []

    for doc, scores in document_scores.items():

        avg_score = sum(scores) / len(scores)

        ranked_documents.append((doc, avg_score))

    ranked_documents.sort(key=lambda x: x[1])

    if not ranked_documents:
        return None

    best_document = ranked_documents[0][0]

    return best_document