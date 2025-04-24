import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = "mgm.engineeringtie847@gmail.com"
EMAIL_PASSWORD = "GMAIL_PASSWORd"

msg = EmailMessage()
msg["Subject"] = "Test Email"
msg["From"] = EMAIL_ADDRESS
msg["To"] = "matikomaroa12@gmail.com"
msg.set_content("This is a test from the server.")

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("Email sent successfully")
except Exception as e:
    print("Error:", e)
