from flask import render_template, request, jsonify
from app.models import db, LivestockHealth

from . import health_monitoring_bp

@health_monitoring_bp.route('/metric-charts', methods=['GET'])
def metrics_monitoring():
    """
    Route to display metrics monitoring page.
    
    Returns:
        render_template: HTML template for metrics monitoring page.
    """
    return render_template('metrics_monitoring.html')

@health_monitoring_bp.route('/livestock-health-data/<int:livestock_id>', methods=['POST'])
def receive_health_data(livestock_id):
    """
    Endpoint to receive livestock health data from LoRa/ESP32 devices.
    
    Returns:
        str: Success message.
    """
    data = request.get_json()
    print(f"📊 Received livestock health data for ID {livestock_id}: {data}")
    
    if not data:
        print("❌ No data received")
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    temperature = data.get('temperature')
    pulse = data.get('pulse')
    
    if temperature is None or pulse is None:
        print("❌ Invalid data format")
        return jsonify({"status": "error", "message": "Missing temperature or pulse values"}), 400
    
    livestock = LivestockHealth.query.get(livestock_id)
    if not livestock:
        print(f"❌ Livestock with ID {livestock_id} not found")
        return jsonify({"status": "error", "message": "Livestock not found"}), 404

    farmer_id = livestock.farmer_id
    if livestock.farmer_id != farmer_id:
        print(f"❌ Unauthorized access to livestock ID {livestock_id}")
        return jsonify({"status": "error", "message": "Unauthorized access"}), 403
    
    health_data = LivestockHealth(
        livestock_id=livestock_id,
        temperature=temperature,
        pulse=pulse
    )
    
    db.session.add(health_data)
    db.session.commit()
    
    return jsonify({"status": "succes", "message": "Health data saved successfully", "farmer_id": farmer_id}), 200
    
    # from .shared_data import latest_data
    # data = request.json
    
    # if 'temperature' in data and 'pulse' in data:
    #     latest_data.clear()
    #     latest_data.update(data)
        
    #     print(f"📊 Received livestock data: {latest_data}")
        
    #     return jsonify({"status": "success", "message": "Data received successfully"}), 200
    # else:
    #     print("❌ Invalid data received")
    #     return jsonify({"status": "error", "message": "Invalid data"}), 400