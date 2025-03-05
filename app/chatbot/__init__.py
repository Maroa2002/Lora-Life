"""
This module initializes the chatbot blueprint for the Flask application.

It sets up the following:
- Blueprint for chatbot routes
- Imports the routes for chatbot

The blueprint handles rendering the chatbot page and getting responses from the chatbot.
"""

from flask import Blueprint

# Create a blueprint for chatbot
chatbot_bp = Blueprint('chatbot', __name__, template_folder='templates')

# Import the routes for chatbot
from . import routes