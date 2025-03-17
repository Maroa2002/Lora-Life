from flask import render_template

from . import health_monitoring_bp

@health_monitoring_bp.route('/metric-charts', methods=['GET'])
def metrics_monitoring():
    """
    Route to display metrics monitoring page.
    
    Returns:
        render_template: HTML template for metrics monitoring page.
    """
    return render_template('metrics_monitoring.html')