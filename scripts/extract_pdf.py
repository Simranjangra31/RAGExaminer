import fitz

doc = fitz.open(r'C:\Users\DELL\Downloads\Report-Format.pdf')
for i, page in enumerate(doc):
    print(f"--- Page {i+1} ---")
    print(page.get_text())
