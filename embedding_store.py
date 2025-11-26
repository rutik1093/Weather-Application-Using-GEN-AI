# app/embedding_store.py

import numpy as np

# In-memory vector store
DATABASE = []  # each item: {"text": "...", "vector": np.array([...])}


def upsert_texts(texts, vectors):
    for t, v in zip(texts, vectors):
        DATABASE.append({
            "text": t,
            "vector": np.array(v, dtype=float)
        })


def semantic_search(query_vector, k=4):
    q = np.array(query_vector, dtype=float)

    scored = []
    for item in DATABASE:
        vec = item["vector"]
        if vec is None:
            continue

        # cosine similarity
        score = np.dot(q, vec) / (np.linalg.norm(q) * np.linalg.norm(vec))
        scored.append({
            "text": item["text"],
            "score": float(score)
        })

    # highest score → most relevant
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]
