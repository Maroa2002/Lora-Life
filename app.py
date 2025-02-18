from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Farmer, Vet
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

# load environment variables from .env
load_dotenv()


# Fetch database credentials from environment variables
db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PwD")
db_name = os.getenv("MYSQL_DB")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():

    return render_template('index.html')


@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Get common data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        user_role = request.form.get('role')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        errors = []
        if not all ([full_name, email, phone, user_role, password, confirm_password]):
            errors.append('All required fields must be filled')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if user_role not in ['farmer', 'vet']:
            errors.append('Invalid user role')
            
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('register'))
        
        try:
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))
            if User.query.filter_by(phone=phone).first():
                flash('Phone number already registered', 'danger')
                return redirect(url_for('register'))

            # Create new user
            new_user = User(
                full_name = full_name,
                email = email,
                phone = phone,
                user_role = user_role
            )
            new_user.set_password(password)

            # Handling form-specific data
            if user_role == 'farmer':
                farmer = Farmer(
                    farm_name = request.form.get('farm_name'),
                    farm_location = request.form.get('farm_location')
                )
                new_user.farmer_profile = farmer
            elif user_role == 'vet':
                # Handle file upload
                if 'verification_documents' not in request.files:
                    flash('No verification document uploaded', 'danger')
                    return redirect(url_for('register'))
                
                file = request.files['verification_documents']
                if file.filename == '':
                    flash('No selected file', 'danger')
                    return redirect(url_for('register'))
                
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                else:
                    flash('Invalid file type', 'danger')
                    return redirect(url_for('register'))

                vet = Vet(
                    specialization = request.form.get('specialization'),
                    years_experience = request.form.get('years_experience'),
                    verification_document_path = request.form.get('verification_documents'),
                    clinic_name = request.form.get('clinic_name'),
                    service_area = request.form.get('service_area')
                )
                new_user.vet_profile = vet
        
            # save to database
            db.session.add(new_user)
            db.session.commit
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            return redirect(url_for('register'))
    
    # GET request - show registration form 
    return render_template('register.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)