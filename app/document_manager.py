from app.chunk_utils import (
    create_chunks
)

from app.vector_store import (
    create_vector_store
)


# Global storage
DOCUMENTS = {}

INDEX = None

CHUNKS = []


# --------------------------------
# Add Document
# --------------------------------

def add_document(file_path):

    global INDEX
    global CHUNKS


    # Create chunks
    chunks = create_chunks(
        file_path
    )


    # Store chunks
    CHUNKS.extend(chunks)


    # Rebuild vector DB
    INDEX, embeddings = (
        create_vector_store(
            CHUNKS
        )
    )


    return {

        "message":
            "Document added successfully",

        "total_chunks":
            len(CHUNKS)
    }


# --------------------------------
# Get Vector Store
# --------------------------------

def get_vector_store():

    return INDEX, CHUNKS