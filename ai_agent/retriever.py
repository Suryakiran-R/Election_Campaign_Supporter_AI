# ai_agent/retriever.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SimpleRetriever:
    def __init__(self, chunks, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.chunks = chunks
        self.embeddings = self.model.encode(chunks)

    def retrieve(self, query, top_k=3):
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices]