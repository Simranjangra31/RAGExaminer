import random

class ExamRuleEngine:
    def __init__(self):
        # available difficulty levels
        self.difficulty_levels = ["easy", "medium", "hard"]

        # question variation types
        self.question_variants = [
            "architecture-based",
            "hyperparameter-based",
            "application-based",
            "error-analysis-based"
        ]

    def get_rules(self, difficulty=None, variant=None):
        return {
            "difficulty": difficulty if difficulty else random.choice(self.difficulty_levels),
            "variant": variant if variant else random.choice(self.question_variants)
        }
