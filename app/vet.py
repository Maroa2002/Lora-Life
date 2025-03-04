"""
This module defines the routes for vet-related functionalities in the Flask application.

It includes the following routes:
- Manage availability slots
- Delete availability slot
- View appointments
- Manage appointments
- View and update vet profile

Functions:
- manage_availability(): Allows vets to manage their availability slots.
- delete_availability(slot_id): Allows vets to delete an availability slot.
- view_appointments(): Allows vets to view their appointments.
- manage_appointment(appointment_id, action): Allows vets to manage appointments.
- vet_profile(): Allows vets to view and update their profile.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import db, VetAvailability, Appointment
from .email_service import send_email
from datetime import datetime
from flask_login import login_required, current_user

vet_bp = Blueprint('vet', __name__)

@vet_bp.route('/manage_availability', methods=['GET', 'POST'])
@login_required
def manage_availability():
    """
    Route for vets to manage their availability slots.
    
    GET: Renders the form to add availability slots and shows existing slots.
    POST: Processes the form to add a new availability slot.
    
    Returns:
        Response: Rendered HTML template for managing availability slots.
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

@vet_bp.route('/manage_availability/<int:slot_id>/delete', methods=['POST'])
@login_required
def delete_availability(slot_id):
    """
    Route for vets to delete an availability slot.
    
    Args:
        slot_id (int): The ID of the slot to delete.
    
    Returns:
        Response: Redirects to the manage availability page with a success or error message.
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

@vet_bp.route('/appointments', methods=['GET'])
@login_required
def view_appointments():
    """
    Route for vets to view their appointments.
    
    Returns:
        Response: Rendered HTML template for viewing appointments.
    """
    if current_user.user_role != 'vet':
        abort(403)
        
    appointments = Appointment.query.filter(
        Appointment.vet_id == current_user.id
    ).all()
    return render_template('vet_appointments.html', appointments=appointments)

@vet_bp.route('/appointment/<int:appointment_id>/<action>', methods=['POST'])
@login_required
def manage_appointment(appointment_id, action):
    """
    Route for vets to manage appointments.
    
    Args:
        appointment_id (int): The ID of the appointment to manage.
        action (str): The action to perform on the appointment (confirm, cancel, complete, delete).
    
    Returns:
        Response: Redirects to the vet profile page with a success or error message.
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

@vet_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def vet_profile():
    """
    Route to view and update user profile.
    
    GET: Renders the profile page.
    POST: Processes the profile update form.
    
    Returns:
        Response: Rendered HTML template for viewing and updating the vet profile.
    """
    if current_user.user_role != 'vet':
        abort(403)
    
    appointments = Appointment.query.filter(
        Appointment.vet_id == current_user.id
    ).all()
    
    return render_template('vet_profile.html', appointments=appointments)
