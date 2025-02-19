from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Farmer, Vet, VetAvailability, Appointment
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from datetime import datetime

# load environment variables from .env
load_dotenv()


# Fetch database credentials from environment variables
db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PwD")
db_name = os.getenv("MYSQL_DB")
app_secret_key = os.getenv('SECRET_KEY')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = app_secret_key

db.init_app(app)
migrate = Migrate(app, db)

# Initialize the Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# loader for Flask_Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Basic validation
        if not email or not password:
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        
        # check if the user exists and the password is correct
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        
        # login the user
        login_user(user)
        flash('Login successful!', 'success')
        
        # redirect based on role
        if user.user_role == 'farmer':
            return redirect(url_for('home'))
        elif user.user_role == 'vet':
            return redirect(url_for('home'))
            

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        print(request.form)
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
                    verification_document_path = file_path,
                    clinic_name = request.form.get('clinic_name'),
                    service_area = request.form.get('service_area')
                )
                new_user.vet_profile = vet
        
            # save to database
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            return redirect(url_for('register'))
    
    # GET request - show registration form 
    return render_template('register.html')


# Farmer - View Available vets
@app.route('/vets', methods=['GET'])
@login_required
def list_vets():
    if current_user.user_role != 'farmer':
        abort(403)

    vets = Vet.query.all()
    return render_template('list_vets.html', vets=vets)


# Farmer - view vet availabilty slots
@app.route('/vet/<int:vet_id>/availability', methods=['GET'])
@login_required
def vet_availability(vet_id):
    vet = Vet.query.get_or_404(vet_id)
    availability_slots = VetAvailability.query.filter_by(vet_id=vet.user_id, is_booked=False).all()
    
    return render_template('vet_availability.html', vet=vet, availability_slots=availability_slots)


# Vet - Manage Availability
@app.route('/vet/add_availability', methods=['GET', 'POST'])
@login_required
def add_availability():
    if current_user.user_role != 'vet':
        abort(403)
        
    if request.method == 'POST':
        try:
            start_time = datetime.fromisoformat(request.form.get('start_time'))
            end_time = datetime.fromisoformat(request.form.get('end_time'))
            
            if start_time >= end_time:
                flash('End time must be after start time', 'danger')
                return redirect(url_for('add_availability'))
            
            # check for overlapping slots
            overlapping = VetAvailability.query.filter(
                VetAvailability.vet_id == current_user.id,
                VetAvailability.start_time < end_time,
                VetAvailability.end_time > start_time
            ).first()
            
            if overlapping:
                flash('Time slot overlaps with existing availability', 'danger')
                return redirect(url_for('add_availability'))
            
            new_slot = VetAvailability(
                vet_id=current_user.id,
                start_time=start_time,
                end_time=end_time,
                is_booked=False
            )
            
            db.session.add(new_slot)
            db.session.commit()
            flash('Availability slot added successfully', 'success')
            
        except ValueError:
            flash('Invalid date/time format', 'danger')
            
        return redirect(url_for('add_availability'))
    
    # Get request - show existing slots
    slots = VetAvailability.query.filter_by(vet_id=current_user.id)\
            .order_by(VetAvailability.start_time.asc()).all()
    return render_template('add_availability.html', slots=slots)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)