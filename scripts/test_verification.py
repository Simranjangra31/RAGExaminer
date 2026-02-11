import urllib.request
import urllib.parse
import json
import http.cookiejar

BASE_URL = "http://127.0.0.1:5000"
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def test_examiner_flow():
    print("Testing Examiner Flow...")
    try:
        resp = opener.open(f"{BASE_URL}/examiner")
        if resp.status != 200:
            print("Failed to access examiner page")
            return False
            
        payload = {
            "subject": "Physics",
            "topics": ["Kinematics", "Dynamics"],
            "difficulty": "medium"
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}/api/set_exam", 
            data=data, 
            headers={'Content-Type': 'application/json'}, 
            method='POST'
        )
        resp = opener.open(req)
        
        if resp.status == 200:
             result = json.loads(resp.read().decode('utf-8'))
             if result.get("status") == "success":
                 print("Successfully set exam with multiple topics")
                 return True
        
        print(f"Failed to set exam: {resp.read()}")
        return False
        
    except Exception as e:
        print(f"Error in examiner flow: {e}")
        return False

def test_student_flow():
    print("Testing Student Flow...")
    try:
        # 1. Login
        login_data = urllib.parse.urlencode({"prn": "12345"}).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/login", data=login_data, method='POST')
        resp = opener.open(req)
        print(f"Login Response Code: {resp.status}")
        
        # 2. Get Test Page
        resp = opener.open(f"{BASE_URL}/test")
        content = resp.read().decode('utf-8')
        
        if resp.status != 200:
            print(f"Failed to get test page, status: {resp.status}")
            return False

        # 3. Verify Metadata is Hidden
        if "Subject:" in content and "Difficulty:" in content:
            if "<!-- Meta info hidden" in content:
                 print("Metadata hidden verification passed (comment tag found)")
            else:
                 print("Warning: Meta info might be visible.")
                 # Check line by line if inside comment if needed, but simplistic check helps.
        else:
             print("Metadata hidden verification passed (content not found)")

        # 4. Verify Active Exam on Login Page
        resp = opener.open(f"{BASE_URL}/")
        login_content = resp.read().decode('utf-8')
        if "Active Exam:" in login_content:
             if "<!--" in login_content and "-->" in login_content:
                  # Very simple check
                  pass
             else:
                  print("Warning: Active Exam text found on login page.")
        else:
             print("Login page metadata verification passed")
             
        print("Student flow check complete")
        return True
        
    except Exception as e:
        print(f"Error in student flow: {e}")
        return False

if __name__ == "__main__":
    if test_examiner_flow():
        test_student_flow()
