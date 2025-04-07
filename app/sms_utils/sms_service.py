import requests
import os
from dotenv import load_dotenv

load_dotenv()

# API Endpoint and Key
API_URL = os.getenv('SEND_SMS_ENDPOINT')
API_KEY = os.getenv('TIARA_API_KEY')

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def send_sms(phone_number: str, message: str, ref_id: str = "defaultRefId"):
    """
    Send an SMS using the Tiara SMS service.

    :param phone_number: The recipient's phone number.
    :param message: The message to be sent.
    :param ref_id: A reference ID for tracking the message.
    :return: Response from the SMS service.
    """
    sms_data = {
        "from": "TIARACONECT",
        "to": phone_number,
        "message": message,
        "redId": ref_id,
        "messageType": "1"
    }
    
    try:
        response = requests.post(API_URL, json=sms_data, headers=HEADERS)
        
        if response.status_code == 200:
            print(f"✅ SMS sent to {phone_number}")
            return response.json()
        else:
            print(f"❌ Failed to send SMS to {phone_number}: {response.text}")
            return {"error": response.text}
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return {"error": str(e)}
