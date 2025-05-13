from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from controller.admin.viewUserAccController import viewUserAccController  
from controller.admin.viewUserAccDetailController import viewUserAccDetailController
from controller.admin.searchUserAccController import SearchUserAccController
from controller.admin.suspendUserAccController import SuspendUserAccController
from controller.admin.updateUserAccController import UpdateUserAccController
from controller.admin.createUserAccController import createUserAccController
from controller.admin.reactivateUserAccController import reactivateUserAccController

from db_config import db
from entity.UserProfile import UserProfile

# Create a blueprint for all user management routes
user_management_bp = Blueprint('user_management', __name__, url_prefix='/users')

# View users route
@user_management_bp.route('/view', methods=['GET'])
def view_users():
    """
    View all users
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    users = viewUserAccController.get_all_users()
    
    # Render user management template
    return render_template('admin/userManagementPage.html', users=users)


@user_management_bp.route('/detail/<int:target_user_id>', methods=['GET'])
def view_user_detail(target_user_id):
    """
    View detailed information about a specific user
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Get user details from controller
    user, error_message = viewUserAccDetailController.get_user_with_details(target_user_id)
    
    # If user not found or error occurred
    if not user:
        flash(error_message or "User not found", "error")
        return redirect(url_for('user_management.view_users'))
    
    # Render the user detail template
    return render_template('admin/userDetailPage.html', user=user)

@user_management_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    
    # This would typically have authentication checks to ensure only admins can access
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    user_id = session['user_id']
        
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role_id = request.form.get('role_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        # Basic validation
        if not email or not password or not role_id:
            flash('Email, password, and role are required fields', 'error')
            # Get user profiles (roles) for the form
            profiles = UserProfile.get_all_active()
            return render_template('admin/createUserAccPage.html', profiles=profiles)
            
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            # Get user profiles (roles) for the form
            profiles = UserProfile.get_all_active()
            return render_template('admin/createUserAccPage.html', profiles=profiles)
        
        # Use the controller to create user with all profile info in one operation
        success, message, new_user_id = createUserAccController.create_user(
            email=email,
            password=password,
            role_id=int(role_id),  # Convert to int since form data comes as string
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone
        )
        
        if not success:
            flash(message, 'error')
            # Get user profiles (roles) for the form
            profiles = UserProfile.get_all_active()
            return render_template('admin/createUserAccPage.html', profiles=profiles)
                
        flash("User created successfully", 'success')
        return redirect(url_for('user_management.view_users'))
    
    # GET request - show the form
    # Fetch all user profiles from the database to populate the dropdown
    profiles = UserProfile.get_all_active()
    return render_template('admin/createUserAccPage.html', profiles=profiles)

@user_management_bp.route('/edit/<int:target_user_id>', methods=['GET', 'POST'])
def update_user(target_user_id):
    """
    Update a user
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
        
    # GET request - show the update form
    if request.method == 'GET':
        # Get user from controller with the combined method
        success, message, user = UpdateUserAccController.update_user(target_user_id)
        
        if not success:
            flash(message, "error")
            return redirect(url_for('user_management.view_users'))
        
        # Get all available roles/profiles for dropdown
        from entity.UserProfile import UserProfile
        profiles = UserProfile.get_all_active()
        
        # Render update user form
        return render_template('admin/edit_user.html', user=user, profiles=profiles)
        
    # POST request - update the user
    elif request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        role_id = request.form.get('role_id')
        password = request.form.get('password')  # Optional - might be empty if not changing
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        # Update user through controller
        success, message, user = UpdateUserAccController.update_user(
            user_id=target_user_id,
            email=email,
            role_id=int(role_id) if role_id else None,
            password=password,  # Controller should handle empty password
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
        )
        
        if success:
            flash("User updated successfully", "success")
            return redirect(url_for('user_management.view_users'))
        else:
            flash(f"Error updating user: {message}", "error")
            from entity.UserProfile import UserProfile
            profiles = UserProfile.get_all_active()
            return render_template('admin/edit_user.html', user=user or {}, profiles=profiles)


# Suspend/Reactivate user routes
@user_management_bp.route('/suspend/<int:target_user_id>', methods=['POST'])
def suspend_user(target_user_id):
    """
    Suspend a user
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Suspend user through controller
    success, message = SuspendUserAccController.suspend_user(target_user_id)
    
    if success:
        flash("User suspended successfully", "success")
    else:
        flash(f"Error suspending user: {message}", "error")
    
    # Redirect back to user view
    return redirect(url_for('user_management.view_users'))

@user_management_bp.route('/reactivate/<int:target_user_id>', methods=['POST'])
def reactivate_user(target_user_id):
    """
    Reactivate a suspended user
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Reactivate user through controller
    success, message = reactivateUserAccController.reactivate_user(target_user_id)
    
    if success:
        flash("User reactivated successfully", "success")
    else:
        flash(f"Error reactivating user: {message}", "error")
    
    # Redirect back to user view
    return redirect(url_for('user_management.view_users'))

# Search user route
@user_management_bp.route('/search', methods=['GET', 'POST'])
def search_users():
    """
    Search users
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    keyword = ""
    users = []
    
    # Check if it's a POST request (search form submitted)
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        if keyword:
            # Get search results from controller
            users = SearchUserAccController.search_users(keyword)
    
    # Render the template with search results
    return render_template('admin/userManagementPage.html', 
                          users=users, 
                          search_keyword=keyword)