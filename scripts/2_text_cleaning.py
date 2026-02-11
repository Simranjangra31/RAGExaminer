import os
import re

PROCESSED_PATH = "../data/processed/"

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

for subject in os.listdir(PROCESSED_PATH):
    subject_path = os.path.join(PROCESSED_PATH, subject)

    for file in os.listdir(subject_path):
        if file.endswith(".txt"):
            file_path = os.path.join(subject_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                cleaned = clean_text(f.read())
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

print("✅ Text cleaning completed")
