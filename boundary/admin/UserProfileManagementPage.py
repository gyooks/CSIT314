from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from controller.admin.viewUserProfileController import ViewUserProfileController
from controller.admin.viewUserProfileDetailController import ViewUserProfileDetailController
from controller.admin.createUserProfileController import CreateUserProfileController
from controller.admin.searchUserProfileController import SearchProfileController
from controller.admin.suspendUserProfileController import SuspendProfileController
from controller.admin.updateUserProfileController import UpdateProfileController
from controller.admin.reactivateUserProfileController import reactivateUserProfileController

# Create a single blueprint for all profile (role) management routes
profile_management_bp = Blueprint('profile_management', __name__, url_prefix='/profile')

# View profile routes
@profile_management_bp.route('/view', methods=['GET'])
def view_profile():
    """
    View all user profiles (roles)
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    userprofiles = ViewUserProfileController.get_all_profiles()
    
    # Render profile management template
    return render_template('admin/userProfileManagementPage.html', userprofiles=userprofiles)



@profile_management_bp.route('/detail/<int:role_id>', methods=['GET'])
def view_profile_detail(role_id):
    """
    View details of a specific user profile (role)
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Get profile details from controller
    userprofile = ViewUserProfileDetailController.get_profile_detail(role_id)
    
    if not userprofile:
        flash("Role not found", "error")
        return redirect(url_for('profile_management.view_profile'))
    
    # Render profile detail template
    return render_template('admin/userProfileDetailPage.html', userprofile=userprofile)

# Create profile route
@profile_management_bp.route('/create', methods=['GET', 'POST'])
def create_profile():
    """
    Create a new user profile (role)
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # GET request - show the create form
    if request.method == 'GET':
        return render_template('admin/create_userProfile.html')
    
    # POST request - create the profile
    elif request.method == 'POST':
        # Get form data
        role_name = request.form.get('role_name')
        description = request.form.get('description')
        
        # Create profile through controller
        success, message = CreateUserProfileController.create_profile(
            role_name=role_name,
            description=description
        )
        
        if success:
            flash(message, "success")
            return redirect(url_for('profile_management.view_profile'))
        else:
            flash(message, "error")
            return render_template('admin/create_userProfile.html')

# Update profile route
@profile_management_bp.route('/edit/<int:role_id>', methods=['GET', 'POST'])
def update_profile(role_id):
    """
    Update a user profile (role)
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
        
    # GET request - show the update form
    if request.method == 'GET':
        # Get profile from controller using the combined method
        success, message, userprofile = UpdateProfileController.update_profile(role_id)
        
        if not success:
            flash(message, "error")
            return redirect(url_for('profile_management.view_profile'))
            
        # Render update profile form
        return render_template('admin/edit_userProfile.html', userprofile=userprofile)
        
    # POST request - update the profile
    elif request.method == 'POST':
        # Get form data
        role_name = request.form.get('role_name')
        description = request.form.get('description')
        
        # Update profile through controller
        success, message, userprofile = UpdateProfileController.update_profile(
            role_id=role_id,
            role_name=role_name,
            description=description
        )
        
        if success:
            flash(message, "success")
            return redirect(url_for('profile_management.view_profile'))
        else:
            flash(message, "error")
            return render_template('admin/edit_userProfile.html', userprofile=userprofile)
            
# Suspend/Reactivate profile routes
@profile_management_bp.route('/suspend/<int:role_id>', methods=['POST'])
def suspend_profile(role_id):
    """
    Suspend a user profile (role)
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Suspend profile through controller
    success, message = SuspendProfileController.suspend_profile(role_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    # Redirect back to profile view
    return redirect(url_for('profile_management.view_profile'))

@profile_management_bp.route('/reactivate/<int:role_id>', methods=['POST'])
def reactivate_profile(role_id):
    """
    Reactivate a suspended user profile (role)
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Reactivate profile through controller
    success, message = reactivateUserProfileController.reactivate_profile(role_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    # Redirect back to profile view
    return redirect(url_for('profile_management.view_profile'))

# Search profile route
@profile_management_bp.route('/search', methods=['GET', 'POST'])
def search_profile():
    """
    Search user profiles (roles)
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    keyword = ""
    userprofiles = []
    
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