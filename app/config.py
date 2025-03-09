import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """
    Set Flask configuration variables.
    """
    # Load app configurations
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database configurations
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PWD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload configurations
    UPLOAD_FOLDER = 'uploads'
    PROFILE_PIC_FOLDER = 'static/uploads/profile_pics'
    VERIFICATION_FOLDER = 'static/uploads/verification'