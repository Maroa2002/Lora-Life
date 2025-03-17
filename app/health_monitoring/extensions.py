"""
This module initializes the SocketIO extension for the Flask application.

It sets up the following:
- SocketIO instance for real-time communication

The SocketIO instance is used to handle real-time events and communication in the application.
"""

from flask_socketio import SocketIO

# Initialize SocketIO instance
socketio = SocketIO()