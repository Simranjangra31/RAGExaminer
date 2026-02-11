import json
import urllib.request
import urllib.error

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen:0.5b" # Extremely lightweight model for resource-constrained systems

def call_ollama(prompt, model=DEFAULT_MODEL):
    """
    Calls the local Ollama API to generate a response.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_gpu": 0
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        OLLAMA_API_URL, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('response', '').strip()
            
    except urllib.error.URLError as e:
        # Check if connection refused (machine not listening)
        if hasattr(e, 'reason') and "No connection" in str(e.reason):
             return (
                 "ERROR: Could not connect to Ollama.\n\n"
                 "Please ensure Ollama is installed and running.\n"
                 "Run 'ollama serve' in a terminal."
             )
        # Check if 404 (model not found likely)
        if hasattr(e, 'code') and e.code == 404:
             return (
                 f"ERROR: Model '{model}' not found.\n\n"
                 f"Please run 'ollama pull {model}' to download it."
             )
        return f"ERROR: Ollama API call failed: {e}"
    except Exception as e:
        return f"ERROR: An unexpected error occurred: {e}"

def generate_question(prompt):
    """
    Generates an exam question based on the prompt.
    Parses JSON output for MCQ structure.
    """
    response = call_ollama(prompt)
    
    if "ERROR:" in response:
        # Robust fallback for resource-constrained systems
        mock_question = (
            "DYNAMIC QUESTION (FALLBACK MODE):\n\n"
            "Explain the fundamental principles and real-world applications of the topic based on the provided context.\n\n"
            "Note: This question was generated in fallback mode because the local LLM (Ollama) "
            "encountered a system memory error."
        )
        return {
            "question": f"{response}\n\n---\n\n{mock_question}",
            "options": ["N/A", "N/A", "N/A", "N/A"],
            "answer": "N/A"
        }

    try:
        # Try to find JSON in the response (useful if LLM adds preamble)
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return {
                "question": data.get("question", "No question generated"),
                "options": data.get("options", ["A", "B", "C", "D"]),
                "answer": data.get("answer", "Unknown")
            }
    except Exception:
        pass

    # Basic fallback if JSON parsing fails but we have text
    return {
        "question": response,
        "options": ["A", "B", "C", "D"],
        "answer": "N/A"
    }
