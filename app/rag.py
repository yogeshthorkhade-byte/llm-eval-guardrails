from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)
from app.chunk_utils import (
    create_chunks
)
from app.pdf_loader import load_pdf

from app.document_manager import (
    get_vector_store
)

from app.vector_store import (
    retrieve_chunks
)


# -------------------------------


# --------------------------------
# Retrieve Context
# --------------------------------

def get_relevant_context(query):

    index, chunks = (
        get_vector_store()
    )


    results = retrieve_chunks(
        query,
        chunks,
        index
    )


    context_list = []


    for item in results:

        context_list.append(
            item["chunk"]
        )


    context = "\n\n".join(
        context_list
    )


    return context, results