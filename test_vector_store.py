from app.rag import create_chunks

from app.vector_store import (
    create_vector_store,
    retrieve_chunks
)


# Create chunks from PDF
chunks = create_chunks(
    "data/ai_notes.pdf"
)


# Create vector database
index, embeddings = (
    create_vector_store(chunks)
)


# User query
query = "What is this document about?"


# Retrieve relevant chunks
results = retrieve_chunks(
    query,
    chunks,
    index
)


print("\nRetrieved Chunks:\n")


for chunk in results:

    print(chunk)

    print("\n-------------------\n")