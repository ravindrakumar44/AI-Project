from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
from flask_cors import CORS 
load_dotenv()

app = Flask(_name_)
CORS(app)
# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        chat_history = data.get('history', [])

        # Format history for Gemini
        formatted_history = []
        for msg in chat_history:
            if msg['sender'] == 'user':
                formatted_history.append({'role': 'user', 'parts': [msg['message']]})
            else:
                formatted_history.append({'role': 'model', 'parts': [msg['message']]})

        # Start chat with history
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(user_message)
        
        return jsonify({
            'response': response.text,
            'history': chat_history + [
                {'sender': 'user', 'message': user_message},
                {'sender': 'bot', 'message': response.text}
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True, port=5000)
