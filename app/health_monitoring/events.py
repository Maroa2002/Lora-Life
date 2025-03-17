from .extensions import socketio

@socketio.on('connect')
def handle_connect():
    """Handle Client Connection"""
    print("✅ Client connected!")