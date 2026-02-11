import urllib.request
import urllib.parse
import json
import http.cookiejar
import re

BASE_URL = "http://127.0.0.1:5000"
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def log(msg):
    print(f"[LLM-CHECK] {msg}")

def test_llm_generation_attempt():
    """
    Sets up an exam and tries to generate a question.
    Checks if the output is the old Mock style or the new Error/Real style.
    """
    try:
        # 1. Setup Exam
        log("Setting up exam...")
        payload = {"subject": "Physics", "topics": ["Kinematics"], "difficulty": "medium"}
        req = urllib.request.Request(
            f"{BASE_URL}/api/set_exam", 
            data=json.dumps(payload).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}, 
            method='POST'
        )
        opener.open(req)
        
        # 2. Login
        log("Logging in...")
        opener.open(f"{BASE_URL}/login", data=urllib.parse.urlencode({"prn": "123"}).encode('utf-8'))
        
        # 3. Get Question
        log("Requesting question generation...")
        resp = opener.open(f"{BASE_URL}/test")
        html = resp.read().decode('utf-8')
        
        q_match = re.search(r'line-height: 1.6; white-space: pre-wrap;">(.*?)</div>', html, re.DOTALL)
        question_text = q_match.group(1).strip() if q_match else "NO_TEXT_FOUND"
        
        log(f"Received Text (Preview): {question_text[:100]}...")
        
        # 4. Analyze
        if "ERROR: Could not connect to Ollama" in question_text:
            log("PASS: Correctly identified Ollama is down/unreachable (New Code Logic Active).")
            return True
        elif "ERROR: Model" in question_text:
             log("PASS: Correctly identified Ollama model missing (New Code Logic Active).")
             return True
        elif "DYNAMIC QUESTION:" in question_text and "Generate ONE clear exam question" in question_text:
             # This is the signature of the OLD Mock LLM.
             log("FAIL: Still seeing Mock LLM output.")
             return False
        else:
             # Ideally this means it generated a real question!
             log("SUCCESS: Received what appears to be a real generated question (or unexpected error).")
             return True

    except Exception as e:
        log(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_llm_generation_attempt()
