import faiss

import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


# --------------------------------
# Load Embedding Model
# --------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------
# Create Vector Store
# --------------------------------

def create_vector_store(chunks):

    # Remove empty chunks
    chunks = [

        chunk.strip()

        for chunk in chunks

        if chunk.strip()
    ]


    # Safety check
    if len(chunks) == 0:

        raise ValueError(
            "No valid chunks found"
        )


    # Create embeddings
    embeddings = model.encode(
        chunks
    )


    # Convert to numpy array
    embeddings = np.array(
        embeddings
    )


    # Ensure 2D shape
    if len(embeddings.shape) != 2:

        raise ValueError(
            "Embeddings shape invalid"
        )


    # Get vector dimension
    dimension = embeddings.shape[1]


    # Create FAISS index
    index = faiss.IndexFlatL2(
        dimension
    )


    # Add embeddings
    index.add(
        embeddings.astype("float32")
    )


    return index, embeddings


# --------------------------------
# Retrieve Chunks
# --------------------------------

def retrieve_chunks(
    query,
    chunks,
    index,
    top_k=3
):

    # Encode query
    query_embedding = model.encode(
        [query]
    )


    query_embedding = np.array(
        query_embedding
    ).astype("float32")


    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )


    results = []


    for i, idx in enumerate(indices[0]):

        results.append({

            "chunk": chunks[idx],

            "score":
                float(
                    distances[0][i]
                )
        })


    return results