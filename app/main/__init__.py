"""
This module initializes the main blueprint for the Flask application.

It sets up the following:
- Blueprint for main routes
- Imports the routes for main

The blueprint handles the main functionalities of the application, such as rendering the home page and handling contact form submissions.
"""

from flask import Blueprint

# Create a blueprint for main
main_bp = Blueprint('main', __name__, template_folder='templates')

# Import the routes for main
from . import routes