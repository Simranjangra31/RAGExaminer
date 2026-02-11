import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(BASE_DIR, "..", "embeddings", "faiss_index.index")
META_PATH = os.path.join(BASE_DIR, "..", "embeddings", "metadata.pkl")

index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(subject, topic, k=6):
    query = f"{subject} {topic}"
    q_embedding = model.encode([query])

    _, indices = index.search(np.array(q_embedding), k)

    context = []
    for i in indices[0]:
        if metadata[i]["subject"] == subject and metadata[i]["topic"] == topic:
            context.append(metadata[i]["text"])

    return context
