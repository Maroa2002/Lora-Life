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
from flask_mail import Mail
from .config import Config
from .health_monitoring.events import socketio

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Load app configurations
    app.config.from_object(Config)
    
    # Initialize Flask extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    mail.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from .chat_app import chat_socket
    from .health_monitoring import events
    
    # Import blueprints
    from .auth import auth_bp as auth_blueprint
    from .farmer import farmer_bp as farmer_blueprint
    from .vet import vet_bp as vet_blueprint
    from .chatbot import chatbot_bp as chatbot_blueprint
    from .main import main_bp as main_blueprint
    from .health_monitoring import health_monitoring_bp as health_monitoring_blueprint
    from .chat_app import chat_app_bp as chat_app_blueprint
    
    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(farmer_blueprint, url_prefix='/farmer')
    app.register_blueprint(vet_blueprint, url_prefix='/vet')
    app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')
    app.register_blueprint(health_monitoring_blueprint, url_prefix='/health-monitoring')
    app.register_blueprint(chat_app_blueprint, url_prefix='/chat-app')
    
    # Import models
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Function to load a user object from the database.

        Args:
            user_id (int): The ID of the user to load.

        Returns:
            User: The user object corresponding to the user ID.
        """
        return User.query.get(int(user_id))
    
    return app