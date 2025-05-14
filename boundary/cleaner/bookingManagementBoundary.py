from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.cleaner.viewBookingController import ViewBookingController
from controller.cleaner.filterBookingHistoryController import filterBookingHistoryController
from controller.cleaner.cleanerGeneralFunction import cleanerGeneralFunction

# Initialize the controller
viewBookingController = ViewBookingController()

# Create blueprint for booking management UI
BookingManagementUI_bp = Blueprint('BookingManagementUI', __name__, url_prefix='/cleaner')

@BookingManagementUI_bp.route('/bookings')
def manage_bookings():
    """
    Display all bookings for the logged-in cleaner
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Get status filter if provided
    status_filter = request.args.get('status', None)
    
    # Get all bookings for this cleaner with details
    if status_filter and status_filter != 'All':
        bookings = filterBookingHistoryController.filter_bookings_by_status(cleaner_id, status_filter)
    else:
        bookings = viewBookingController.get_cleaner_bookings_with_details(cleaner_id)
    
    return render_template('cleaner/bookingManagementPage.html', 
                           bookings=bookings, 
                           current_status=status_filter)

@BookingManagementUI_bp.route('/bookings/update-status/<int:booking_id>', methods=['POST'])
def update_booking_status(booking_id):
    """
    Update the status of a booking
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    new_status = request.form.get('status')
    
    # Validate the new status
    valid_statuses = ['Pending', 'Confirmed', 'Completed', 'Cancelled']
    if new_status not in valid_statuses:
        flash("Invalid status provided", "danger")
        return redirect(url_for('BookingManagementUI.manage_bookings'))
    
    # Get the booking
    booking = cleanerGeneralFunction.get_booking_by_id(booking_id)
    
    # Check if booking exists and belongs to the logged-in cleaner
    if not booking or booking.cleanerID != cleaner_id:
        flash("Booking not found or you don't have permission to update it", "danger")
        return redirect(url_for('BookingManagementUI.manage_bookings'))
    
    # Update the booking status
    if cleanerGeneralFunction.update_booking_status(booking_id, new_status):
        flash(f"Booking status updated to {new_status}", "success")
    else:
        flash("Failed to update booking status", "danger")
    
    return redirect(url_for('BookingManagementUI.manage_bookings'))