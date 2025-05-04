from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from controller.admin.viewUserProfileController import viewUserProfileController
from controller.admin.searchUserProfileController import SearchProfileController
from controller.admin.suspendUserProfileController import SuspendProfileController
from controller.admin.updateUserProfileController import UpdateProfileController

# Create a single blueprint for all profile management routes
profile_management_bp = Blueprint('profile_management', __name__, url_prefix='/profile')

# View profile routes
@profile_management_bp.route('/view', methods=['GET'])
def view_profile():
    """
    View a user profile by profile ID
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    userprofiles = viewUserProfileController.get_all_profiles()
    
    # Render profile detail template
    return render_template('admin/userProfileManagementPage.html', userprofiles=userprofiles)

# Update profile routes
@profile_management_bp.route('/edit/<int:profile_id>', methods=['GET', 'POST'])
def update_profile(profile_id):
    """
    Update a user profile
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # GET request - show the update form
    if request.method == 'GET':
        # Get profile from controller
        userprofiles = UpdateProfileController.get_profile_by_profile_id(profile_id)
        
        if not userprofiles:
            flash("Profile not found", "error")
            return redirect(url_for('profile_management.view_profile'))
        
        # Render update profile form
        return render_template('admin/editProfile.html', userprofiles=userprofiles)
    
    # POST request - update the profile
    elif request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        # Update profile through controller
        success, message = UpdateProfileController.update_profile(
            profile_id=profile_id,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone
        )
        
        if success:
            flash(message, "success")
            return redirect(url_for('profile_management.view_profile', profile_id=profile_id))
        else:
            flash(message, "error")
            return render_template('admin/updateProfile.html', 
                                  profile=viewUserProfileController.get_profile_by_profile_id(profile_id))

# Delete profile route
@profile_management_bp.route('/delete/<int:profile_id>', methods=['POST'])
def delete_profile(profile_id):
    """
    Delete a user profile
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Delete profile through controller
    success, message = DeleteProfileController.delete_profile(profile_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    # Redirect back to dashboard after deletion
    return redirect(url_for('profile_management.view_profile'))

# Suspend/Reactivate profile routes
@profile_management_bp.route('/suspend/<int:profile_id>', methods=['POST'])
def suspend_profile(profile_id):
    """
    Suspend a user profile
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Suspend profile through controller
    success, message = SuspendProfileController.suspend_profile(profile_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    # Redirect back to profile view
    return redirect(url_for('profile_management.view_profile', profile_id=profile_id))

@profile_management_bp.route('/reactivate/<int:profile_id>', methods=['POST'])
def reactivate_profile(profile_id):
    """
    Reactivate a suspended user profile
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Reactivate profile through controller
    success, message = SuspendProfileController.reactivate_profile(profile_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    # Redirect back to profile view
    return redirect(url_for('profile_management.view_profile', profile_id=profile_id))

# Search profile route
@profile_management_bp.route('/search', methods=['GET', 'POST'])
def search_profile():
    """
    Search user profiles
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    keyword = ""
    userprofiles = []  #match with html page...
    
    # Check if it's a POST request (search form submitted)
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        if keyword:
            # Get search results from controller
            userprofiles = SearchProfileController.search_profiles(keyword)
    
    # Render the template with search results
    return render_template('admin/userProfileManagementPage.html', 
                          userprofiles=userprofiles, 
                          search_keyword=keyword)