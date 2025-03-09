"""
This module provides utility functions for the Flask application.

Functions:
- allowed_file(filename): Checks if a file is allowed based on its extension.
- send_email(recipient_email, msg): Sends an email using SMTP.
"""

from flask import current_app
from werkzeug.utils import secure_filename
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch email credentials from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """
    Check if a file is allowed based on its extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file is allowed, False otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, upload_folder):
    """
    Save a file to a specified folder.

    Args:
        file (FileStorage): The file to save.
        folder (str): The folder to save the file in.

    Returns:
        str: The filename of the saved file.
    """
    if file and allowed_file(file.filename):
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None

def send_email(recipient_email, msg):
    """
    Send an email using SMTP.

    Args:
        recipient_email (str): The email address of the recipient.
        msg (str): The message to send.

    Raises:
        smtplib.SMTPException: If there is an error sending the email.
        Exception: If there is a general error.
    """
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, recipient_email, msg=msg)
        server.quit()
    except smtplib.SMTPException as e:
        print('Error sending email: {}'.format(e))
    except Exception as e:
        print('Error: {}'.format(e))
        

KENYA_COUNTIES = [
    ('', 'Select County'),  # Default option
    ('baringo', 'Baringo'),
    ('bomet', 'Bomet'),
    ('bungoma', 'Bungoma'),
    ('busia', 'Busia'),
    ('elgeyo_marakwet', 'Elgeyo Marakwet'),
    ('embu', 'Embu'),
    ('garissa', 'Garissa'),
    ('homa_bay', 'Homa Bay'),
    ('isiolo', 'Isiolo'),
    ('kajiado', 'Kajiado'),
    ('kakamega', 'Kakamega'),
    ('kericho', 'Kericho'),
    ('kiambu', 'Kiambu'),
    ('kilifi', 'Kilifi'),
    ('kirinyaga', 'Kirinyaga'),
    ('kisii', 'Kisii'),
    ('kisumu', 'Kisumu'),
    ('kitui', 'Kitui'),
    ('kwale', 'Kwale'),
    ('laikipia', 'Laikipia'),
    ('lamu', 'Lamu'),
    ('machakos', 'Machakos'),
    ('makueni', 'Makueni'),
    ('mandera', 'Mandera'),
    ('marsabit', 'Marsabit'),
    ('meru', 'Meru'),
    ('migori', 'Migori'),
    ('mungoma', 'Mungoma'),
    ('murang_a', 'Murang’a'),
    ('nairobi', 'Nairobi'),
    ('nakuru', 'Nakuru'),
    ('nandi', 'Nandi'),
    ('narok', 'Narok'),
    ('nyamira', 'Nyamira'),
    ('nyandarua', 'Nyandarua'),
    ('nyeri', 'Nyeri'),
    ('samburu', 'Samburu'),
    ('siaya', 'Siaya'),
    ('taita_taveta', 'Taita Taveta'),
    ('tana_river', 'Tana River'),
    ('tharaka_nithi', 'Tharaka Nithi'),
    ('trans_nzoia', 'Trans Nzoia'),
    ('turkana', 'Turkana'),
    ('uasin_gishu', 'Uasin Gishu'),
    ('vihiga', 'Vihiga'),
    ('wajir', 'Wajir'),
    ('west_pokot', 'West Pokot')
]

COUNTY_TOWNS = {
    "baringo": ["Kabarnet", "Eldama Ravine", "Mogotio", "Marigat", "Ravine"],
    "bomet": ["Bomet Town", "Sotik", "Kaplong", "Mulot", "Longisa"],
    "bungoma": ["Bungoma Town", "Webuye", "Kimilili", "Chwele", "Sirisia"],
    "busia": ["Busia Town", "Malaba", "Port Victoria", "Nambale", "Amukura"],
    "elgeyo_marakwet": ["Iten", "Kapsowar", "Chepkorio", "Chebara", "Flax"],
    "embu": ["Embu Town", "Runyenjes", "Siakago", "Kiritiri", "Ishiara"],
    "garissa": ["Garissa Town", "Dadaab", "Masalani", "Hulugho", "Modogashe"],
    "homa_bay": ["Homa Bay Town", "Mbita", "Kendu Bay", "Rodi Kopany", "Oyugis"],
    "isiolo": ["Isiolo Town", "Merti", "Kinna", "Garbatulla", "Oldonyiro"],
    "kajiado": ["Kajiado Town", "Ngong", "Kitengela", "Loitoktok", "Ongata Rongai"],
    "kakamega": ["Kakamega Town", "Mumias", "Butere", "Lugari", "Malava"],
    "kericho": ["Kericho Town", "Litein", "Kipkelion", "Chepseon", "Kapsoit"],
    "kiambu": ["Kiambu Town", "Thika", "Ruiru", "Githunguri", "Limuru", "Kikuyu", "Juja"],
    "kilifi": ["Kilifi Town", "Malindi", "Watamu", "Mtwapa", "Mariakani"],
    "kirinyaga": ["Kerugoya", "Kutus", "Sagana", "Wanguru", "Kianyaga"],
    "kisii": ["Kisii Town", "Ogembo", "Nyamache", "Masimba", "Keumbu"],
    "kisumu": ["Kisumu City", "Maseno", "Ahero", "Muhoroni", "Nyamasaria"],
    "kitui": ["Kitui Town", "Mwingi", "Mutomo", "Zombe", "Kwa Vonza"],
    "kwale": ["Kwale Town", "Diani", "Msambweni", "Kinango", "Lunga Lunga"],
    "laikipia": ["Nanyuki", "Nyahururu", "Rumuruti", "Doldol", "Kinamba"],
    "lamu": ["Lamu Town", "Mokowe", "Faza", "Kizingitini", "Mpeketoni"],
    "machakos": ["Machakos Town", "Mwala", "Kangundo", "Matuu", "Kathiani"],
    "makueni": ["Wote", "Emali", "Kibwezi", "Sultan Hamud", "Makindu"],
    "mandera": ["Mandera Town", "El Wak", "Rhamu", "Takaba", "Banisa"],
    "marsabit": ["Marsabit Town", "Moyale", "Sololo", "Laisamis", "North Horr"],
    "meru": ["Meru Town", "Maua", "Timau", "Nkubu", "Mitunguu"],
    "migori": ["Migori Town", "Kehancha", "Awendo", "Rongo", "Isebania"],
    "mombasa": ["Mombasa Island", "Nyali", "Likoni", "Changamwe", "Kisauni"],
    "murang_a": ["Murang'a Town", "Kangema", "Kiriaini", "Kahuro", "Makuyu"],
    "nairobi": ["Westlands", "Kibra", "Kasarani", "Embakasi", "Lang'ata"],
    "nakuru": ["Nakuru Town", "Naivasha", "Gilgil", "Molo", "Subukia"],
    "nandi": ["Kapsabet", "Nandi Hills", "Mosoriot", "Kabiyet", "Chepkumia"],
    "narok": ["Narok Town", "Kilgoris", "Ololulung'a", "Lolgorian", "Emurua Dikirr"],
    "nyamira": ["Nyamira Town", "Keroka", "Ekerenyo", "Magombo", "Nyansiongo"],
    "nyandarua": ["Ol Kalou", "Engineer", "Mairo Inya", "Njabini", "Ndaragua"],
    "nyeri": ["Nyeri Town", "Othaya", "Mukurweini", "Karatina", "Chaka"],
    "samburu": ["Maralal", "Baragoi", "Wamba", "Archers Post", "Suguta Marmar"],
    "siaya": ["Siaya Town", "Bondo", "Usenge", "Ugunja", "Yala"],
    "taita_taveta": ["Voi", "Taveta", "Wundanyi", "Mwatate", "Maungu"],
    "tana_river": ["Hola", "Garsen", "Bura", "Madogo", "Kipini"],
    "tharaka_nithi": ["Chuka", "Marimanti", "Kathwana", "Chiakariga", "Gatunga"],
    "trans_nzoia": ["Kitale", "Kiminini", "Endebess", "Saboti", "Kapenguria"],
    "turkana": ["Lodwar", "Lokichogio", "Kakuma", "Lokori", "Kalokol"],
    "uasin_gishu": ["Eldoret", "Burnt Forest", "Kapsabet", "Moiben", "Tembelio"],
    "vihiga": ["Vihiga", "Mbale", "Chavakali", "Luanda", "Majengo"],
    "wajir": ["Wajir Town", "Bute", "Griftu", "Eldas", "Tarbaj"],
    "west_pokot": ["Kapenguria", "Lokichar", "Alale", "Sigor", "Kacheliba"],
}
