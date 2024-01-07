# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define fixed question-answer pairs
fixed_responses = {
    "What is TechKnowGram Limited?": "TechKnowGram Limited is a tech company focused on...",
    "Who created you?": "I am created by Sobjanta Limited.",
    "জমির মালিকানা সূত্র কি কি ভাবে হতে পারে / কী কী ভাবে জমির মালিকানা পাওয়া যায় বা পরিবর্তন হয়" :"অনুগ্রহপূর্বক https://eporcha.gov.bd এই ওয়েবসাইট এ প্রবেশ করুন। এরপর নাগরিক কর্নার থেকে খতিয়ান আবেদন অপশনটি নির্বাচন করে খতিয়ান অনলাইন আবেদন ফরম এ গিয়ে ফরমের যাবতীয় তথ্যাদি (বিভাগ, জেলা, উপজেলা, খতিয়ানের ধরন, মৌজা বা জে এল নম্বর, খতিয়ান নং/ দাগ নং/মালিকানা নাম/ পিতা বা স্বামীর নাম) দিয়ে অনুসন্ধানের মাধ্যমে সার্টিফাইড কপিটি সংগ্রহের মাধ্যমে উক্ত বিষয়টি সম্পর্কে জানতে পারবেন। এছাড়াও সঠিক দলিলটি উপজেলা সাব রেজিস্টার অফিস থেকে সংগ্রহ করেও জানতে পারবেন। আপনার বিষয়টির তথ্য অনুসন্ধানের জন্য অনুগ্রহ পূর্বক আপনার জমির সংশ্লিষ্ট বিভাগ, জেলা, উপজেলা, খতিয়ানের ধরণ, মৌজা বা জে এল নম্বর, খতিয়ান নম্বর/ দাগ নম্বর/ মালিকের নাম/ পিতা বা স্বামীর নাম জানিয়ে সহায়তা করুন। বিস্তারিত জানতে ভূমি সেবা হেল্পলাইন ১৬১২২ নম্বরে কল করুন।",
    # Add more predefined questions and answers as needed
}

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/api')
def api():
    user_input = request.args.get('user_message')
    ai_response = generate_response(user_input)
    
    response_json = {
        'ai_response': ai_response,
        'user_message': user_input,
    }
    return jsonify(response_json)

def generate_response(user_input: str) -> str:
    user_message = user_input

    if user_message in fixed_responses:
        return fixed_responses[user_message]
    else:
        return "I'm sorry, I don't have an answer for that question."

@app.route('/process_chat', methods=['POST'])
def process_chat():
    user_message = request.json['user_message']

    if user_message in fixed_responses:
        ai_response = fixed_responses[user_message]
    else:
        ai_response = "I'm sorry, I don't have an answer for that question."

    return jsonify({'response_message': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
