
import faiss
import numpy as np
import json
import os

from src.rag.embeddings import model


# Store vectors in FAISS
def save_vectors(chunks, vectors):

    vectors = np.array(vectors).astype("float32")

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(vectors)

    # Create FAISS index
    index = faiss.IndexFlatIP(vectors.shape[1])

    # Add vectors to index
    index.add(vectors)

    # Create storage folder
    os.makedirs("data/processed", exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, "data/processed/index.faiss")

    # Save chunks
    with open("data/processed/chunks.json", "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=4)

    print("Vectors saved successfully!")


# Search for similar chunks
def search_vectors(question, top_k=3):

    # Load FAISS index
    index = faiss.read_index("data/processed/index.faiss")

    # Load stored chunks
    with open("data/processed/chunks.json", "r", encoding="utf-8") as file:
        chunks = json.load(file)

    # Convert question into embedding
    question_vector = model.encode([question])

    question_vector = np.array(question_vector).astype("float32")

    faiss.normalize_L2(question_vector)

    # Search similar vectors
    scores, indices = index.search(question_vector, top_k)

    results = []

    for i in indices[0]:

        if i != -1:
            results.append(chunks[i])

    return results


if __name__ == "__main__":

    print("Vector store module created!")
