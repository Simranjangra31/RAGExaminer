def build_prompt(context, topic, rules):
    joined_context = "\n".join(context)

    prompt = f"""
You are an intelligent exam question generator. 
Generate ONE multiple-choice question (MCQ) based on the context below.

Topic: {topic}
Difficulty: {rules['difficulty']}

Context:
{joined_context}

STRICT OUTPUT FORMAT (JSON ONLY):
{{
  "question": "The question text",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": "The correct option text exactly as it appears in the options list"
}}
"""
    return prompt
