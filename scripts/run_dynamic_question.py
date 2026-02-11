from exam_rule_engine import ExamRuleEngine
from subject_topic_selector import get_unique_subjects, get_topics_by_subject
from rag_retriever import retrieve_context
from prompt_builder import build_prompt
from llm_question_generator import generate_question

def get_user_choice(options, label):
    print(f"\nSelect {label}:")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    while True:
        try:
            choice = int(input(f"Enter choice (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Invalid choice, try again.")
        except ValueError:
            print("Please enter a number.")

def main():
    # 1. Subject & topic
    subjects = get_unique_subjects()
    if not subjects:
        print("No subjects found in metadata!")
        return

    subject = get_user_choice(subjects, "Subject")
    topics = get_topics_by_subject(subject)
    
    if not topics:
         print(f"No topics found for subject: {subject}")
         return

    topic = get_user_choice(topics, "Topic")

    # 2. Exam rules (Difficulty)
    engine = ExamRuleEngine()
    difficulty = get_user_choice(engine.difficulty_levels, "Difficulty")
    rules = engine.get_rules(difficulty=difficulty)

    # 3. RAG retrieval
    print(f"\nRetrieving context for {subject} - {topic}...")
    context = retrieve_context(subject, topic)

    # 4. Prompt
    prompt = build_prompt(context, topic, rules)

    # 5. LLM generation
    question = generate_question(prompt)

    print("\n===== DYNAMIC EXAM QUESTION =====\n")
    print("Subject:", subject)
    print("Topic:", topic)
    print("Difficulty:", rules["difficulty"])
    print("Variant:", rules["variant"])
    print("\n", question)

if __name__ == "__main__":
    main()