"""
This module initializes the health monitoring blueprint for the Flask application.

It sets up the following:
- Blueprint for health monitoring routes
- Imports the routes for health monitoring

The blueprint handles functionalities related to health monitoring of livestock.
"""

from flask import Blueprint

# Create a blueprint for health monitoring
health_monitoring_bp = Blueprint('health_monitoring', __name__, template_folder='templates')

# Import the routes for health monitoring
from . import routes