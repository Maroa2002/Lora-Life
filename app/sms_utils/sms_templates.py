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

def appointment_booked_farmer_template(vet_name, date_time):
    """
    SMS template for notifying the farmer when they book an appointment.
    
    Args:
        vet_name (str): The vet's name.
        date_time (str): The date and time of the appointment.
    
    Returns:
        str: SMS content for the farmer.
    """
    return (
        f"Appointment Confirmed!\n"
        f"You have booked an appointment with Dr. {vet_name} on {date_time}."
    )

def appointment_cancelled_farmer_template(vet_name, date_time):
    """
    SMS template for notifying the farmer when their appointment is cancelled.
    
    Args:
        vet_name (str): The vet's name.
        date_time (str): The cancelled appointment's date and time.
    
    Returns:
        str: SMS content for the farmer.
    """
    return (
        f"Appointment Cancelled.\n"
        f"Your appointment with Dr. {vet_name} on {date_time} has been cancelled. Please reschedule if needed."
    )
    
def appointment_notification_vet_template(farmer_name, date_time, notes):
    """
    SMS template for notifying the vet of a new appointment including notes.
    
    Args:
        farmer_name (str): The farmer's name.
        date_time (str): The date and time of the appointment.
        notes (str): Notes provided by the farmer.
    
    Returns:
        str: SMS content for the vet.
    """
    return (
        f"New Appointment!\n"
        f"{farmer_name} has booked an appointment with you on {date_time}.\n\n"
        f"Issue: {notes if notes else 'No additional notes provided.'}"
    )
