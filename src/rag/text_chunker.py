
def create_chunks(text, chunk_size=500, overlap=50):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks


if __name__ == "__main__":

    text = """
    Artificial Intelligence is a technology that helps
    machines perform intelligent tasks.

    Machine Learning is a subset of Artificial Intelligence.

    Deep Learning uses neural networks to learn complex patterns.
    """

    chunks = create_chunks(text, chunk_size=100, overlap=20)

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks):
        print("\nChunk", i + 1)
        print(chunk)
