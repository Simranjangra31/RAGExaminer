from pypdf import PdfReader
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_PATH = os.path.join(BASE_DIR, "..", "data", "raw")
PROCESSED_PATH = os.path.join(BASE_DIR, "..", "data", "processed")

os.makedirs(PROCESSED_PATH, exist_ok=True)

def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

for subject in os.listdir(RAW_PATH):
    subject_path = os.path.join(RAW_PATH, subject)

    if not os.path.isdir(subject_path):
        continue

    output_subject_path = os.path.join(PROCESSED_PATH, subject)
    os.makedirs(output_subject_path, exist_ok=True)

    for file in os.listdir(subject_path):
        file_path = os.path.join(subject_path, file)

        if file.endswith(".pdf"):
            text = extract_pdf_text(file_path)

        elif file.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        else:
            continue

        output_file = file.replace(".pdf", ".txt")

        with open(os.path.join(output_subject_path, output_file),
                  "w",
                  encoding="utf-8") as f:
            f.write(text)

print("✅ Text extraction completed for all subjects")
