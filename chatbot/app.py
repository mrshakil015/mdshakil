# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from datadict import data_dict
from bot_response import fixed_responses
from fuzzywuzzy import fuzz

app = Flask(__name__)

# Define fixed question-answer pairs
keywords = ["জমির দাগ", "জমি অনলাইনে", "অনলাইন", "দাগ"]

def process_keyword(keyword):
    if "জমির দাগ" in keyword:
        return data_dict.get("জমির দাগ", "দুঃখিত! আপনার প্রশ্নের উত্তরটি দিতে পারছি না।")
    elif "জমি অনলাইনে" in keyword:
        return data_dict.get("জমি অনলাইনে", "দুঃখিত! আপনার প্রশ্নের উত্তরটি দিতে পারছি না।")
    elif "অনলাইন" in keyword:
        return data_dict.get("অনলাইন", "দুঃখিত! আপনার প্রশ্নের উত্তরটি দিতে পারছি না।")
    elif "দাগ" in keyword:
        return data_dict.get("দাগ", "দুঃখিত! আপনার প্রশ্নের উত্তরটি দিতে পারছি না।")
    else:
        return "দুঃখিত! আপনার প্রশ্নের উত্তরটি দিতে পারছি না।"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_chat', methods=['POST'])
def process_chat():
    user_message = request.json['user_message']

    if user_message in fixed_responses:
        ai_response = fixed_responses[user_message]
    else:
        similarity_scores = {
            question: fuzz.token_set_ratio(user_message, question)
            for question in fixed_responses.keys()
        }
        most_similar_question = max(similarity_scores, key=similarity_scores.get)
        if similarity_scores[most_similar_question] > 90:
            ai_response = fixed_responses[most_similar_question]
        else:
            match_score_threshold = 70
            matched_keywords = [key for key in keywords if fuzz.partial_ratio(key.lower(), user_message.lower()) >= match_score_threshold]
            result = None  # Initialize result variable
            if matched_keywords:
                matched_keyword = max(matched_keywords, key=lambda key: fuzz.partial_ratio(key.lower(), user_message.lower()))
                result = process_keyword(matched_keyword.lower())  # Update result variable
            if isinstance(result, list):
                formatted_list = "\n".join(result)
                ai_response = f"আপনার প্রশ্নটির দ্বারা সমস্যাটি বুঝতে পারছি না, আপনি কি নিম্নক্ত প্রশ্নগুলো বুঝাতে চাচ্ছেন?\n{formatted_list}"
            else:
                ai_response = f"দুঃখিত! আপনার প্রশ্নের উত্তরটি দিতে পারছি না।"

    return jsonify({'response_message': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
