import os
import json
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHUNKS_FILE = os.path.join(BASE_DIR, "..", "data", "chunks.json")
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "..", "embeddings")

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# Load chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

if len(chunks) == 0:
    raise ValueError("❌ No chunks found. Run 3_chunking.py first.")

texts = [c["text"] for c in chunks]
metadata = chunks

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(texts, show_progress_bar=True)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, os.path.join(EMBEDDINGS_DIR, "faiss_index.index"))

with open(os.path.join(EMBEDDINGS_DIR, "metadata.pkl"), "wb") as f:
    pickle.dump(metadata, f)

print("✅ Embeddings created and stored successfully")
