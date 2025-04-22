from app.health_monitoring.extensions import socketio
from flask_socketio import emit

@socketio.on("message")
def handle_message(data):
    """
    Handle incoming messages from clients.
    
    This function is triggered when a message is received from a client.
    It emits the message back to all connected clients.
    
    Args:
        data (dict): The data received from the client.
    """
    # Emit the message back to all connected clients
    emit("message", data, broadcast=True)