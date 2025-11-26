# app/pdf_rag.py

import pypdf
from sentence_transformers import SentenceTransformer
from .embedding_store import upsert_texts, semantic_search

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_pdf(pdf_path: str):
    """Extract text from PDF, generate embeddings, insert into store."""
    reader = pypdf.PdfReader(pdf_path)

    chunks = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            chunks.append(text.strip())

    if not chunks:
        return 0

    # Convert embeddings → list so they work with your store
    vectors = model.encode(chunks, convert_to_numpy=True)
    vectors = [v.tolist() for v in vectors]

    upsert_texts(chunks, vectors)
    return len(chunks)


def retrieve_for_query(query: str, k: int = 4) -> str:
    """Embed query → semantic search → return combined string."""
    q_vec = model.encode([query], convert_to_numpy=True)[0].tolist()

    results = semantic_search(q_vec, k=k)

    if not results:
        return "No relevant information found in the PDF."

    # semantic_search returns list of text chunks
    return "\n\n---\n\n".join(results)
