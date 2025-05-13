from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.homeowner.bookingServiceController import BookingServiceController
from controller.homeowner.searchBookingController import SearchBookingController
from datetime import datetime

# Create Homeowner Booking Management Blueprint
viewBookingPage_bp = Blueprint('viewBookingPage', __name__, url_prefix='/homeowner')

# View all bookings
@viewBookingPage_bp.route('/bookings')
def view_bookings():
    """
    Display all bookings made by the homeowner
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    homeowner_id = session['user_id']
    
    # Get status filter if any
    status = request.args.get('status', None)
    
    # Get search keyword if any
    keyword = request.args.get('keyword', '')
    
    # Get all bookings for this homeowner with optional filters
    if keyword:
        bookings = SearchBookingController.search_bookings(homeowner_id, keyword)
    elif status:
        bookings = BookingServiceController.get_bookings_by_status(homeowner_id, status)
    else:
        bookings = BookingServiceController.get_all_bookings(homeowner_id)
    
    # Get all possible booking statuses for filtering
    statuses = ['Pending', 'Confirmed', 'Completed', 'Cancelled', 'Rejected']
    
    return render_template('homeowner/bookingListingPage.html', 
                           bookings=bookings, 
                           statuses=statuses,
                           selected_status=status,
                           search_keyword=keyword)

# Cancel booking
@viewBookingPage_bp.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    """
    Cancel a booking
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    homeowner_id = session['user_id']
    
    # Cancel the booking
    from controller.homeowner.bookingServiceController import bookingServiceController
    success, message = bookingServiceController.cancel_booking(booking_id, homeowner_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('viewBookingPage.view_bookings'))

# Search bookings
@viewBookingPage_bp.route('/bookings/search', methods=['GET'])
def search_bookings():
    """
    Search bookings by keyword
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    return redirect(url_for('viewBookingPage.view_bookings', keyword=request.args.get('keyword', '')))