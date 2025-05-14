from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.homeowner.searchShortlistController import SearchShortlistController
from controller.homeowner.viewShortlistController import viewShortlistController
from controller.homeowner.HomeownerGeneralFunction import HomeownerGeneralFunction

from datetime import datetime

# Create Homeowner Service Management Blueprint
viewShortlistPage_bp = Blueprint('viewShortlistPage', __name__, url_prefix='/homeowner')

# Shortlist Service Listing View
@viewShortlistPage_bp.route('/shortlist')
def view_shortlist():
    """
    Display all shortlisted cleaning services for the logged-in homeowner
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    # Get homeowner ID from session
    homeowner_id = session['user_id']
    
    # Get all shortlisted services for the homeowner
    shortlisted_services = viewShortlistController.get_homeowner_shortlist(homeowner_id)
    
    return render_template('homeowner/shortlistPage.html', shortlisted_services=shortlisted_services)

# Remove from Shortlist
@viewShortlistPage_bp.route('/shortlist/remove/<int:service_id>', methods=['POST'])
def remove_from_shortlist(service_id):
    """
    Remove a service from the homeowner's shortlist
    
    Args:
        service_id (int): ID of the service to remove
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    # Get homeowner ID from session
    homeowner_id = session['user_id']
    
    # Remove service from shortlist
    success, message = HomeownerGeneralFunction.remove_from_shortlist(homeowner_id, service_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('viewShortlistPage.view_shortlist'))

@viewShortlistPage_bp.route('/shortlist/search')
def search_shortlist():
    """
    Search through homeowner's shortlisted services
    """
    if 'user_id' not in session:
        flash("You must be logged in to search your shortlist", "danger")
        return redirect(url_for('homeowner_login.homeownerLogin'))
    
    # Get homeowner ID from session
    homeowner_id = session['user_id']
    
    # Get search keyword
    keyword = request.args.get('keyword', '')
    
    # Search shortlisted services
    shortlisted_services = SearchShortlistController.search_shortlist(homeowner_id, keyword)
    
    
    return render_template(
        'homeowner/shortlistPage.html',
        shortlisted_services=shortlisted_services,
        search_keyword=keyword,
    )