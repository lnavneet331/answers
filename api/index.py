from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

def get_gemini_response(input_text):
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(input_text)
        
        return response.text
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Please provide a query parameter 'q'"}), 400
    
    response = get_gemini_response(query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)