from flask import request
from flask_socketio import join_room
import random
import eventlet

from .extensions import socketio

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
        
        if clients > 0:
            data = {
                "temperature": round(random.uniform(35.5, 41.0), 1),
                "pulse": random.randint(50, 110),
            }
            print(f"📊 Sending data: {data}")
            socketio.emit("livestock_data", data, room="livestock_room")
        else:
            print("🚫 No clients connected. Skipping data transmission.")
            
        eventlet.sleep(5)