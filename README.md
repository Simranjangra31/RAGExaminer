DYNAMIC QUESTION GENERATION RAG SYSTEM

This is a project I built to help automate the process of creating exam questions. It uses a Retrieval-Augmented Generation (RAG) approach, which means it looks at actual study materials like PDFs or text files to create questions that are relevant to the topic. It uses a local AI model called Qwen to make sure everything runs locally without needing an expensive API.

PROJECT STRUCTURE

I organized the project so that it is easy to manage the study materials:
- data/raw: This is where you put your folders for different subjects. Inside those folders, you can put your PDFs or TXT files.
- scripts: This contains all the code for extracting text, chunking it into smaller pieces, and creating the AI search index.
- templates: These are the HTML pages for the website interface.
- static: Contains the CSS files for the design.

HOW TO SET IT UP

First, make sure you have Python installed. You should also have Ollama installed on your machine to run the AI model.

1. Create a virtual environment and install the requirements:
   pip install -r requirements.txt

2. Make sure Ollama is running and has the qwen:0.5b model:
   ollama pull qwen:0.5b

3. Process your data:
   If you added new files to the data/raw folder, run these scripts in order:
   - python scripts/1_text_extraction.py
   - python scripts/chunking.py
   - python scripts/4_embedding_and_storage.py

4. Start the application:
   python app.py

HOW TO USE THE SYSTEM

- Dashboard: Go to http://127.0.0.1:5000/ to see the main page.
- Examiner Section: From here, you can choose a subject and select the topics (which are just the files you uploaded) using the checkboxes.
- Student Section: Once the examiner publishes the exam, students can login using their PRN number to start the test.

The system will generate multiple-choice questions dynamically based on the documents provided. It is designed to run even on computers without a lot of RAM by using a very small model and efficient memory management.

TECHNICAL DETAILS

- Framework: Flask for the web server.
- AI Search: FAISS for fast text retrieval.
- LLM: Qwen 0.5B via Ollama.
- Embeddings: Sentence-Transformers (all-MiniLM-L6-v2).
