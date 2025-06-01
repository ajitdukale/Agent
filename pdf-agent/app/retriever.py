import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def add(self, chunk_embedding_pairs):
        embeddings = np.array([pair[1] for pair in chunk_embedding_pairs]).astype("float32")
        self.index.add(embeddings)
        self.chunks = [pair[0] for pair in chunk_embedding_pairs]

    def search(self, query_embedding, top_k=5):
        D, I = self.index.search(np.array([query_embedding]).astype("float32"), top_k)
        return [self.chunks[i] for i in I[0]]
