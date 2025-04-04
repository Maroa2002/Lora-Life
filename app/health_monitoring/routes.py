from flask import render_template, request, jsonify

from . import health_monitoring_bp

@health_monitoring_bp.route('/metric-charts', methods=['GET'])
def metrics_monitoring():
    """
    Route to display metrics monitoring page.
    
    Returns:
        render_template: HTML template for metrics monitoring page.
    """
    return render_template('metrics_monitoring.html')

@health_monitoring_bp.route('/livestock-data', methods=['POST'])
def livestock_data():
    """
    Route to receive and store livestock data.
    
    Returns:
        str: Success message.
    """
    from .shared_data import latest_data
    data = request.json
    
    if 'temperature' in data and 'pulse' in data:
        latest_data.clear()
        latest_data.update(data)
        
        print(f"📊 Received livestock data: {latest_data}")
        
        return jsonify({"status": "success", "message": "Data received successfully"}), 200
    else:
        print("❌ Invalid data received")
        return jsonify({"status": "error", "message": "Invalid data"}), 400