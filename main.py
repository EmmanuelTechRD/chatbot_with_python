import re
import random
import json

# Cargando respuestas desde un archivo JSON:
def load_responses(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

responses_data = load_responses('responses.json')

def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob = {}

    # Agregando respuestas dinámicamente desde el archivo JSON:
    for response_data in responses_data['responses']:
        response_text = response_data['response']
        list_of_words = response_data['list_of_words']
        single_response = response_data['single_response']
        required_words = response_data['required_words']
        
        highest_prob[response_text] = message_probability(
            message, list_of_words, single_response, required_words
        )

    best_match = max(highest_prob, key=highest_prob.get)
    # print(highest_prob)

    return unknown() if highest_prob[best_match] < 1 else best_match

def unknown():
    response = ['¿Puedes decirlo de nuevo?', 'No estoy seguro de lo que quieres...', 'Búscalo en google a ver que tal.'][random.randrange(3)]
    return response

while True:
    print("Bot: " + get_response(input('You: ')))