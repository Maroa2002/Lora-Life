"""
This module initializes the Flask application and its extensions.

It sets up the following:
- Flask application instance
- SQLAlchemy for database interactions
- Flask-Login for user session management
- Flask-Migrate for database migrations
- Flask-CORS for handling Cross-Origin Resource Sharing (CORS)
- Environment variables for configuration

The module also registers blueprints for different parts of the application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up database configurations
db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PwD")
db_name = os.getenv("MYSQL_DB")
app_secret_key = os.getenv('SECRET_KEY')

# Set up file upload configurations
UPLOAD_FOLDER = 'uploads'

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Load app configurations
    app.config['SECRET_KEY'] = app_secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Initialize Flask extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import blueprints
    from .auth import auth_bp as auth_blueprint
    from .farmer import farmer_bp as farmer_blueprint
    from .vet import vet_bp as vet_blueprint
    from .chatbot import chatbot_bp as chatbot_blueprint
    from .main import main_bp as main_blueprint
    
    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(farmer_blueprint, url_prefix='/farmer')
    app.register_blueprint(vet_blueprint, url_prefix='/vet')
    app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')
    
    return app