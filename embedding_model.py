# app/embedding_model.py

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    if not text:
        return [0.0]

    # SentenceTransformers already returns a numpy array (not list)
    return model.encode(text)
