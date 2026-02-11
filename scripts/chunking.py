import os
import json

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_PATH = os.path.join(BASE_DIR, "..", "data", "processed")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "data", "chunks.json")

def chunk_text(text):
    words = text.split()
    chunks = []
    for i in range(0, len(words), CHUNK_SIZE - CHUNK_OVERLAP):
        chunks.append(" ".join(words[i:i + CHUNK_SIZE]))
    return chunks

all_chunks = []

for subject in os.listdir(PROCESSED_PATH):
    subject_path = os.path.join(PROCESSED_PATH, subject)

    if not os.path.isdir(subject_path):
        continue

    for file in os.listdir(subject_path):
        if not file.endswith(".txt"):
            continue

        topic = file.replace(".txt", "")
        file_path = os.path.join(subject_path, file)

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        chunks = chunk_text(text)

        for chunk in chunks:
            if chunk.strip():
                all_chunks.append({
                    "text": chunk,
                    "subject": subject,
                    "topic": topic,
                    "source": file
                })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2)

print(f"✅ Created {len(all_chunks)} chunks across all subjects")
print(f"📁 Saved to {OUTPUT_FILE}")
