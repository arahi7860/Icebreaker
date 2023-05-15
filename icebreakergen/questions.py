import json

def load_questions():
    with open('questions.json') as f:
        data = json.load(f)
    return data
