"""
This module runs the Flask application.

It imports the create_app function from the app package and runs the application in debug mode.
"""

from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)