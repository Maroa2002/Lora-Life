"""
This module defines the routes for farmer-related functionalities in the Flask application.

It includes the following routes:
- View and update farmer profile
- View available vets
- View vet availability slots
- Book an appointment
- View farmer appointments

Functions:
- farmer_profile(): Allows farmers to view and update their profile.
- find_vets(): Allows farmers to view available vets.
- vet_availability(vet_id): Allows farmers to view a vet's availability slots.
- book_appointment(slot_id): Allows farmers to book an appointment with a vet.
- farmer_appointments(): Allows farmers to view their appointments.
"""

from flask import current_app, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import db, Appointment, Vet, VetAvailability, Livestock
from app.utils import send_email
from datetime import datetime
from .forms import LivestockForm

from . import farmer_bp

@farmer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def farmer_profile():
    """
    Route to view and update farmer profile.

    GET: Renders the profile page.
    POST: Processes the profile update form.

    Returns:
        Response: Rendered HTML template for viewing and updating the farmer profile.
    """
    if current_user.user_role != 'farmer':
        abort(403)
    
    appointments = Appointment.query.filter(
        Appointment.farmer_id == current_user.id
    ).all()
    
    return render_template('farmer_profile.html', appointments=appointments)

@farmer_bp.route('/find-vets', methods=['GET'])
@login_required
def find_vets():
    """
    Route for farmers to view available vets.

    Returns:
        Response: Rendered HTML template for viewing available vets.
    """
    if current_user.user_role != 'farmer':
        abort(403)

    vets = Vet.query.all()
    return render_template('find_vets.html', vets=vets)

@farmer_bp.route('/vet/<int:vet_id>/availability', methods=['GET'])
@login_required
def vet_availability(vet_id):
    """
    Route for farmers to view a vet's availability slots.

    Args:
        vet_id (int): The ID of the vet whose availability slots are to be viewed.

    Returns:
        Response: Rendered HTML template for viewing vet availability slots.
    """
    vet = Vet.query.get_or_404(vet_id)
    
    # Get available slots in the future
    availability_slots = VetAvailability.query.filter(
        VetAvailability.vet_id == vet.user_id,
        VetAvailability.start_time > datetime.utcnow(),
        VetAvailability.is_booked == False
        ).order_by(VetAvailability.start_time.asc()).all()
    
    return render_template('vet_availability.html', vet=vet, availability_slots=availability_slots)

@farmer_bp.route('/book_appointment/<int:slot_id>', methods=['POST'])
@login_required
def book_appointment(slot_id):
    """
    Route for farmers to book an appointment with a vet.

    Args:
        slot_id (int): The ID of the slot to book.

    Returns:
        Response: Redirects to the farmer profile page with a success or error message.
    """
    if current_user.user_role != 'farmer':
        abort(403)
        
    slot = VetAvailability.query.get_or_404(slot_id)
    
    if slot.is_booked:
        flash('This slot is already booked', 'danger')
        return redirect(url_for('farmer.vet_availability', vet_id=slot.vet_id))
    
    if slot.start_time < datetime.utcnow():
        flash('Cannot book past availability slots', 'danger')
        return redirect(url_for('farmer.vet_availability', vet_id=slot.vet_id))
    
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
        current_app.logger.error('No vet found with user_id {}'.format(slot.vet_id))
        # Notify the user
        flash('Appointment booked, but vet notification failed. Please contact support.', 'warning')
    
    flash('Appointment booked successfully', 'success')
    return redirect(url_for('farmer.farmer_profile'))

@farmer_bp.route('/add-livestock', methods=['GET', 'POST'])
@login_required
def add_livestock():
    """
    Route for farmers to add livestock.

    Returns:
        Response: Rendered HTML template for adding livestock.
    """
    if current_user.user_role != 'farmer':
        abort(403)
        
    form = LivestockForm()
    
    if form.validate_on_submit():
        livestock = Livestock(
            farmer_id =current_user.id,
            name = form.name.data,
            age = form.age.data,
            breed = form.breed.data,
            weight = form.weight.data
        )
        
        db.session.add(livestock)
        db.session.commit()
        
        flash('Livestock added successfully', 'success')
        return redirect(url_for('farmer.farmer_profile'))
    
    return render_template('add_livestock.html', form=form)

@farmer_bp.route('/appointments', methods=['GET'])
@login_required
def farmer_appointments():
    """
    Route for farmers to view their appointments.

    Returns:
        Response: Rendered HTML template for viewing farmer appointments.
    """
    if current_user.user_role != 'farmer':
        abort(403)
        
    appointments = Appointment.query.filter_by(farmer_id=current_user.id)\
        .order_by(Appointment.created_at.desc()).all()
    
    return render_template('farmer_appointments.html', appointments=appointments)

