from flask import request
from flask_socketio import join_room
import eventlet

from .extensions import socketio
from .shared_data import latest_health_data

# Thresholds
TEMP_THRESHOLD_HIGH = 40.0
TEMP_THRESHOLD_LOW = 36.0
PULSE_THRESHOLD_HIGH = 100
PULSE_THRESHOLD_LOW = 60

@socketio.on('connect')
def handle_connect():
    """Handle Client Connection"""
    sid = request.sid
    print(f"✅ Client connected with session_id {sid}!")
    
    join_room("livestock_room")
    print(f"🔹 Client {sid} joined 'livestock_room'")
    
    socketio.start_background_task(send_livestock_data)


def send_livestock_data():
    print("🐄 Sending Livestock Data...")
    
    while True:
        clients = len(list(socketio.server.manager.get_participants('/', 'livestock_room')))
        print(f"👥 Connected clients: {clients}")
        
        if clients > 0 and latest_health_data:
            print(f"📊 Latest data: {latest_health_data}")
            print(f"📊 Sending data: {latest_health_data}")
            
            # Check if latest_health_data exceeds thresholds and send alerts
            if latest_health_data["temperature"] > TEMP_THRESHOLD_HIGH:
                socketio.emit("livestock_alert", {"message": "High temperature detected!", "type": "temperature", "value": latest_health_data["temperature"], "isExceeding": True}, room="livestock_room")
            elif latest_health_data["temperature"] < TEMP_THRESHOLD_LOW:
                socketio.emit("livestock_alert", {"message": "Low temperature detected!", "type": "temperature", "value": latest_health_data["temperature"], "isExceeding": False}, room="livestock_room")
            
            if latest_health_data["pulse"] > PULSE_THRESHOLD_HIGH:
                socketio.emit("livestock_alert", {"message": "High pulse rate detected!", "type": "pulse", "value": latest_health_data["pulse"], "isExceeding": True}, room="livestock_room")
            elif latest_health_data["pulse"] < PULSE_THRESHOLD_LOW:
                socketio.emit("livestock_alert", {"message": "Low pulse rate detected!", "type": "pulse", "value": latest_health_data["pulse"], "isExceeding": False}, room="livestock_room")
            
            socketio.emit("livestock_data", latest_health_data, room="livestock_room")
        else:
            print("🚫 No clients connected. Skipping data transmission.")
            
        eventlet.sleep(10)