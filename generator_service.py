import random # Added for random topic selection
import torch  # Fix for WinError 1114
import os
import sys

# Ensure scripts directory is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from exam_rule_engine import ExamRuleEngine
from subject_topic_selector import get_unique_subjects, get_topics_by_subject
from rag_retriever import retrieve_context
from prompt_builder import build_prompt
from llm_question_generator import generate_question

class QuestionGenerator:
    def __init__(self):
        self.engine = ExamRuleEngine()

    def generate(self, subject, topics, difficulty):
        # Select one topic randomly if a list is provided
        current_topic = random.choice(topics) if isinstance(topics, list) else topics
        
        rules = self.engine.get_rules(difficulty=difficulty)
        context = retrieve_context(subject, current_topic)
        prompt = build_prompt(context, current_topic, rules)
        result = generate_question(prompt)
        
        return {
            "subject": subject,
            "topic": current_topic,
            "difficulty": rules["difficulty"],
            "variant": rules["variant"],
            "question": result.get("question"),
            "options": result.get("options"),
            "answer": result.get("answer")
        }

    def get_subjects(self):
        return get_unique_subjects()

    def get_topics(self, subject):
        return get_topics_by_subject(subject)
