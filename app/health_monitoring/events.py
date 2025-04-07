from flask import request
from flask_socketio import join_room
import eventlet

from app.sms_utils.sms_service import send_sms
from app.sms_utils.sms_templates import livestock_alert_template

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
                send_sms(
                    phone_number="254740830422",
                    message=livestock_alert_template("temperature", latest_health_data["temperature"], True),
                    ref_id="livestock_alert"
                ) 
                socketio.emit(
                    "livestock_alert", 
                    {
                        "message": "High temperature detected!", 
                        "type": "temperature", 
                        "value": latest_health_data["temperature"], 
                        "isExceeding": True
                    }, 
                    room="livestock_room")
            elif latest_health_data["temperature"] < TEMP_THRESHOLD_LOW:
                send_sms(
                    phone_number="254740830422",
                    message=livestock_alert_template("temperature", latest_health_data["temperature"], False),
                    ref_id="livestock_alert"
                )
                socketio.emit(
                    "livestock_alert", 
                    {
                        "message": "Low temperature detected!", 
                        "type": "temperature", 
                        "value": latest_health_data["temperature"], 
                        "isExceeding": False
                        }, 
                    room="livestock_room"
                    )
            
            if latest_health_data["pulse"] > PULSE_THRESHOLD_HIGH:
                send_sms(
                    phone_number="254740830422",
                    message=livestock_alert_template("pulse", latest_health_data["pulse"], True),
                    ref_id="livestock_alert"
                )
                socketio.emit(
                    "livestock_alert", 
                    {
                        "message": "High pulse rate detected!", 
                        "type": "pulse", 
                        "value": latest_health_data["pulse"], 
                        "isExceeding": True
                        }, 
                    room="livestock_room"
                    )
            elif latest_health_data["pulse"] < PULSE_THRESHOLD_LOW:
                send_sms(
                    phone_number="254740830422",
                    message=livestock_alert_template("pulse", latest_health_data["pulse"], False),
                    ref_id="livestock_alert"
                )
                socketio.emit(
                    "livestock_alert", 
                    {
                        "message": "Low pulse rate detected!", 
                        "type": "pulse", 
                        "value": latest_health_data["pulse"], 
                        "isExceeding": False
                        }, 
                    room="livestock_room"
                    )
            
            socketio.emit("livestock_data", latest_health_data, room="livestock_room")
        else:
            print("🚫 No clients connected. Skipping data transmission.")
            
        eventlet.sleep(10)