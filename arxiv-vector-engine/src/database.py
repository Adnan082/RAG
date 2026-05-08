import chromadb

class VectorVault:
    def __init__(self, path="./physics_db"):
        # Creates a folder named 'physics_db' where your data lives permanently
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name="arxiv_physics")

    def store_papers(self, ids, vectors, metadata, documents):
        self.collection.add(
            ids=ids,
            embeddings=vectors.tolist(),
            metadatas=metadata,
            documents=documents
        )

    def search_vault(self, query_vector, n_results=3):
        # This does the high-dimensional math to find the closest answers
        return self.collection.query(
            query_embeddings=query_vector.tolist(),
            n_results=n_results
        )