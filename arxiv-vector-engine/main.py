import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from src.model import PhysicsEmbedder
from src.database import VectorVault

DATA_PATH  = os.path.join(os.path.dirname(__file__), "data", "arxiv_data.csv")
DB_PATH    = os.path.join(os.path.dirname(__file__), "physics_db")
BATCH_SIZE = 512   # safe batch size for embedding + ChromaDB


def load_and_index(vault: VectorVault, embedder: PhysicsEmbedder):
    print(f"\nLoading data from {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH).fillna("")
    total = len(df)
    print(f"Total papers to index: {total}")

    for batch_start in range(0, total, BATCH_SIZE):
        batch = df.iloc[batch_start: batch_start + BATCH_SIZE]
        texts = (batch["titles"] + ". " + batch["summaries"]).tolist()
        ids   = [str(i) for i in range(batch_start, batch_start + len(batch))]
        meta  = [{"title": row["titles"], "terms": row["terms"]}
                 for _, row in batch.iterrows()]

        print(f"\n[{batch_start + len(batch)}/{total}] Embedding batch ...")
        vectors = embedder.generate_vectors(texts)

        vault.store_papers(ids=ids, vectors=vectors, metadata=meta, documents=texts)

    print(f"\n[OK] All {total} papers indexed.\n")


def search(vault: VectorVault, embedder: PhysicsEmbedder, query: str, n: int = 5):
    q_vec = embedder.generate_vectors([query])
    results = vault.search_vault(q_vec, n_results=n)

    docs      = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print(f"\nTop {n} results for: \"{query}\"\n" + "-" * 60)
    for rank, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances), 1):
        title = meta.get("title", "")
        terms = meta.get("terms", "")
        score = round(1 - dist, 4)          # cosine similarity approx
        print(f"{rank}. [{score}] {title}")
        print(f"   Terms : {terms}")
        summary_preview = doc[:200].replace("\n", " ")
        print(f"   Summary: {summary_preview}...")
        print()


def main():
    print("=== ArXiv RAG Vector Search Engine ===")

    embedder = PhysicsEmbedder()
    vault    = VectorVault(path=DB_PATH)

    # Check total rows in CSV to decide if re-indexing is needed
    total_in_csv = len(pd.read_csv(DATA_PATH))
    count = vault.collection.count()
    if count < total_in_csv:
        if count > 0:
            print(f"Collection has {count}/{total_in_csv} papers — clearing and re-indexing all ...")
            vault.client.delete_collection("arxiv_physics")
            vault.collection = vault.client.get_or_create_collection(name="arxiv_physics")
        else:
            print("Collection is empty — indexing all papers ...")
        load_and_index(vault, embedder)
    else:
        print(f"Collection already has all {count} papers. Skipping indexing.")

    print("\nEnter a search query (or 'quit' to exit):")
    while True:
        try:
            query = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        search(vault, embedder, query)


if __name__ == "__main__":
    main()
