def livestock_alert_template(alert_type, value, is_exceeding):
    """
    Generates an SMS template for livestock alerts.

    Args:
        alert_type (str): The type of alert (e.g., "temperature", "humidity").
        value (float): The value that triggered the alert.
        is_exceeding (bool): Indicates if the value is exceeding the threshold.

    Returns:
        str: The formatted SMS message.
    """
    if alert_type == "temperature":
        state = "High" if is_exceeding else "Low"
        return f"Livestock Alert: {state} temperature detected!\nCurrent temperature: {value}°C."
    
    if alert_type == "pulse":
        state = "High" if is_exceeding else "Low"
        return f"Livestock Alert: {state} pulse detected!\nCurrent pulse: {value} BPM."
    
    return "Livestock Alert: Abnormal Health Parameter Detected!"

def otp_template(otp_code):
    """
    Generates an OTP SMS template.
    
    Args:
        otp_code (str): The OTP code to be sent.
    
    Returns:
        str: The formatted OTP message.
    """
    return f"Your OTP code is: {otp_code}. Please do not share this code with anyone."