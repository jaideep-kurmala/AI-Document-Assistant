
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):

    # Extract text from chunks
    texts = [chunk["text"] for chunk in chunks]

    # Convert text into numerical vectors
    embeddings = model.encode(texts)

    return embeddings


if __name__ == "__main__":

    sample_texts = [
        {"text": "Artificial Intelligence makes machines intelligent."},
        {"text": "Machine Learning is a subset of AI."},
        {"text": "Python is a programming language."}
    ]

    vectors = create_embeddings(sample_texts)

    print("Embeddings created successfully!")

    print("Total sentences:", len(vectors))
    print("Vector dimensions:", vectors.shape[1])

    print("\nFirst embedding:")
    print(vectors[0])
