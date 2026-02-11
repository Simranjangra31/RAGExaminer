import pickle
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
META_PATH = os.path.join(BASE_DIR, "..", "embeddings", "metadata.pkl")

with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

def select_subject():
    subjects = list(set(m["subject"] for m in metadata))
    return random.choice(subjects)

def select_topic(subject):
    topics = list(set(
        m["topic"] for m in metadata if m["subject"] == subject
    ))
    return random.choice(topics)

def get_unique_subjects():
    return sorted(list(set(m["subject"] for m in metadata)))

def get_topics_by_subject(subject):
    return sorted(list(set(
        m["topic"] for m in metadata if m["subject"] == subject
    )))
