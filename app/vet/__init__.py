"""
This module initializes the vet blueprint for the Flask application.

It sets up the following:
- Blueprint for vet routes
- Imports the routes for vet

The blueprint handles functionalities related to vets, such as managing availability slots, viewing appointments, and managing appointments.
"""

from flask import Blueprint

# Create a blueprint for vet
vet_bp = Blueprint('vet', __name__, template_folder='templates')

# Import the routes for vet
from . import routes