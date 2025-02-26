from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Farmer, Vet, VetAvailability, Appointment
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from datetime import datetime
import smtplib

# load environment variables from .env
load_dotenv()


# Fetch database credentials from environment variables
db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PwD")
db_name = os.getenv("MYSQL_DB")
app_secret_key = os.getenv('SECRET_KEY')

# Fetch email credentials from env variables
email_user = os.getenv("EMAIL_USER")
email_password = os.getenv("EMAIL_PASSWORD")


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
    """
    Route to render the home page.
    """
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route to handle user login.
    GET: Renders the login form.
    POST: Processes the login form and logs in the user.
    """
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
            return redirect(url_for('farmer_appointments'))
        elif user.user_role == 'vet':
            return redirect(url_for('vet_profile'))
            

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    """
    Route to handle user registration.
    GET: Renders the registration form.
    POST: Processes the registration form and registers the user.
    """
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
@app.route('/find-vets', methods=['GET'])
@login_required
def find_vets():
    """
    Route for farmers to view available vets.
    """
    if current_user.user_role != 'farmer':
        abort(403)

    vets = Vet.query.all()
    return render_template('find_vets.html', vets=vets)


# Farmer - view vet availabilty slots
@app.route('/vet/<int:vet_id>/availability', methods=['GET'])
@login_required
def vet_availability(vet_id):
    """
    Route for farmers to view a vet's availability slots.
    """
    vet = Vet.query.get_or_404(vet_id)
    
    # Get availables slots in the future
    availability_slots = VetAvailability.query.filter(
        VetAvailability.vet_id == vet.user_id,
        VetAvailability.start_time > datetime.utcnow(),
        VetAvailability.is_booked == False
        ).order_by(VetAvailability.start_time.asc()).all()
    
    return render_template('vet_availability.html', vet=vet, availability_slots=availability_slots)


# Farmer - Book an appointment
@app.route('/book_appointment/<int:slot_id>', methods=['POST'])
@login_required
def book_appointment(slot_id):
    """
    Route for farmers to book an appointment with a vet.
    """
    if current_user.user_role != 'farmer':
        abort(403)
        
    slot = VetAvailability.query.get_or_404(slot_id)
    
    if slot.is_booked:
        flash('This slot is already booked', 'danger')
        return redirect(url_for('vet_availability'))
    
    if slot.start_time < datetime.utcnow():
        flash('Cannot book past availability slots', 'danger')
        return redirect(url_for('vet_availability'))
    
    appointment = Appointment(
        farmer_id=current_user.id,
        vet_id=slot.vet_id,
        slot_id=slot.id,
        notes=request.form.get('notes', '')
    )
    
    slot.is_booked = True
    db.session.add(appointment)
    db.session.commit()
    
    # Send Email to Vet
    vet = Vet.query.filter_by(user_id=slot.vet_id).first()
    if vet:
        vet_email = vet.user.email
        message = f"Hello {vet.user.full_name},\n\nYou have a new appointment with {current_user.full_name} on {slot.start_time}."
        msg = 'Subject: New Appointment\n\n{}'.format(message)
        send_email(vet_email, msg)
    else:
        # Log the error
        app.logger.error('No vet found with user_id {}'.format(slot.vet_id))
        # Notify the user
        flash('Appointment booked, but vet notification failed. Please contact support.', 'warning')
    
    flash('Appointment booked successfully', 'success')
    return redirect(url_for('farmer_appointments'))


# Farmer - view appointments
@app.route('/farmer/appointments')
@login_required
def farmer_appointments():
    """
    Route for farmers to view their appointments.
    """
    if current_user.user_role != 'farmer':
        abort(403)
        
    appointments = Appointment.query.filter_by(farmer_id=current_user.id)\
        .order_by(Appointment.created_at.desc()).all()
    
    return render_template('farmer_appointments.html', appointments=appointments)


# Vet - Manage Availability
@app.route('/vet/manage_availability', methods=['GET', 'POST'])
@login_required
def manage_availability():
    """
    Route for vets to manage their availability slots.
    GET: Renders the form to add availability slots and shows existing slots.
    POST: Processes the form to add a new availability slot.
    """
    if current_user.user_role != 'vet':
        abort(403)
        
    if request.method == 'POST':
        try:
            start_time = datetime.fromisoformat(request.form.get('start_time'))
            end_time = datetime.fromisoformat(request.form.get('end_time'))
            
            if start_time >= end_time:
                flash('End time must be after start time', 'danger')
                return redirect(url_for('manage_availability'))
            
            # check for overlapping slots
            overlapping = VetAvailability.query.filter(
                VetAvailability.vet_id == current_user.id,
                VetAvailability.start_time < end_time,
                VetAvailability.end_time > start_time
            ).first()
            
            if overlapping:
                flash('Time slot overlaps with existing availability', 'danger')
                return redirect(url_for('manage_availability'))
            
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
            
        return redirect(url_for('manage_availability'))
    
    # Get request - show existing slots
    slots = VetAvailability.query.filter_by(vet_id=current_user.id)\
            .order_by(VetAvailability.start_time.asc()).all()
    return render_template('manage_availability.html', slots=slots)


# Vet - Delete availability slot
@app.route('/vet/manage_availability/<int:slot_id>/delete', methods=['POST'])
@login_required
def delete_availability(slot_id):
    """
    Route for vets to delete an availability slot.
    """
    slot = VetAvailability.query.get_or_404(slot_id)
    if slot.vet_id != current_user.id:
        abort(403)
    
    if slot.is_booked:
        flash('Cannot delete a booked slot', 'danger')
    else:
        db.session.delete(slot)
        db.session.commit()
        flash('Slot deleted successfully', 'success')
    
    return redirect(url_for('manage_availability'))


# Vet - View Appointments
@app.route('/vet/appointments', methods=['GET'])
@login_required
def view_appointments():
    """
    Route for vets to view their appointments.
    """
    if current_user.user_role != 'vet':
        abort(403)
        
    appointments = Appointment.query.filter(
        Appointment.vet_id == current_user.id
    ).all()
    return render_template('vet_appointments.html', appointments=appointments)



# Vet - manage appointments
@app.route('/vet/appointment/<int:appointment_id>/<action>', methods=['POST'])
@login_required
def manage_appointment(appointment_id, action):
    """
    Route for vets to manage appointments.
    """
    if current_user.user_role != 'vet':
        abort(403)
        
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if action == 'confirm':
        appointment.status = 'confirmed'
        message = f"Hello {appointment.farmer.full_name},\n\nYour appointment with Dr {current_user.full_name} has been confirmed."
        msg = 'Subject: Appointment Confirmed\n\n{}'.format(message)
        send_email(appointment.farmer.email, msg)
        flash('Appointment confirmed', 'success')
    elif action == 'cancel':
        appointment.status = 'cancelled'
        message = f"Hello {appointment.farmer.full_name},\n\nYour appointment with Dr {current_user.full_name} has been cancelled."
        msg = 'Subject: Appointment Cancelled\n\n{}'.format(message)
        send_email(appointment.farmer.email, msg)
        appointment.slot.is_booked = False
        flash('Appointment cancelled', 'danger')
    elif action == 'complete':
        appointment.status = 'completed'
        flash('Appointment completed', 'success')
    elif action == 'delete':
        db.session.delete(appointment)
        flash('Appointment deleted', 'danger')
    else:
        flash('Invalid action', 'danger')
    
    db.session.commit()
    return redirect(url_for('vet_profile'))


# Vet - view profile
@app.route('/vet/profile', methods=['GET', 'POST'])
@login_required
def vet_profile():
    """
    Route to view and update user profile.
    GET: Renders the profile page.
    POST: Processes the profile update form.
    """
    if current_user.user_role != 'vet':
        abort(403)
    
    appointments = Appointment.query.filter(
        Appointment.vet_id == current_user.id
    ).all()
    
    return render_template('profile.html', appointments=appointments)


@app.route('/contact', methods=['POST'])
def contact():
    """
    Route to handle contact form submission.
    """
    user_name = request.form.get('name')
    user_email = request.form.get('email')
    message = request.form.get('message')
    
    msg = "Subject: Contatct Us\n\n{}\n\n{}\n\n{}".format(user_name, user_email, message)
    
    send_email(user_email, msg)
    flash('Message sent successfully', 'success')
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    """
    Route to log out the current user.
    """
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


def allowed_file(filename):
    """
    Helper function to check if a file is allowed based on its extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def send_email(recipient_email, msg):
    """
    Helper function to send an email.
    """
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, recipient_email, msg=msg)
        server.quit()
    except smtplib.SMTPException as e:
        print('Error sending email: {}'.format(e))
    except Exception as e:
        print('Error: {}'.format(e))

if __name__ == '__main__':
    app.run(debug=True)