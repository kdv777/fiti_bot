import json
from fuzzywuzzy import fuzz
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

with open("faq.json", encoding='utf-8') as json_file:
    faq = json.load(json_file)


def classify_question(text):
    text = ' '.join(morph.parse(word)[0].normal_form for word in text.split())
    questions = list(faq.keys())
    scores = list()

    for question in questions:
        norm_question = ' '.join(morph.parse(word)[0].normal_form for word in question.split())
        scores.append(fuzz.token_sort_ratio(norm_question.lower(), text.lower()))

    answer = faq[questions[scores.index(max(scores))]]

    return answer
