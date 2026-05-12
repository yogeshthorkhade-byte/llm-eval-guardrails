from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from app.pdf_loader import load_pdf


# --------------------------------
# Create Chunks
# --------------------------------

def create_chunks(file_path):

    # Load PDF text
    text = load_pdf(file_path)


    # Create splitter
    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
    )


    # Split text
    chunks = splitter.split_text(text)

    return chunks