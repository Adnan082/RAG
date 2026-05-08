import numpy as np
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


class PhysicsEmbedder:
    def __init__(self, model_name=None):
        print("Loading Embedding Model (ChromaDB built-in ONNX embedder)...")
        # Uses chromadb's onnxruntime-backed all-MiniLM-L6-v2 — no scipy needed
        self.ef = DefaultEmbeddingFunction()
        print("Model loaded.")

    def generate_vectors(self, text_list):
        print(f"Generating vectors for {len(text_list)} items...")
        embeddings = self.ef(text_list)          # returns list of lists
        return np.array(embeddings, dtype="float32")
