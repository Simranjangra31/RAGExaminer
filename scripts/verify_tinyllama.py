import json
import urllib.request
import urllib.error

def test_tinyllama():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "tinyllama",
        "prompt": "Say 'Working' if you can hear me.",
        "stream": False
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    
    print("Connecting to Ollama...")
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\nOllama Output:")
            print(result.get('response', ''))
            print("\nOllama is working correctly!")
    except urllib.error.URLError as e:
        print(f"\nConnection error: {e}")
        if hasattr(e, 'read'):
            print(f"Server response: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    test_tinyllama()
