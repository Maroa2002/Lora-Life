"""
This module initializes the authentication blueprint for the Flask application.

It sets up the following:
- Blueprint for authentication routes
- Imports the routes for authentication

The blueprint handles user login, registration, and logout functionalities.
"""

from flask import Blueprint

# Create a blueprint for authentication
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Import the routes for authentication
from . import routes