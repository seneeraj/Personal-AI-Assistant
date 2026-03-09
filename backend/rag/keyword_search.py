from rank_bm25 import BM25Okapi


class KeywordSearch:

    def __init__(self):

        self.documents = []
        self.tokenized = []
        self.bm25 = None

    def index(self, chunks):

        if not chunks:
            return

        # store documents
        self.documents.extend(chunks)

        # tokenize
        self.tokenized = [doc.split() for doc in self.documents]

        # build BM25 index
        if self.tokenized:
            self.bm25 = BM25Okapi(self.tokenized)

    def search(self, query, top_k=5):

        if not self.bm25:
            return []

        tokens = query.split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, score in ranked[:top_k]]


keyword_engine = KeywordSearch()