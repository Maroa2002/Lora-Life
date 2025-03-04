"""
This module defines the routes for chatbot-related functionalities in the Flask application.

It includes the following routes:
- Render the chatbot page
- Get a response from the chatbot

Functions:
- chatbot(): Renders the chatbot page.
- get_response(): Gets a response from the chatbot based on user input.
"""

from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
from langdetect import detect
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Load the OpenAI API key from the environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a blueprint
chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/', methods=['GET'])
def chatbot():
    """
    Route to render the chatbot page.

    Returns:
        Response: Rendered HTML template for the chatbot page.
    """
    return render_template('chatbot.html')


@chatbot_bp.route('/get_response', methods=['POST'])
def get_response():
    """
    Route to get a response from the chatbot.

    Processes the user message, detects the language, and gets a response from the OpenAI API.

    Returns:
        Response: JSON response containing the chatbot's reply and detected language.
    """
    data = request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        # Detect language
        detected_lang = detect(user_message)
        
        # Modify system message based on language
        if detected_lang == "sw":
            system_message = "Wewe ni mtaalamu wa mifugo na unatoa ushauri kuhusu afya ya wanyama."
        else:
            system_message = "You are a helpful veterinary assistant providing insights on animal health."
        
        # Get response from OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )
        response = completion.choices[0].message.content
        
        return jsonify({"reply": response, "language": detected_lang}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

