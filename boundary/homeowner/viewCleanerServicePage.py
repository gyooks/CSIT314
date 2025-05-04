from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.homeowner.viewServiceController import viewCleanerServiceController
from controller.homeowner.shortlistServiceController import shortlistServiceController
from controller.homeowner.bookingServiceController import BookingServiceController
from entity.Category import Category
from datetime import datetime

# Create Homeowner Service Management Blueprint
CleanerServiceManagementUI_bp = Blueprint('CleanerServiceManagementUI', __name__, url_prefix='/homeowner')

# Cleaner Service Listing View
@CleanerServiceManagementUI_bp.route('/services')
def view_services():
    """
    Display all cleaning services available to homeowners
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    homeowner_id = session['user_id']
    
    # Get category filter if any
    category_id = request.args.get('category_id', None)
    
    # Get all services with cleaner info
    if category_id:
        services = viewCleanerServiceController.get_services_by_category(category_id)
    else:
        services = viewCleanerServiceController.get_all_services()
    
    # Get all active categories for filtering
    categories = Category.get_all_active()
    
    # Get shortlisted service IDs for this homeowner
    shortlisted_services = viewCleanerServiceController.get_shortlisted_service_ids(homeowner_id)
    
    # Get today's date for the booking form
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('homeowner/serviceListingPage.html', 
                           services=services, 
                           categories=categories, 
                           selected_category=category_id,
                           shortlisted_services=shortlisted_services,
                           today=today)


# Shortlist Service
@CleanerServiceManagementUI_bp.route('/services/shortlist/<int:service_id>', methods=['POST'])
def shortlist_service(service_id):
    """
    Add a service to the homeowner's shortlist
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    homeowner_id = session['user_id']
    
    # Shortlist the service
    success, message = shortlistServiceController.add_to_shortlist(homeowner_id, service_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(request.referrer or url_for('CleanerServiceManagementUI.view_services'))



# Book Service
@CleanerServiceManagementUI_bp.route('/services/book/<int:service_id>', methods=['POST'])
def book_service(service_id):
    """
    Book a cleaning service
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    homeowner_id = session['user_id']
    booking_date = request.form.get('booking_date')
    hours = request.form.get('hours', 1)
    
    if not booking_date:
        flash("Booking date is required", "danger")
        return redirect(url_for('CleanerServiceManagementUI.view_services', service_id=service_id))
    
    # Book the service
    success, message = BookingServiceController.create_booking(homeowner_id, service_id, booking_date, hours)
    
    if success:
        flash(message, "success")
        return redirect(url_for('viewBookingPage.view_bookings'))
    else:
        flash(message, "danger")
        return redirect(url_for('CleanerServiceManagementUI.view_services', service_id=service_id))

# Search Services
@CleanerServiceManagementUI_bp.route('/services/search', methods=['GET'])
def search_services():
    """
    Search services by keyword
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    homeowner_id = session['user_id']
    
    # Get search keyword
    keyword = request.args.get('keyword', '')
    
    # Search services
    services = viewCleanerServiceController.search_services(keyword)
    
    # Get all active categories for filtering
    categories = Category.get_all_active()
    selected_category = request.args.get('category_id')
    
    # Get shortlisted service IDs for this homeowner
    shortlisted_services = viewCleanerServiceController.get_shortlisted_service_ids(homeowner_id)
    
    # Get today's date for the booking form
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('homeowner/serviceListingPage.html', 
                           services=services, 
                           categories=categories, 
                           search_keyword=keyword,
                           selected_category=None,
                           shortlisted_services=shortlisted_services,
                           today=today)