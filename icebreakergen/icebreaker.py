# import json
# import random

# with open('questions.json', 'r') as f:
#     questions = json.load(f)

# questions_dict = {category['name']: category['questions'] for category in questions['categories']}

# random_category = random.choice(list(questions_dict.keys()))
# random_question = random.choice(questions_dict[random_category])

# print(f"Category: {random_category}")
# print(f"Question: {random_question}")

# import json
# import random

# def get_random_question():
#     with open('questions.json', 'r') as f:
#         questions = json.load(f)

#     questions_dict = {category['name']: category['questions'] for category in questions['categories']}

#     random_category = random.choice(list(questions_dict.keys()))
#     random_question = random.choice(questions_dict[random_category])

#     return f"Category: {random_category}\nQuestion: {random_question}"

import json
import random

def get_random_question():
    with open('questions.json', 'r') as f:
        questions = json.load(f)

    questions_dict = {category['name']: category['questions'] for category in questions['categories']}

    random_category = random.choice(list(questions_dict.keys()))
    random_question = random.choice(questions_dict[random_category])

    return {
        'category': random_category,
        'question': random_question
    }

print(get_random_question())
