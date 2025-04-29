from flask import render_template, request, jsonify
from flask_login import login_required
from datetime import datetime

from . import health_monitoring_bp

@health_monitoring_bp.route('/metric-charts', methods=['GET'])
@login_required
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
    from app.models import db, LivestockHealth, Livestock
    
    # Get the data from the request
    data = request.get_json()
    print(f"📊 Received livestock health data for ID {livestock_id}: {data}")
    
    if not data:
        print("❌ No data received")
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    # Extract temperature and pulse from the data
    temperature = data.get('temperature')
    pulse = data.get('pulse')
    
    # Check if temperature and pulse are present in the data
    if temperature is None or pulse is None:
        print("❌ Invalid data format")
        return jsonify({"status": "error", "message": "Missing temperature or pulse values"}), 400
    
    # Check if the livestock ID exists in the database
    livestock = Livestock.query.get(livestock_id)
    if not livestock:
        print(f"❌ Livestock with ID {livestock_id} not found")
        return jsonify({"status": "error", "message": "Livestock not found"}), 404

    # Check if the livestock belongs to the farmer
    farmer_id = livestock.farmer_id
    farmer_phone = livestock.farmer.user.phone
    if livestock.farmer_id != farmer_id:
        print(f"❌ Unauthorized access to livestock ID {livestock_id}")
        return jsonify({"status": "error", "message": "Unauthorized access"}), 403
    
    # Save the health data to the database
    health_data = LivestockHealth(
        livestock_id=livestock_id,
        temperature=temperature,
        pulse=pulse
    )
    
    db.session.add(health_data)
    db.session.commit()
    
    # Update shared latest_data for real-time transmission
    from .shared_data import latest_health_data
    latest_health_data.clear()
    latest_health_data.update({
        "livestock_id": livestock_id,
        "temperature": temperature,
        "pulse": pulse,
        "farmer_phone": farmer_phone,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return jsonify({"status": "succes", "message": "Health data saved successfully", "farmer_id": farmer_id}), 200