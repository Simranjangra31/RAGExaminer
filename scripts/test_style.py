import urllib.request
import urllib.parse
import json
import http.cookiejar

BASE_URL = "http://127.0.0.1:5000"
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def log(msg):
    print(f"[STYLE-CHECK] {msg}")

def test_style_setup():
    # 1. Examiner sets exam
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
        opener.open(req)
        
        # 2. Login
        data = urllib.parse.urlencode({"prn": "12345"}).encode('utf-8')
        opener.open(f"{BASE_URL}/login", data=data)
        return True
    except Exception as e:
        log(f"Setup Error: {e}")
        return False

def test_button_classes():
    try:
        resp = opener.open(f"{BASE_URL}/test")
        html = resp.read().decode('utf-8')
        
        # Check for new classes
        checks = [
            ("btn btn-primary", "Next Button"),
            ("btn btn-danger", "Submit Button"),
            ("btn-disabled", "Disabled Previous Button")
        ]
        
        all_passed = True
        for cls, name in checks:
            if cls in html:
                log(f"PASS: {name} has class '{cls}'")
            else:
                log(f"FAIL: {name} missing class '{cls}'")
                all_passed = False
                
        # Check if old generic styling is gone (heuristic)
        if "background-color: #e74c3c" not in html: # We removed inline styles
             log("PASS: Inline styles removed")
        else:
             log("FAIL: Inline styles still present")
             all_passed = False
             
        return all_passed

    except Exception as e:
        log(f"Test Error: {e}")
        return False

if __name__ == "__main__":
    if test_style_setup():
        if test_button_classes():
            log("ALL STYLE CHECKS PASSED")
        else:
            log("STYLE CHECKS FAILED")
