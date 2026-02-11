import sys
import os

# Ensure scripts directory is in path
sys.path.append(os.path.dirname(__file__))

from llm_question_generator import generate_question

def test():
    test_prompt = "Generate a very short multiple choice question about photosynthesis."
    print(f"Testing Ollama with prompt: {test_prompt}")
    try:
        response = generate_question(test_prompt)
        print("\nOllama Response:")
        print(response)
        
        if "ERROR" in response:
            print("\nVerification FAILED.")
            sys.exit(1)
        else:
            print("\nVerification SUCCESSFUL.")
    except Exception as e:
        print(f"\nVerification FAILED with exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test()
