import urllib.request
import urllib.parse
import json
import http.cookiejar
import re

BASE_URL = "http://127.0.0.1:5000"
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def log(msg):
    print(f"[TEST] {msg}")

def check_content(html, text, error_msg):
    if text not in html:
        log(f"FAIL: {error_msg}")
        return False
    return True

def test_setup():
    # 1. Examiner sets exam
    log("Setting up exam...")
    try:
        payload = {
            "subject": "Physics",
            "topics": ["Kinematics"],
            "difficulty": "medium"
        }
        req = urllib.request.Request(
            f"{BASE_URL}/api/set_exam", 
            data=json.dumps(payload).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}, 
            method='POST'
        )
        resp = opener.open(req)
        if resp.status != 200:
            log("Failed to set exam")
            return False
            
        # 2. Login
        log("Logging in student...")
        data = urllib.parse.urlencode({"prn": "12345"}).encode('utf-8')
        opener.open(f"{BASE_URL}/login", data=data) 
        
        return True
    except Exception as e:
        log(f"Setup Error: {e}")
        return False

def test_navigation():
    try:
        # Q1
        log("Getting Question 1...")
        resp = opener.open(f"{BASE_URL}/test")
        q1_html = resp.read().decode('utf-8')
        
        if "Question 1" not in q1_html:
            log("Failed to find 'Question 1' label")
            return False
        if 'disabled' not in q1_html and 'Previous' in q1_html: 
             # Check previous button state. It should be disabled or styled as such generally,
             # but we implemented `<button disabled` for prev.
             if '<button disabled' not in q1_html:
                  log("Previous button should be disabled for Q1")
        
        q1_text_match = re.search(r'line-height: 1.6; white-space: pre-wrap;">(.*?)</div>', q1_html, re.DOTALL)
        q1_text = q1_text_match.group(1).strip() if q1_text_match else "UNKNOWN_Q1"
        log(f"Q1 Text: {q1_text[:30]}...")

        # Next -> Q2
        log("Clicking Next for Question 2...")
        resp = opener.open(f"{BASE_URL}/test?action=next")
        q2_html = resp.read().decode('utf-8')
        
        if "Question 2" not in q2_html:
            log("Failed to find 'Question 2' label")
            return False
            
        q2_text_match = re.search(r'line-height: 1.6; white-space: pre-wrap;">(.*?)</div>', q2_html, re.DOTALL)
        q2_text = q2_text_match.group(1).strip() if q2_text_match else "UNKNOWN_Q2"
        log(f"Q2 Text: {q2_text[:30]}...")
        
        if q1_text == q2_text:
             log("WARNING: Q1 and Q2 text are identical. Maybe random chance or logic error.")

        # Prev -> Q1
        log("Clicking Previous for Question 1 (History check)...")
        resp = opener.open(f"{BASE_URL}/test?action=prev")
        q1_again_html = resp.read().decode('utf-8')
        
        if "Question 1" not in q1_again_html:
            log("Failed to go back to Question 1")
            return False
            
        q1_again_text_match = re.search(r'line-height: 1.6; white-space: pre-wrap;">(.*?)</div>', q1_again_html, re.DOTALL)
        q1_again_text = q1_again_text_match.group(1).strip() if q1_again_text_match else "UNKNOWN_Q1_AGAIN"
        
        if q1_text != q1_again_text:
            log("FAIL: History mismatch. Q1 content changed when revisiting.")
            log(f"Original: {q1_text[:30]}")
            log(f"Revisit:  {q1_again_text[:30]}")
            return False
        else:
            log("History check passed: Q1 content persisted.")

        # Submit
        log("Submitting exam...")
        resp = opener.open(f"{BASE_URL}/submit")
        if "Waiting for Exam" in resp.read().decode('utf-8') or resp.url.endswith("/"): 
             # Redirects to / or renders waiting template.
             log("Submission successful, returned to waiting/login area.")
             return True
        else:
             log("Submission might have failed, check logic.")
             return False

    except Exception as e:
        log(f"Navigation Test Error: {e}")
        return False

if __name__ == "__main__":
    if test_setup():
        if test_navigation():
            log("ALL TESTS PASSED")
        else:
            log("TESTS FAILED")
    else:
        log("SETUP FAILED")
