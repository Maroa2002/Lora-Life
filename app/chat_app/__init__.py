"""
    This module initializes the chat application.
    
    It sets up the following:
        - Blueprint for chat application routes
        - Imports the routes for chat application
        
    The blueprint handles rendering the chat application page and getting responses from the chat application.
"""

# Import necessary modules
from flask import Blueprint

# Create a blueprint for the chat application
chat_app_bp = Blueprint(
    'chat_app', 
    __name__, 
    template_folder='templates', 
    static_folder='static'
    )

# Import the routes for the chat application
from . import routes