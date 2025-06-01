from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')  # Local embedding model

def embed_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return [(chunk, embedding) for chunk, embedding in zip(chunks, embeddings)]
