"""
This module initializes the farmer blueprint for the Flask application.

It sets up the following:
- Blueprint for farmer routes
- Imports the routes for farmer

The blueprint handles functionalities related to farmers, such as viewing and updating profiles, viewing available vets, and booking appointments.
"""

from flask import Blueprint

# Create a blueprint for farmer
farmer_bp = Blueprint('farmer', __name__, template_folder='templates')

# Import the routes for farmer
from . import routes