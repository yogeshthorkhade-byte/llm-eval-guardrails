from app.rag import create_chunks


chunks = create_chunks(
    "data/ai_notes.pdf"
)


print(f"Total Chunks: {len(chunks)}")

print()

print(chunks[0])