from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.cleaner.viewCleaningServiceController import viewCleaningServiceController
from controller.cleaner.createCleaningServiceController import createCleaningServiceController
from controller.cleaner.searchCleaningServiceController import searchCleaningServiceController
from controller.cleaner.suspendCleaningServiceController import suspendCleaningServiceController
from controller.cleaner.updateCleaningServiceController import updateCleaningServiceController
from controller.cleaner.viewDetailServiceController import viewDetailServiceController
from entity.Category import Category

# Create Cleaner Service Management Blueprint
CleaningServiceManagementUI_bp = Blueprint('CleaningServiceManagementUI', __name__, url_prefix='/cleaner')

# Cleaning Service Management View
@CleaningServiceManagementUI_bp.route('/services')
def manage_services():
    """
    Display all cleaning services for the logged-in cleaner
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Get all services for this cleaner with shortlist counts
    services = viewCleaningServiceController.get_cleaner_services_with_shortlist_count(cleaner_id)
    return render_template('cleaner/serviceManagementPage.html', services=services)

# Service Detail View
@CleaningServiceManagementUI_bp.route('/services/detail/<int:service_id>')
def view_service_detail(service_id):
    """
    Display detailed information for a specific cleaning service
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Get service details with verification that it belongs to this cleaner
    service_detail = viewDetailServiceController.get_service_detail(service_id, cleaner_id)
    
    if not service_detail:
        flash("Service not found or you don't have permission to view it.", "danger")
        return redirect(url_for('CleaningServiceManagementUI.manage_services'))
    
    return render_template('cleaner/serviceDetailPage.html', service=service_detail)

# Create New Service - GET
@CleaningServiceManagementUI_bp.route('/services/create', methods=['GET'])
def create_service_form():
    """
    Show service creation form
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    # Get all active categories for the dropdown
    categories = Category.get_all_active()
    
    return render_template('cleaner/createService.html', categories=categories)

# Create New Service - POST
@CleaningServiceManagementUI_bp.route('/services/create', methods=['POST'])
def create_service():
    """
    Process service creation form
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Get form data
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    category_id = request.form.get('category_id')
    
    # Validate form data
    if not title:
        flash("Service title is required", "danger")
        return redirect(url_for('CleaningServiceManagementUI.create_service_form'))
    
    if not price:
        flash("Service price is required", "danger")
        return redirect(url_for('CleaningServiceManagementUI.create_service_form'))
    
    if not category_id:
        flash("Category is required", "danger")
        return redirect(url_for('CleaningServiceManagementUI.create_service_form'))
    
    # Create service
    success, message = createCleaningServiceController.create_service(cleaner_id, category_id, title, description, price)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('CleaningServiceManagementUI.manage_services'))

# Edit Service - GET
@CleaningServiceManagementUI_bp.route('/services/edit/<int:service_id>', methods=['GET'])
def edit_service_form(service_id):
    """
    Show service edit form
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Get service by ID
    service = updateCleaningServiceController.get_service_by_id(service_id)
    
    if not service:
        flash("Service not found.", "danger")
        return redirect(url_for('CleaningServiceManagementUI.manage_services'))
    
    # Check if this service belongs to the logged-in cleaner
    if service.cleanerID != cleaner_id:
        flash("You do not have permission to edit this service.", "danger")
        return redirect(url_for('CleaningServiceManagementUI.manage_services'))
    
    # Get all active categories for the dropdown
    categories = Category.get_all_active()
    
    return render_template('cleaner/editService.html', service=service, categories=categories)

# Edit Service - POST
@CleaningServiceManagementUI_bp.route('/services/edit/<int:service_id>', methods=['POST'])
def edit_service(service_id):
    """
    Process service edit form
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Verify ownership of service
    service = updateCleaningServiceController.get_service_by_id(service_id)
    if not service or service.cleanerID != cleaner_id:
        flash("You do not have permission to edit this service.", "danger")
        return redirect(url_for('CleaningServiceManagementUI.manage_services'))
    
    # Get form data
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    category_id = request.form.get('category_id')
    
    # Validate form data
    if not title:
        flash("Service title is required", "danger")
        return redirect(url_for('CleaningServiceManagementUI.edit_service_form', service_id=service_id))
    
    # Update service
    success = updateCleaningServiceController.update_service(service_id, title, description, price, category_id)
    
    if success:
        flash("Service updated successfully!", "success")
    else:
        flash("Failed to update service.", "danger")
    
    return redirect(url_for('CleaningServiceManagementUI.manage_services'))



# Suspend Service
@CleaningServiceManagementUI_bp.route('/services/suspend/<int:service_id>', methods=['POST'])
def suspend_service(service_id):
    """
    Suspend a service
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Verify ownership before suspension
    service = updateCleaningServiceController.get_service_by_id(service_id)
    if not service or service.cleanerID != cleaner_id:
        flash("You do not have permission to suspend this service.", "danger")
        return redirect(url_for('CleaningServiceManagementUI.manage_services'))
    
    # Suspend service
    success, message = suspendCleaningServiceController.suspend_service(service_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('CleaningServiceManagementUI.manage_services'))

# Reactivate Service
@CleaningServiceManagementUI_bp.route('/services/reactivate/<int:service_id>', methods=['POST'])
def reactivate_service(service_id):
    """
    Reactivate a service
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Verify ownership before reactivation
    service = updateCleaningServiceController.get_service_by_id(service_id)
    if not service or service.cleanerID != cleaner_id:
        flash("You do not have permission to reactivate this service.", "danger")
        return redirect(url_for('CleaningServiceManagementUI.manage_services'))
    
    # Reactivate service
    success, message = suspendCleaningServiceController.reactivate_service(service_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('CleaningServiceManagementUI.manage_services'))

# Search Services
@CleaningServiceManagementUI_bp.route('/services/search', methods=['POST'])
def search_service():
    """
    Search services by keyword
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('cleaner_login.cleanerLogin'))
    
    cleaner_id = session['user_id']
    
    # Get search keyword
    keyword = request.form.get('keyword', '')
    
    # Search services
    services = searchCleaningServiceController.search_services(cleaner_id, keyword)
    
    return render_template('cleaner/serviceManagementPage.html', 
                         services=services, 
                         search_keyword=keyword)